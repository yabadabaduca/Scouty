"""
Data parsing utilities for CSV, HTML, and other formats
"""

import csv
import os
from typing import List, Dict, Optional
from pathlib import Path
from .player import Player, Position

# Security limits
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
MAX_JSON_SIZE = 10 * 1024 * 1024  # 10 MB


# Mapping from Portuguese position codes to Position enum
POSITION_MAP = {
    'GO': 'GK',  # Goleiro
    'ZC': 'CD',  # Zagueiro Central
    'LD': 'WB',  # Lateral Direito
    'LE': 'WB',  # Lateral Esquerdo
    'AD': 'WB',  # Ala Direito
    'AE': 'WB',  # Ala Esquerdo
    'MC': 'IM',  # Meia Central
    'MD': 'IM',  # Meia Direito
    'ME': 'IM',  # Meia Esquerdo
    'AT': 'FW',  # Atacante
    'PD': 'FW',  # Ponta Direito
    'PE': 'FW',  # Ponta Esquerdo
}

# Mapping from Portuguese column names to English
COLUMN_MAP = {
    'ID do jogador': 'id',
    'Nome': 'name',
    'Idade': 'age',
    'Posição na última partida': 'position',
    'TSI': 'tsi',
    'Salário': 'salary',
    'Forma': 'form',
    'Resistência': 'stamina',
    'Experiência': 'experience',
    'Liderança': 'leadership',
    'Goleiro': 'goalkeeping',
    'Defesa': 'defending',
    'Armação': 'playmaking',
    'Ala': 'winger',
    'Finalização': 'scoring',
    'Bola Parada': 'set_pieces',
}


def _validate_file_path(file_path: str) -> Path:
    """Validate and normalize file path to prevent path traversal"""
    path = Path(file_path).resolve()
    
    # Check if file exists
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check if it's a file (not directory)
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    # Check file size
    file_size = path.stat().st_size
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {file_size} bytes (max: {MAX_FILE_SIZE})")
    
    return path


def parse_players_csv(file_path: str) -> List[Player]:
    """
    Parse players from CSV file
    
    Supports multiple formats:
    1. English format: id, name, age, position, skills (JSON), salary, tsi, form, stamina, experience, leadership
    2. Portuguese format from Hattrick export (main team) with columns:
       Nacionalidade, Número da camisa, Nome, ID do jogador, ..., Idade, ..., TSI, Salário, ..., 
       Experiência, Liderança, ..., Forma, Resistência, Goleiro, Defesa, Armação, Ala, Finalização, Bola Parada, ...
    3. Portuguese format from Hattrick export (youth team) with columns:
       Nacionalidade, Número da camisa, Nome, ID do jogador, ..., Idade, ..., Dias até poder promover, ...
       Goleiro, Goleiro, Defesa, Defesa, Armação, Armação, Ala, Ala, Finalização, Finalização, Bola Parada, Bola Parada, ...
    """
    # Validate file path
    validated_path = _validate_file_path(file_path)
    players = []
    
    try:
        # Check if this is youth format by reading first line
        with open(validated_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            is_youth_format = 'Dias até poder promover' in first_line
        
        # Reopen file for reading
        with open(validated_path, 'r', encoding='utf-8') as f:
            if is_youth_format:
                # For youth format, we need to handle duplicate column names
                reader = csv.reader(f)
                header = next(reader)
                
                # Find indices of important columns
                col_indices = {}
                for i, col in enumerate(header):
                    if col == 'ID do jogador':
                        col_indices['id'] = i
                    elif col == 'Nome':
                        col_indices['name'] = i
                    elif col == 'Idade':
                        col_indices['age'] = i
                    elif col == 'Posição na última partida':
                        col_indices['position'] = i
                    elif col == 'Goleiro' and 'goalkeeping' not in col_indices:
                        col_indices['goalkeeping'] = i  # First occurrence (current value)
                    elif col == 'Defesa' and 'defending' not in col_indices:
                        col_indices['defending'] = i
                    elif col == 'Armação' and 'playmaking' not in col_indices:
                        col_indices['playmaking'] = i
                    elif col == 'Ala' and 'winger' not in col_indices:
                        col_indices['winger'] = i
                    elif col == 'Finalização' and 'scoring' not in col_indices:
                        col_indices['scoring'] = i
                    elif col == 'Bola Parada' and 'set_pieces' not in col_indices:
                        col_indices['set_pieces'] = i
                
                for row in reader:
                    try:
                        player = _parse_youth_portuguese_format_by_index(row, col_indices)
                        if player:
                            players.append(player)
                    except Exception as e:
                        id_idx = col_indices.get('id', 0)
                        player_id = row[id_idx] if id_idx < len(row) else 'unknown'
                        print(f"Error parsing player {player_id}: {e}")
                        continue
            else:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # Check if this is Portuguese format (has 'ID do jogador' column)
                        if 'ID do jogador' in row:
                            player = _parse_portuguese_format(row)
                        else:
                            # English format
                            player = _parse_english_format(row)
                        
                        if player:
                            players.append(player)
                    except Exception as e:
                        player_id = row.get('ID do jogador') or row.get('id', 'unknown')
                        print(f"Error parsing player {player_id}: {e}")
                        continue
    except (FileNotFoundError, ValueError) as e:
        raise
    except Exception as e:
        raise RuntimeError(f"Error reading file {file_path}: {e}") from e
    
    return players


def _validate_player_data(age: int, form: int, stamina: int, experience: int, leadership: int) -> None:
    """Validate player data ranges"""
    if age < 15 or age > 50:
        raise ValueError(f"Invalid age: {age} (must be between 15 and 50)")
    if form < 1 or form > 8:
        raise ValueError(f"Invalid form: {form} (must be between 1 and 8)")
    if stamina < 0 or stamina > 100:
        raise ValueError(f"Invalid stamina: {stamina} (must be between 0 and 100)")
    if experience < 0 or experience > 20:
        raise ValueError(f"Invalid experience: {experience} (must be between 0 and 20)")
    if leadership < 0 or leadership > 20:
        raise ValueError(f"Invalid leadership: {leadership} (must be between 0 and 20)")


def _parse_portuguese_format(row: Dict) -> Optional[Player]:
    """Parse player from Portuguese CSV format"""
    import json
    
    # Map columns
    player_id = str(row.get('ID do jogador', ''))
    name = row.get('Nome', '')
    
    # Validate and convert age
    try:
        age = int(row.get('Idade', 0))
    except (ValueError, TypeError):
        age = 0
    
    # Convert position
    pos_code = row.get('Posição na última partida', 'MC')
    position_key = POSITION_MAP.get(pos_code, 'IM')
    position = Position[position_key]
    
    # Build skills dictionary
    skills = {
        'goalkeeping': int(row.get('Goleiro', 0)),
        'defending': int(row.get('Defesa', 0)),
        'playmaking': int(row.get('Armação', 0)),
        'winger': int(row.get('Ala', 0)),
        'scoring': int(row.get('Finalização', 0)),
        'set_pieces': int(row.get('Bola Parada', 0)),
    }
    
    # Get other attributes with validation
    try:
        salary = float(row.get('Salário', 0))
        tsi = int(row.get('TSI', 0))
        form = int(row.get('Forma', 5))
        stamina = int(row.get('Resistência', 0))
        experience = int(row.get('Experiência', 0))
        leadership = int(row.get('Liderança', 0))
    except (ValueError, TypeError):
        # Use defaults if conversion fails
        salary = 0.0
        tsi = 0
        form = 5
        stamina = 0
        experience = 0
        leadership = 0
    
    # Validate data ranges
    try:
        _validate_player_data(age, form, stamina, experience, leadership)
    except ValueError:
        # If validation fails, use safe defaults
        form = 5
        stamina = 0
        experience = 0
        leadership = 0
    
    return Player(
        id=player_id,
        name=name,
        age=age,
        position=position,
        skills=skills,
        salary=salary,
        tsi=tsi,
        form=form,
        stamina=stamina,
        experience=experience,
        leadership=leadership
    )


def _parse_youth_portuguese_format_by_index(row: List[str], col_indices: Dict[str, int]) -> Optional[Player]:
    """Parse youth player from Portuguese CSV format using column indices"""
    def parse_skill_value(value: str) -> int:
        """Parse skill value that can be '?', '/?', '3/4', or just a number"""
        if not value or value.strip() == '' or value == '?' or value == '/?':
            return 0
        # Handle format like "3/4" (current/potential) - take current value
        if '/' in str(value):
            parts = str(value).split('/')
            if parts[0] and parts[0] != '?':
                try:
                    return int(parts[0])
                except:
                    return 0
        try:
            return int(value)
        except:
            return 0
    
    def safe_get(index: int, default: str = '') -> str:
        """Safely get value from row by index"""
        if index < len(row):
            return row[index] or default
        return default
    
    # Get values by index with safety checks
    id_idx = col_indices.get('id', 3)
    name_idx = col_indices.get('name', 2)
    age_idx = col_indices.get('age', 7)
    pos_idx = col_indices.get('position', -1)
    
    player_id = str(safe_get(id_idx, ''))
    name = safe_get(name_idx, '')
    
    if not player_id or not name:
        return None
    
    try:
        age = int(safe_get(age_idx, '0'))
    except:
        age = 0
    
    # Convert position
    pos_code = safe_get(pos_idx, 'MC')
    position_key = POSITION_MAP.get(pos_code, 'IM')
    position = Position[position_key]
    
    # Get skill values by index (first occurrence = current value)
    skills = {
        'goalkeeping': parse_skill_value(safe_get(col_indices.get('goalkeeping', 12), '0')),
        'defending': parse_skill_value(safe_get(col_indices.get('defending', 14), '0')),
        'playmaking': parse_skill_value(safe_get(col_indices.get('playmaking', 16), '0')),
        'winger': parse_skill_value(safe_get(col_indices.get('winger', 18), '0')),
        'scoring': parse_skill_value(safe_get(col_indices.get('scoring', 22), '0')),
        'set_pieces': parse_skill_value(safe_get(col_indices.get('set_pieces', 24), '0')),
    }
    
    # Youth players don't have salary, TSI, form, etc. - set defaults
    return Player(
        id=player_id,
        name=name,
        age=age,
        position=position,
        skills=skills,
        salary=0.0,  # Youth players don't have salary
        tsi=0,  # Youth players don't have TSI
        form=5,  # Default form
        stamina=0,  # Youth players don't have stamina
        experience=0,  # Youth players don't have experience
        leadership=0  # Youth players don't have leadership
    )


# Removed unused function _parse_youth_portuguese_format - using _parse_youth_portuguese_format_by_index instead


def _parse_english_format(row: Dict) -> Optional[Player]:
    """Parse player from English CSV format"""
    import json
    
    # Safely parse JSON skills with size limit
    skills_str = row.get('skills', '{}')
    if len(skills_str) > MAX_JSON_SIZE:
        raise ValueError(f"Skills JSON too large: {len(skills_str)} bytes")
    
    try:
        skills = json.loads(skills_str)
        if not isinstance(skills, dict):
            skills = {}
    except (json.JSONDecodeError, TypeError):
        skills = {}
    
    # Validate and convert with error handling
    try:
        age = int(row.get('age', 0))
        salary = float(row.get('salary', 0))
        tsi = int(row.get('tsi', 0))
        form = int(row.get('form', 5))
        stamina = int(row.get('stamina', 0))
        experience = int(row.get('experience', 0))
        leadership = int(row.get('leadership', 0))
    except (ValueError, TypeError, KeyError):
        raise ValueError(f"Invalid player data for ID: {row.get('id', 'unknown')}")
    
    # Validate data ranges
    _validate_player_data(age, form, stamina, experience, leadership)
    
    # Validate position
    position_key = row.get('position', 'IM')
    if position_key not in [p.name for p in Position]:
        position_key = 'IM'
    
    return Player(
        id=str(row.get('id', '')),
        name=str(row.get('name', '')),
        age=age,
        position=Position[position_key],
        skills=skills,
        salary=salary,
        tsi=tsi,
        form=form,
        stamina=stamina,
        experience=experience,
        leadership=leadership
    )


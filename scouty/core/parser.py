"""
Data parsing utilities for CSV, HTML, and other formats
"""

import csv
from typing import List, Dict
from pathlib import Path
from .player import Player, Position


def parse_players_csv(file_path: str) -> List[Player]:
    """
    Parse players from CSV file
    Expected CSV format: id, name, age, position, skills (JSON), salary, tsi, form, stamina, experience, leadership
    """
    players = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                import json
                skills = json.loads(row.get('skills', '{}'))
                
                player = Player(
                    id=row['id'],
                    name=row['name'],
                    age=int(row['age']),
                    position=Position[row.get('position', 'IM')],
                    skills=skills,
                    salary=float(row.get('salary', 0)),
                    tsi=int(row.get('tsi', 0)),
                    form=int(row.get('form', 5)),
                    stamina=int(row.get('stamina', 0)),
                    experience=int(row.get('experience', 0)),
                    leadership=int(row.get('leadership', 0))
                )
                players.append(player)
            except Exception as e:
                print(f"Error parsing player {row.get('id', 'unknown')}: {e}")
                continue
    
    return players


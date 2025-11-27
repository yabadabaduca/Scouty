"""
Core player data models and utilities
"""

from dataclasses import dataclass
from typing import Optional, Dict, List
from enum import Enum


class Position(Enum):
    """Player positions in Hattrick"""
    GK = "Goalkeeper"
    CD = "Central Defender"
    WB = "Wing Back"
    IM = "Inner Midfielder"
    WI = "Winger"
    FW = "Forward"


@dataclass
class Player:
    """Player data model"""
    id: str
    name: str
    age: int
    position: Position
    skills: Dict[str, int]  # e.g., {"defending": 15, "playmaking": 12}
    salary: float
    tsi: int  # Total Skill Index
    form: int
    stamina: int
    experience: int
    leadership: int
    
    def get_best_position(self) -> Position:
        """Calculate best position based on skills"""
        # Simplified logic - can be enhanced
        if self.skills.get("goalkeeping", 0) > 10:
            return Position.GK
        
        defending = self.skills.get("defending", 0)
        playmaking = self.skills.get("playmaking", 0)
        winger = self.skills.get("winger", 0)
        scoring = self.skills.get("scoring", 0)
        
        if scoring > max(defending, playmaking, winger):
            return Position.FW
        elif defending > max(playmaking, winger):
            return Position.CD
        elif winger > playmaking:
            return Position.WI
        else:
            return Position.IM
    
    def calculate_cost_benefit(self) -> float:
        """Calculate cost-benefit ratio (TSI / salary)"""
        if self.salary == 0:
            return 0.0
        return self.tsi / self.salary
    
    def estimate_potential(self) -> str:
        """Estimate player potential based on age and skills"""
        if self.age < 20:
            return "High"
        elif self.age < 25:
            return "Medium"
        else:
            return "Low"


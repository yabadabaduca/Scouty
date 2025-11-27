"""
Team Snapshot Module
Full overview of squad strengths, weaknesses and tactical recommendations.
"""

from typing import List, Dict
from scouty.core.player import Player
from collections import defaultdict


class TeamSnapshot:
    """Generate team overview and analysis"""
    
    def __init__(self, players: List[Player]):
        self.players = players
    
    def generate_snapshot(self) -> Dict:
        """Generate complete team snapshot"""
        return {
            "total_players": len(self.players),
            "average_age": self._calculate_average_age(),
            "total_salary": self._calculate_total_salary(),
            "total_tsi": self._calculate_total_tsi(),
            "position_distribution": self._analyze_positions(),
            "strengths": self._identify_strengths(),
            "weaknesses": self._identify_weaknesses(),
            "tactical_recommendations": self._tactical_recommendations(),
            "best_lineup": self._suggest_best_lineup()
        }
    
    def _calculate_average_age(self) -> float:
        """Calculate average team age"""
        if not self.players:
            return 0.0
        return sum(p.age for p in self.players) / len(self.players)
    
    def _calculate_total_salary(self) -> float:
        """Calculate total team salary"""
        return sum(p.salary for p in self.players)
    
    def _calculate_total_tsi(self) -> int:
        """Calculate total TSI"""
        return sum(p.tsi for p in self.players)
    
    def _analyze_positions(self) -> Dict:
        """Analyze position distribution"""
        position_count = defaultdict(int)
        for player in self.players:
            position_count[player.position.value] += 1
        
        return dict(position_count)
    
    def _identify_strengths(self) -> List[str]:
        """Identify team strengths"""
        strengths = []
        
        # Analyze average skills by position
        avg_skills = self._calculate_average_skills()
        
        if avg_skills.get("defending", 0) > 12:
            strengths.append("Strong defense")
        if avg_skills.get("playmaking", 0) > 12:
            strengths.append("Good midfield control")
        if avg_skills.get("scoring", 0) > 12:
            strengths.append("Strong attack")
        
        if self._calculate_average_age() < 24:
            strengths.append("Young squad with potential")
        
        return strengths if strengths else ["Balanced team"]
    
    def _identify_weaknesses(self) -> List[str]:
        """Identify team weaknesses"""
        weaknesses = []
        
        avg_skills = self._calculate_average_skills()
        position_dist = self._analyze_positions()
        
        if avg_skills.get("defending", 0) < 10:
            weaknesses.append("Weak defense")
        if avg_skills.get("playmaking", 0) < 10:
            weaknesses.append("Weak midfield")
        if avg_skills.get("scoring", 0) < 10:
            weaknesses.append("Weak attack")
        
        if position_dist.get("Goalkeeper", 0) == 0:
            weaknesses.append("Missing goalkeeper")
        
        return weaknesses
    
    def _calculate_average_skills(self) -> Dict[str, float]:
        """Calculate average skills across all players"""
        skill_sums = defaultdict(float)
        skill_counts = defaultdict(int)
        
        for player in self.players:
            for skill, value in player.skills.items():
                skill_sums[skill] += value
                skill_counts[skill] += 1
        
        return {
            skill: skill_sums[skill] / skill_counts[skill] 
            for skill in skill_sums.keys()
        }
    
    def _tactical_recommendations(self) -> List[str]:
        """Generate tactical recommendations"""
        recommendations = []
        weaknesses = self._identify_weaknesses()
        
        if "Weak defense" in weaknesses:
            recommendations.append("Consider training defending or buying defenders")
        if "Weak midfield" in weaknesses:
            recommendations.append("Focus on playmaking training")
        if "Weak attack" in weaknesses:
            recommendations.append("Train scoring or invest in forwards")
        
        if not weaknesses:
            recommendations.append("Team is well balanced - focus on maintaining form")
        
        return recommendations
    
    def _suggest_best_lineup(self) -> Dict:
        """Suggest best possible lineup"""
        # Simplified lineup suggestion
        # In a full implementation, this would use more sophisticated algorithms
        
        gk = [p for p in self.players if p.position.value == "Goalkeeper"]
        defenders = [p for p in self.players if "Defender" in p.position.value]
        midfielders = [p for p in self.players if "Midfielder" in p.position.value]
        forwards = [p for p in self.players if p.position.value == "Forward"]
        
        # Sort by TSI (simplified - could use more complex metrics)
        gk.sort(key=lambda x: x.tsi, reverse=True)
        defenders.sort(key=lambda x: x.tsi, reverse=True)
        midfielders.sort(key=lambda x: x.tsi, reverse=True)
        forwards.sort(key=lambda x: x.tsi, reverse=True)
        
        return {
            "goalkeeper": gk[0].name if gk else "None",
            "defenders": [d.name for d in defenders[:4]],
            "midfielders": [m.name for m in midfielders[:4]],
            "forwards": [f.name for f in forwards[:2]]
        }


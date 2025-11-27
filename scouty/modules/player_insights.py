"""
Player Insight Extractor Module
Evaluates skills, roles, cost-benefit, potential and training impact.
"""

from typing import List, Dict
from scouty.core.player import Player


class PlayerInsights:
    """Extract insights from player data"""
    
    def __init__(self, players: List[Player]):
        self.players = players
    
    def analyze_player(self, player: Player) -> Dict:
        """Analyze a single player and return insights"""
        best_position = player.get_best_position()
        cost_benefit = player.calculate_cost_benefit()
        potential = player.estimate_potential()
        
        # Calculate training impact estimate
        training_impact = self._estimate_training_impact(player)
        
        # Decision recommendation
        decision = self._recommend_decision(player, cost_benefit, potential)
        
        return {
            "player_id": player.id,
            "name": player.name,
            "age": player.age,
            "best_position": best_position.value,
            "current_position": player.position.value,
            "cost_benefit": round(cost_benefit, 2),
            "potential": potential,
            "training_impact": training_impact,
            "recommendation": decision,
            "tsi": player.tsi,
            "salary": player.salary
        }
    
    def analyze_all(self) -> List[Dict]:
        """Analyze all players"""
        return [self.analyze_player(p) for p in self.players]
    
    def _estimate_training_impact(self, player: Player) -> Dict:
        """Estimate training impact based on age and current skills"""
        if player.age < 20:
            time_to_improve = "1-2 weeks"
            impact = "High"
        elif player.age < 25:
            time_to_improve = "2-4 weeks"
            impact = "Medium"
        else:
            time_to_improve = "4+ weeks"
            impact = "Low"
        
        return {
            "time_to_improve": time_to_improve,
            "impact": impact
        }
    
    def _recommend_decision(self, player: Player, cost_benefit: float, potential: str) -> str:
        """Recommend action: keep, train, or sell"""
        if player.age > 30 and cost_benefit < 100:
            return "Sell"
        elif potential == "High" and player.age < 22:
            return "Train"
        elif cost_benefit > 200:
            return "Keep"
        elif potential == "Low" and cost_benefit < 150:
            return "Sell"
        else:
            return "Keep"


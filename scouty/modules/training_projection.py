"""
Training Projection Module
Estimate skill-ups, time to improve, financial ROI and impact of switching training types.
"""

from typing import List, Dict, Optional
from scouty.core.player import Player


class TrainingProjection:
    """Project training outcomes and ROI"""
    
    def __init__(self, players: List[Player], current_training: str = "playmaking"):
        self.players = players
        self.current_training = current_training
    
    def project_skill_ups(self, weeks: int = 4) -> List[Dict]:
        """Project skill improvements for next N weeks"""
        projections = []
        
        for player in self.players:
            projection = self._project_player_skill_up(player, weeks)
            projections.append({
                "player_id": player.id,
                "name": player.name,
                "current_skill": self._get_current_training_skill(player),
                "projected_skill": projection["projected_skill"],
                "weeks_to_improve": projection["weeks_to_improve"],
                "estimated_value_increase": projection["value_increase"]
            })
        
        return projections
    
    def compare_training_types(self) -> Dict:
        """Compare different training types and their ROI"""
        training_types = ["playmaking", "defending", "scoring", "winger", "goalkeeping"]
        results = {}
        
        for training_type in training_types:
            affected_players = self._get_players_affected_by_training(training_type)
            roi = self._calculate_training_roi(affected_players, training_type)
            
            results[training_type] = {
                "affected_players": len(affected_players),
                "estimated_roi": roi,
                "weeks_to_first_skillup": self._estimate_weeks_to_skillup(affected_players)
            }
        
        # Recommend best training
        best_training = max(results.items(), key=lambda x: x[1]["estimated_roi"])
        results["recommendation"] = {
            "best_training": best_training[0],
            "reason": f"Highest ROI: {best_training[1]['estimated_roi']:.2f}"
        }
        
        return results
    
    def find_players_near_skillup(self) -> List[Dict]:
        """Find players close to skill improvement"""
        near_skillup = []
        
        for player in self.players:
            skill = self._get_current_training_skill(player)
            if skill is None:
                continue
            
            # Simplified logic: estimate based on age and current skill
            weeks_remaining = self._estimate_weeks_to_skillup([player])
            
            if weeks_remaining <= 2:
                near_skillup.append({
                    "player_id": player.id,
                    "name": player.name,
                    "current_skill": skill,
                    "weeks_to_skillup": weeks_remaining,
                    "estimated_value_increase": self._estimate_value_increase(player, skill)
                })
        
        return sorted(near_skillup, key=lambda x: x["weeks_to_skillup"])
    
    def _project_player_skill_up(self, player: Player, weeks: int) -> Dict:
        """Project skill improvement for a player"""
        current_skill = self._get_current_training_skill(player)
        if current_skill is None:
            return {
                "projected_skill": current_skill,
                "weeks_to_improve": None,
                "value_increase": 0
            }
        
        # Simplified projection based on age
        if player.age < 20:
            skillup_rate = 0.5  # weeks per skill point
        elif player.age < 25:
            skillup_rate = 1.0
        else:
            skillup_rate = 2.0
        
        weeks_to_improve = int(skillup_rate)
        projected_skill = current_skill + (weeks // int(skillup_rate))
        value_increase = self._estimate_value_increase(player, projected_skill)
        
        return {
            "projected_skill": projected_skill,
            "weeks_to_improve": weeks_to_improve,
            "value_increase": value_increase
        }
    
    def _get_current_training_skill(self, player: Player) -> Optional[int]:
        """Get the skill being trained for this player"""
        if self.current_training == "playmaking":
            return player.skills.get("playmaking")
        elif self.current_training == "defending":
            return player.skills.get("defending")
        elif self.current_training == "scoring":
            return player.skills.get("scoring")
        elif self.current_training == "winger":
            return player.skills.get("winger")
        elif self.current_training == "goalkeeping":
            return player.skills.get("goalkeeping")
        return None
    
    def _get_players_affected_by_training(self, training_type: str) -> List[Player]:
        """Get players that would benefit from this training type"""
        # Simplified: return all players (in reality, depends on position and formation)
        return self.players
    
    def _calculate_training_roi(self, players: List[Player], training_type: str) -> float:
        """Calculate ROI for a training type"""
        if not players:
            return 0.0
        
        total_value_increase = sum(
            self._estimate_value_increase(p, self._get_current_training_skill(p) or 0)
            for p in players
        )
        
        # Simplified ROI calculation
        return total_value_increase / len(players) if players else 0.0
    
    def _estimate_weeks_to_skillup(self, players: List[Player]) -> int:
        """Estimate weeks until next skillup"""
        if not players:
            return 999
        
        # Average based on age
        avg_age = sum(p.age for p in players) / len(players)
        if avg_age < 20:
            return 1
        elif avg_age < 25:
            return 2
        else:
            return 4
    
    def _estimate_value_increase(self, player: Player, new_skill: int) -> float:
        """Estimate value increase after skillup"""
        # Simplified: TSI typically increases with skill
        # Rough estimate: 10-20% TSI increase per skill point
        current_tsi = player.tsi
        skill_increase = new_skill - (self._get_current_training_skill(player) or 0)
        estimated_tsi_increase = current_tsi * 0.15 * skill_increase
        
        # Convert to approximate market value (simplified)
        return estimated_tsi_increase * 0.1  # Rough conversion factor


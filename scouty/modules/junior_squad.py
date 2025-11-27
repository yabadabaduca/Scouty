"""
Junior Squad Analysis Module
Predict potential, decide who to promote, train or release.
"""

from typing import List, Dict
from scouty.core.player import Player


class JuniorSquadAnalyzer:
    """Analyze junior squad and provide recommendations"""
    
    def __init__(self, juniors: List[Player]):
        self.juniors = juniors
    
    def analyze_potential(self) -> List[Dict]:
        """Analyze potential of all juniors"""
        analysis = []
        
        for junior in self.juniors:
            potential_score = self._calculate_potential_score(junior)
            recommendation = self._recommend_action(junior, potential_score)
            
            analysis.append({
                "player_id": junior.id,
                "name": junior.name,
                "age": junior.age,
                "potential_score": potential_score,
                "best_position": junior.get_best_position().value,
                "current_skills": junior.skills,
                "recommendation": recommendation,
                "estimated_promotion_value": self._estimate_promotion_value(junior)
            })
        
        return sorted(analysis, key=lambda x: x["potential_score"], reverse=True)
    
    def recommend_promotions(self, max_promotions: int = 3) -> List[Dict]:
        """Recommend which juniors to promote"""
        analysis = self.analyze_potential()
        
        # Filter for promotion candidates
        promotion_candidates = [
            a for a in analysis 
            if a["recommendation"] in ["Promote", "Promote and Train"]
        ]
        
        return promotion_candidates[:max_promotions]
    
    def simulate_training_impact(self, training_type: str, weeks: int = 4) -> Dict:
        """Simulate impact of training juniors"""
        results = {
            "training_type": training_type,
            "weeks": weeks,
            "projections": []
        }
        
        for junior in self.juniors:
            current_skill = junior.skills.get(training_type, 0)
            projected_skill = self._project_junior_skill(junior, training_type, weeks)
            
            results["projections"].append({
                "player_id": junior.id,
                "name": junior.name,
                "current_skill": current_skill,
                "projected_skill": projected_skill,
                "improvement": projected_skill - current_skill
            })
        
        return results
    
    def compare_formations(self) -> Dict:
        """Compare different formation options for juniors"""
        formations = {
            "4-4-2": {"defenders": 4, "midfielders": 4, "forwards": 2},
            "3-5-2": {"defenders": 3, "midfielders": 5, "forwards": 2},
            "4-3-3": {"defenders": 4, "midfielders": 3, "forwards": 3},
            "5-3-2": {"defenders": 5, "midfielders": 3, "forwards": 2}
        }
        
        comparison = {}
        
        for formation_name, positions in formations.items():
            suitability = self._evaluate_formation_suitability(positions)
            comparison[formation_name] = {
                "suitability_score": suitability,
                "can_field": self._can_field_formation(positions)
            }
        
        # Recommend best formation
        best_formation = max(comparison.items(), key=lambda x: x[1]["suitability_score"])
        comparison["recommendation"] = best_formation[0]
        
        return comparison
    
    def _calculate_potential_score(self, junior: Player) -> float:
        """Calculate potential score (0-100)"""
        score = 0.0
        
        # Age factor (younger = better)
        if junior.age < 17:
            score += 30
        elif junior.age < 18:
            score += 20
        elif junior.age < 19:
            score += 10
        
        # Skill factor
        max_skill = max(junior.skills.values()) if junior.skills else 0
        score += min(max_skill * 5, 40)
        
        # TSI factor
        if junior.tsi > 1000:
            score += 20
        elif junior.tsi > 500:
            score += 10
        
        # Form factor
        score += junior.form * 2
        
        return min(score, 100.0)
    
    def _recommend_action(self, junior: Player, potential_score: float) -> str:
        """Recommend action: Promote, Train, or Release"""
        if potential_score >= 70:
            return "Promote and Train"
        elif potential_score >= 50:
            return "Promote"
        elif potential_score >= 30:
            return "Train"
        else:
            return "Release"
    
    def _estimate_promotion_value(self, junior: Player) -> float:
        """Estimate value when promoted to main team"""
        # Simplified: estimate based on current TSI and potential
        potential_score = self._calculate_potential_score(junior)
        base_value = junior.tsi * 10  # Rough conversion
        
        if potential_score > 70:
            multiplier = 2.0
        elif potential_score > 50:
            multiplier = 1.5
        else:
            multiplier = 1.0
        
        return base_value * multiplier
    
    def _project_junior_skill(self, junior: Player, training_type: str, weeks: int) -> int:
        """Project skill after training"""
        current_skill = junior.skills.get(training_type, 0)
        
        # Juniors train faster
        skillup_rate = 0.5  # weeks per skill point for juniors
        projected_improvement = int(weeks / skillup_rate)
        
        return current_skill + projected_improvement
    
    def _evaluate_formation_suitability(self, positions: Dict) -> float:
        """Evaluate how well current juniors fit a formation"""
        defenders = [j for j in self.juniors if "Defender" in j.position.value]
        midfielders = [j for j in self.juniors if "Midfielder" in j.position.value]
        forwards = [j for j in self.juniors if j.position.value == "Forward"]
        
        score = 0.0
        
        # Check if we have enough players for each position
        if len(defenders) >= positions["defenders"]:
            score += 30
        if len(midfielders) >= positions["midfielders"]:
            score += 30
        if len(forwards) >= positions["forwards"]:
            score += 30
        
        # Quality factor
        if defenders:
            avg_def_skill = sum(d.skills.get("defending", 0) for d in defenders) / len(defenders)
            score += min(avg_def_skill * 2, 10)
        
        return score
    
    def _can_field_formation(self, positions: Dict) -> bool:
        """Check if we can field this formation"""
        defenders = [j for j in self.juniors if "Defender" in j.position.value]
        midfielders = [j for j in self.juniors if "Midfielder" in j.position.value]
        forwards = [j for j in self.juniors if j.position.value == "Forward"]
        
        return (
            len(defenders) >= positions["defenders"] and
            len(midfielders) >= positions["midfielders"] and
            len(forwards) >= positions["forwards"]
        )


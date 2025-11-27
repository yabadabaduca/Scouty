"""
Match Analyzer Lite Module
Extract patterns from past games and adapt tactical approach.
"""

from typing import List, Dict, Optional


class MatchAnalyzer:
    """Analyze match patterns and provide tactical insights"""
    
    def __init__(self, matches: List[Dict]):
        """
        Initialize with match data
        Expected match format: {
            "date": str,
            "opponent": str,
            "result": str,  # e.g., "3-1"
            "possession": float,
            "chances": int,
            "tactics": str,
            "formation": str
        }
        """
        self.matches = matches
    
    def extract_patterns(self) -> Dict:
        """Extract key patterns from match history"""
        if not self.matches:
            return {"error": "No matches to analyze"}
        
        return {
            "possession_analysis": self._analyze_possession(),
            "attack_patterns": self._analyze_attack(),
            "defense_patterns": self._analyze_defense(),
            "tactical_recommendations": self._generate_tactical_recommendations(),
            "weak_points": self._identify_weak_points()
        }
    
    def analyze_recent_form(self, last_n: int = 5) -> Dict:
        """Analyze recent form (last N matches)"""
        recent_matches = self.matches[:last_n] if len(self.matches) >= last_n else self.matches
        
        wins = sum(1 for m in recent_matches if self._is_win(m.get("result", "")))
        draws = sum(1 for m in recent_matches if self._is_draw(m.get("result", "")))
        losses = sum(1 for m in recent_matches if self._is_loss(m.get("result", "")))
        
        avg_possession = sum(m.get("possession", 50) for m in recent_matches) / len(recent_matches) if recent_matches else 50
        avg_chances = sum(m.get("chances", 0) for m in recent_matches) / len(recent_matches) if recent_matches else 0
        
        return {
            "matches_analyzed": len(recent_matches),
            "wins": wins,
            "draws": draws,
            "losses": losses,
            "win_rate": (wins / len(recent_matches) * 100) if recent_matches else 0,
            "average_possession": round(avg_possession, 1),
            "average_chances": round(avg_chances, 1),
            "form_trend": self._calculate_form_trend(recent_matches)
        }
    
    def suggest_tactical_changes(self) -> List[str]:
        """Suggest tactical changes based on patterns"""
        patterns = self.extract_patterns()
        suggestions = []
        
        possession_analysis = patterns.get("possession_analysis", {})
        if possession_analysis.get("average") < 45:
            suggestions.append("Low possession - consider training playmaking or changing formation")
        
        attack_patterns = patterns.get("attack_patterns", {})
        if attack_patterns.get("average_chances") < 3:
            suggestions.append("Low chance creation - focus on attacking training or winger development")
        
        defense_patterns = patterns.get("defense_patterns", {})
        if defense_patterns.get("goals_conceded_avg") > 2:
            suggestions.append("High goals conceded - strengthen defense or train defending")
        
        if not suggestions:
            suggestions.append("Team performing well - maintain current tactics")
        
        return suggestions
    
    def _analyze_possession(self) -> Dict:
        """Analyze possession patterns"""
        possessions = [m.get("possession", 50) for m in self.matches if m.get("possession")]
        
        if not possessions:
            return {"average": 50, "trend": "stable"}
        
        avg_possession = sum(possessions) / len(possessions)
        
        # Calculate trend
        recent_avg = sum(possessions[:5]) / min(5, len(possessions)) if possessions else avg_possession
        older_avg = sum(possessions[5:]) / max(1, len(possessions) - 5) if len(possessions) > 5 else avg_possession
        
        if recent_avg > older_avg + 5:
            trend = "improving"
        elif recent_avg < older_avg - 5:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "average": round(avg_possession, 1),
            "trend": trend,
            "recommendation": "Train playmaking" if avg_possession < 45 else "Maintain"
        }
    
    def _analyze_attack(self) -> Dict:
        """Analyze attacking patterns"""
        chances = [m.get("chances", 0) for m in self.matches if m.get("chances")]
        goals_scored = [self._get_goals_scored(m.get("result", "")) for m in self.matches]
        
        return {
            "average_chances": round(sum(chances) / len(chances), 1) if chances else 0,
            "average_goals": round(sum(goals_scored) / len(goals_scored), 1) if goals_scored else 0,
            "conversion_rate": self._calculate_conversion_rate(chances, goals_scored)
        }
    
    def _analyze_defense(self) -> Dict:
        """Analyze defensive patterns"""
        goals_conceded = [self._get_goals_conceded(m.get("result", "")) for m in self.matches]
        
        return {
            "goals_conceded_avg": round(sum(goals_conceded) / len(goals_conceded), 1) if goals_conceded else 0,
            "clean_sheets": sum(1 for gc in goals_conceded if gc == 0),
            "defensive_strength": "Strong" if sum(goals_conceded) / len(goals_conceded) < 1.0 else "Weak"
        }
    
    def _generate_tactical_recommendations(self) -> List[str]:
        """Generate tactical recommendations"""
        recommendations = []
        patterns = self.extract_patterns()
        
        possession = patterns.get("possession_analysis", {}).get("average", 50)
        if possession < 45:
            recommendations.append("Low possession - consider 3-5-2 or 4-5-1 formation")
        
        attack = patterns.get("attack_patterns", {})
        if attack.get("average_chances", 0) < 3:
            recommendations.append("Low chance creation - try counter-attack or focus on wingers")
        
        defense = patterns.get("defense_patterns", {})
        if defense.get("goals_conceded_avg", 0) > 2:
            recommendations.append("Weak defense - consider 5-3-2 or train defending")
        
        return recommendations if recommendations else ["Current tactics are working well"]
    
    def _identify_weak_points(self) -> List[str]:
        """Identify team weak points"""
        weak_points = []
        patterns = self.extract_patterns()
        
        if patterns.get("possession_analysis", {}).get("average", 50) < 45:
            weak_points.append("Midfield control")
        
        if patterns.get("attack_patterns", {}).get("average_chances", 0) < 3:
            weak_points.append("Attack creation")
        
        if patterns.get("defense_patterns", {}).get("goals_conceded_avg", 0) > 2:
            weak_points.append("Defense")
        
        return weak_points if weak_points else ["No major weak points identified"]
    
    def _is_win(self, result: str) -> bool:
        """Check if result is a win"""
        try:
            home, away = result.split("-")
            return int(home) > int(away)
        except:
            return False
    
    def _is_draw(self, result: str) -> bool:
        """Check if result is a draw"""
        try:
            home, away = result.split("-")
            return int(home) == int(away)
        except:
            return False
    
    def _is_loss(self, result: str) -> bool:
        """Check if result is a loss"""
        try:
            home, away = result.split("-")
            return int(home) < int(away)
        except:
            return False
    
    def _get_goals_scored(self, result: str) -> int:
        """Extract goals scored from result"""
        try:
            home, _ = result.split("-")
            return int(home)
        except:
            return 0
    
    def _get_goals_conceded(self, result: str) -> int:
        """Extract goals conceded from result"""
        try:
            _, away = result.split("-")
            return int(away)
        except:
            return 0
    
    def _calculate_conversion_rate(self, chances: List[int], goals: List[int]) -> float:
        """Calculate chance conversion rate"""
        if not chances or sum(chances) == 0:
            return 0.0
        return round((sum(goals) / sum(chances)) * 100, 1)
    
    def _calculate_form_trend(self, matches: List[Dict]) -> str:
        """Calculate form trend"""
        if len(matches) < 2:
            return "insufficient_data"
        
        recent_results = [self._get_match_points(m.get("result", "")) for m in matches[:3]]
        older_results = [self._get_match_points(m.get("result", "")) for m in matches[3:6]] if len(matches) > 3 else []
        
        if not older_results:
            return "stable"
        
        recent_avg = sum(recent_results) / len(recent_results)
        older_avg = sum(older_results) / len(older_results)
        
        if recent_avg > older_avg + 0.5:
            return "improving"
        elif recent_avg < older_avg - 0.5:
            return "declining"
        else:
            return "stable"
    
    def _get_match_points(self, result: str) -> float:
        """Get points from match result (3 for win, 1 for draw, 0 for loss)"""
        if self._is_win(result):
            return 3.0
        elif self._is_draw(result):
            return 1.0
        else:
            return 0.0


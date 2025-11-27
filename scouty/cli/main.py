"""
Scouty CLI - Command-line interface
"""

import argparse
import json
import sys
from pathlib import Path

from scouty.core.parser import parse_players_csv
from scouty.modules.player_insights import PlayerInsights
from scouty.modules.team_snapshot import TeamSnapshot
from scouty.modules.training_projection import TrainingProjection
from scouty.modules.junior_squad import JuniorSquadAnalyzer
from scouty.modules.match_analyzer import MatchAnalyzer


def analyze_players(args):
    """Analyze players from CSV file"""
    try:
        players = parse_players_csv(args.file)
        insights = PlayerInsights(players)
        results = insights.analyze_all()
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Results saved to {args.output}")
        else:
            print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def team_snapshot(args):
    """Generate team snapshot"""
    try:
        players = parse_players_csv(args.file)
        snapshot = TeamSnapshot(players)
        results = snapshot.generate_snapshot()
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Snapshot saved to {args.output}")
        else:
            print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def training_projection(args):
    """Project training outcomes"""
    try:
        players = parse_players_csv(args.file)
        projection = TrainingProjection(players, args.training or "playmaking")
        
        if args.compare:
            results = projection.compare_training_types()
        elif args.near_skillup:
            results = projection.find_players_near_skillup()
        else:
            results = projection.project_skill_ups(args.weeks or 4)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Projection saved to {args.output}")
        else:
            print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def junior_squad(args):
    """Analyze junior squad"""
    try:
        juniors = parse_players_csv(args.file)
        analyzer = JuniorSquadAnalyzer(juniors)
        
        if args.promotions:
            results = analyzer.recommend_promotions(args.max or 3)
        elif args.simulate:
            results = analyzer.simulate_training_impact(args.training or "playmaking", args.weeks or 4)
        elif args.formations:
            results = analyzer.compare_formations()
        else:
            results = analyzer.analyze_potential()
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Analysis saved to {args.output}")
        else:
            print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def match_analyzer(args):
    """Analyze match patterns"""
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            matches = json.load(f)
        
        analyzer = MatchAnalyzer(matches)
        
        if args.recent:
            results = analyzer.analyze_recent_form(args.last_n or 5)
        elif args.suggestions:
            results = {"suggestions": analyzer.suggest_tactical_changes()}
        else:
            results = analyzer.extract_patterns()
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Analysis saved to {args.output}")
        else:
            print(json.dumps(results, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Scouty - Hattrick Analytics and Strategy Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze players command
    parser_analyze = subparsers.add_parser('analyze', help='Analyze players')
    parser_analyze.add_argument('file', help='CSV file with player data')
    parser_analyze.add_argument('-o', '--output', help='Output file (JSON)')
    parser_analyze.set_defaults(func=analyze_players)
    
    # Team snapshot command
    parser_snapshot = subparsers.add_parser('snapshot', help='Generate team snapshot')
    parser_snapshot.add_argument('file', help='CSV file with player data')
    parser_snapshot.add_argument('-o', '--output', help='Output file (JSON)')
    parser_snapshot.set_defaults(func=team_snapshot)
    
    # Training projection command
    parser_training = subparsers.add_parser('training', help='Project training outcomes')
    parser_training.add_argument('file', help='CSV file with player data')
    parser_training.add_argument('-t', '--training', help='Training type (playmaking, defending, scoring, etc.)')
    parser_training.add_argument('-w', '--weeks', type=int, help='Number of weeks to project')
    parser_training.add_argument('-c', '--compare', action='store_true', help='Compare training types')
    parser_training.add_argument('-n', '--near-skillup', action='store_true', help='Find players near skillup')
    parser_training.add_argument('-o', '--output', help='Output file (JSON)')
    parser_training.set_defaults(func=training_projection)
    
    # Junior squad command
    parser_juniors = subparsers.add_parser('juniors', help='Analyze junior squad')
    parser_juniors.add_argument('file', help='CSV file with junior player data')
    parser_juniors.add_argument('-p', '--promotions', action='store_true', help='Recommend promotions')
    parser_juniors.add_argument('-s', '--simulate', action='store_true', help='Simulate training impact')
    parser_juniors.add_argument('-f', '--formations', action='store_true', help='Compare formations')
    parser_juniors.add_argument('-t', '--training', help='Training type for simulation')
    parser_juniors.add_argument('-w', '--weeks', type=int, help='Weeks for simulation')
    parser_juniors.add_argument('-m', '--max', type=int, help='Max promotions to recommend')
    parser_juniors.add_argument('-o', '--output', help='Output file (JSON)')
    parser_juniors.set_defaults(func=junior_squad)
    
    # Match analyzer command
    parser_matches = subparsers.add_parser('matches', help='Analyze match patterns')
    parser_matches.add_argument('file', help='JSON file with match data')
    parser_matches.add_argument('-r', '--recent', action='store_true', help='Analyze recent form')
    parser_matches.add_argument('-l', '--last-n', type=int, help='Number of recent matches to analyze')
    parser_matches.add_argument('-s', '--suggestions', action='store_true', help='Get tactical suggestions')
    parser_matches.add_argument('-o', '--output', help='Output file (JSON)')
    parser_matches.set_defaults(func=match_analyzer)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()


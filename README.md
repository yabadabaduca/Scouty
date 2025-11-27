# Scouty

Scouty is a lightweight, modular analytics and strategy toolkit for Hattrick. It provides player insights, lineup optimization, training projections, junior squad analysis, and decision-making tools — all in a simple, extensible assistant.

## What Scouty Does

Scouty helps you make smarter decisions by analyzing your team, training plan, players, juniors, and upcoming matches.

Each feature is implemented as a module, so you can extend or replace parts of the toolkit as your strategy evolves.

### Player Insights

Evaluate skills, roles, cost-benefit, potential and training impact.

### Team Snapshot

Full overview of your squad strengths, weaknesses and tactical recommendations.

### Training Projection

Estimate skill-ups, time to improve, financial ROI and impact of switching training types.

### Junior Squad Analysis

Predict potential, decide who to promote, train or release.

### Match Insights

Extract patterns from past games and adapt your tactical approach.

### Market Scout (future module)

Identify undervalued players and transfer opportunities based on your team strategy.

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/scouty.git
cd scouty

# Install in development mode
pip install -e .

# Or install dependencies only
pip install -r requirements.txt
```

## Quick Start

### Using the CLI

```bash
# Analyze players from CSV
scouty analyze players.csv

# Generate team snapshot
scouty snapshot players.csv

# Project training outcomes
scouty training players.csv --weeks 4

# Compare training types
scouty training players.csv --compare

# Find players near skillup
scouty training players.csv --near-skillup

# Analyze junior squad
scouty juniors juniors.csv

# Recommend promotions
scouty juniors juniors.csv --promotions --max 3

# Analyze match patterns
scouty matches matches.json

# Get tactical suggestions
scouty matches matches.json --suggestions
```

## Project Structure

```
scouty/
├── core/               # Core utilities and data models
│   ├── player.py      # Player data model
│   └── parser.py      # CSV/HTML parsing utilities
├── modules/            # Feature modules
│   ├── player_insights.py
│   ├── team_snapshot.py
│   ├── training_projection.py
│   ├── junior_squad.py
│   └── match_analyzer.py
├── cli/                # Command-line interface
│   └── main.py
├── storage/            # Data persistence (future)
└── config/             # Configuration management (future)
```

## Data Formats

### Players CSV Format

Expected CSV columns:
- `id`: Player ID
- `name`: Player name
- `age`: Player age
- `position`: Position (GK, CD, WB, IM, WI, FW)
- `skills`: JSON object with skill values (e.g., `{"defending": 15, "playmaking": 12}`)
- `salary`: Player salary
- `tsi`: Total Skill Index
- `form`: Form (1-8)
- `stamina`: Stamina level
- `experience`: Experience level
- `leadership`: Leadership level

### Matches JSON Format

```json
[
  {
    "date": "2024-01-15",
    "opponent": "Team Name",
    "result": "3-1",
    "possession": 52.5,
    "chances": 5,
    "tactics": "Normal",
    "formation": "4-4-2"
  }
]
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Documentation

Additional documentation can be found in the `docs/` directory:

- **HATTRICK_REFERENCE.md**: Reference guide for Hattrick game rules and mechanics

## Resources

- **Hattrick Official Site**: https://www86.hattrick.org/pt-br/
- **Hattrick Rules & Manual**: https://www86.hattrick.org/pt-br/Help/Rules/

## Acknowledgments

Built for the Hattrick community by Hattrick enthusiasts.

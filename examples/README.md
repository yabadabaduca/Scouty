# Examples

This directory contains example data files for testing Scouty.

## Files

- `players_example.csv`: Sample player data in CSV format
- `matches_example.json`: Sample match history in JSON format

## Usage

```bash
# Analyze example players
scouty analyze examples/players_example.csv

# Generate team snapshot
scouty snapshot examples/players_example.csv

# Analyze matches
scouty matches examples/matches_example.json

# Get tactical suggestions
scouty matches examples/matches_example.json --suggestions
```

## CSV Format

The players CSV should have the following columns:
- `id`: Unique player identifier
- `name`: Player name
- `age`: Player age
- `position`: Position code (GK, CD, WB, IM, WI, FW)
- `skills`: JSON object with skill values
- `salary`: Monthly salary
- `tsi`: Total Skill Index
- `form`: Current form (1-8)
- `stamina`: Stamina level
- `experience`: Experience level
- `leadership`: Leadership level

## JSON Format

Matches JSON should be an array of match objects with:
- `date`: Match date
- `opponent`: Opponent team name
- `result`: Match result (e.g., "3-1")
- `possession`: Possession percentage
- `chances`: Number of chances created
- `tactics`: Tactical approach used
- `formation`: Formation used


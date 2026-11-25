"""Team logos and colours from nflverse, cached locally for the chart scripts."""
from pathlib import Path

import matplotlib.image as mpimg
import nflreadpy as nfl
import pandas as pd
import requests

CACHE = Path("data/raw/logos")  # gitignored: re-fetched on demand


def teams() -> pd.DataFrame:
    return nfl.load_teams().to_pandas().set_index("team_abbr")


def _fetch(url: str, name: str):
    path = CACHE / name
    if not path.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        path.write_bytes(resp.content)
    return mpimg.imread(path)


def logo(team: str, table: pd.DataFrame):
    return _fetch(table.loc[team, "team_logo_espn"], f"{team}.png")


def league_logo(table: pd.DataFrame):
    return _fetch(table["team_league_logo"].iloc[0], "NFL.png")

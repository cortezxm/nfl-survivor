"""The picks log joined with results from the latest schedule snapshot."""
from pathlib import Path

import pandas as pd


def implied(moneyline: pd.Series) -> pd.Series:
    """American moneyline -> implied probability, vig included."""
    favorite = -moneyline / (-moneyline + 100)
    underdog = 100 / (moneyline + 100)
    return favorite.where(moneyline < 0, underdog)


def load_picks(season: int = 2026) -> pd.DataFrame:
    picks = pd.read_csv("picks.csv")
    picks = picks[picks["season"] == season]

    # No-vig win probability: normalise the two implied probabilities to sum to 1.
    pick_p, opp_p = implied(picks["pick_moneyline"]), implied(picks["opponent_moneyline"])
    picks = picks.assign(win_prob=pick_p / (pick_p + opp_p))

    # Results come from the latest snapshot, never from picks.csv.
    snapshot = sorted(Path("data/snapshots").glob("schedule_*.csv"))[-1]
    games = pd.read_csv(snapshot)
    games = games[games["season"] == season]
    scores = pd.concat([
        games[["week", "home_team", "home_score", "away_score"]]
            .set_axis(["week", "team", "pf", "pa"], axis=1),
        games[["week", "away_team", "away_score", "home_score"]]
            .set_axis(["week", "team", "pf", "pa"], axis=1),
    ])
    picks = picks.merge(scores, left_on=["week", "pick"], right_on=["week", "team"])
    picks["result"] = "pending"
    picks.loc[picks["pf"] > picks["pa"], "result"] = "won"
    picks.loc[picks["pf"] < picks["pa"], "result"] = "lost"
    return picks

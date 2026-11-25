from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

GOOD, CRITICAL, MUTED = "#0ca30c", "#d03b3b", "#898781"
INK, INK_2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e1e0d9", "#fcfcfb"


def implied(moneyline: pd.Series) -> pd.Series:
    """American moneyline -> implied probability, vig included."""
    favorite = -moneyline / (-moneyline + 100)
    underdog = 100 / (moneyline + 100)
    return favorite.where(moneyline < 0, underdog)


picks = pd.read_csv("picks.csv")
snapshot = sorted(Path("data/snapshots").glob("schedule_*.csv"))[-1]
games = pd.read_csv(snapshot)

# No-vig win probability: normalise the two implied probabilities to sum to 1.
pick_p, opp_p = implied(picks["pick_moneyline"]), implied(picks["opponent_moneyline"])
picks["win_prob"] = pick_p / (pick_p + opp_p)

# Results come from the latest snapshot, never from picks.csv.
games = games[games["season"] == 2026]
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

fig, ax = plt.subplots(figsize=(8, 4.5), facecolor=SURFACE)
ax.set_facecolor(SURFACE)

styles = {
    "won": dict(marker="o", s=90, color=GOOD, label="won"),
    "lost": dict(marker="X", s=130, color=CRITICAL, label="lost"),
    "pending": dict(marker="o", s=90, facecolor="none", edgecolor=MUTED,
                    linewidth=1.6, label="not played yet"),
}
for result, style in styles.items():
    rows = picks[picks["result"] == result]
    if rows.empty:
        continue
    ax.scatter(rows["week"], rows["win_prob"], zorder=3,
               **({"edgecolor": SURFACE, "linewidth": 2} | style))

for _, row in picks.iterrows():
    ax.annotate(row["pick"], (row["week"], row["win_prob"]),
                xytext=(0, 11), textcoords="offset points",
                ha="center", fontsize=8.5, color=INK_2)

first_loss = picks.loc[picks["result"] == "lost", "week"].min()
ax.axvspan(first_loss - 0.5, picks["week"].max() + 0.5, color=MUTED, alpha=0.08, lw=0)
ax.text(first_loss - 0.35, 0.665, f"eliminated in week {first_loss}\n"
        "everything right of here is measurement only",
        fontsize=8.5, color=INK_2, va="bottom")

played = picks[picks["result"] != "pending"]
wins = (played["result"] == "won").sum()
expected = played["win_prob"].sum()
ax.set_title(f"Every pick was a favorite. The record is {wins}-{len(played) - wins}; "
             f"the market expected {expected:.1f} wins.",
             fontsize=11, color=INK, loc="left")

ax.set_xlim(0.5, picks["week"].max() + 0.5)
ax.set_xticks(picks["week"])
ax.set_ylim(0.65, 1.0)
ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
ax.set_xlabel("week", color=INK_2)
ax.set_ylabel("market win probability of the pick (no vig)", color=INK_2)
ax.grid(axis="y", color=GRID, linewidth=1)
ax.set_axisbelow(True)
ax.tick_params(colors=MUTED, length=0)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#c3c2b7")
ax.legend(loc="lower left", frameon=False, fontsize=8.5, labelcolor=INK_2)

fig.tight_layout()
Path("charts").mkdir(exist_ok=True)
fig.savefig("charts/01_pick_probability.png", dpi=160, facecolor=SURFACE)

print(picks[["week", "pick", "opponent", "pick_moneyline", "win_prob", "pf", "pa", "result"]]
      .to_string(index=False))
print(f"expected wins {expected:.2f}, actual {wins}")

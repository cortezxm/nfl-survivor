from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

from brand import logo, teams
from season import load_picks

GOOD, CRITICAL, MUTED = "#0ca30c", "#d03b3b", "#898781"
INK, INK_2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e1e0d9", "#fcfcfb"

picks = load_picks()
team_table = teams()

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

# The team's logo rides above its dot; the tooltip-free PNG names it this way.
for _, row in picks.iterrows():
    badge = OffsetImage(logo(row["pick"], team_table), zoom=0.045)
    ax.add_artist(AnnotationBbox(badge, (row["week"], row["win_prob"]),
                                 xybox=(0, 20), boxcoords="offset points",
                                 frameon=False, zorder=4))

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
print(f"expected wins {expected:.2f}, actual {wins}")

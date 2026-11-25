from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.patches import Circle, FancyBboxPatch

from brand import league_logo, logo, teams
from season import load_picks

NAVY, NAVY_2, WHITE = "#013369", "#0a2a52", "#ffffff"
GOOD, CRITICAL, PENDING = "#0ca30c", "#d03b3b", "#898781"

picks = load_picks()
team_table = teams()
played = picks[picks["result"] != "pending"]
wins = (played["result"] == "won").sum()
first_loss = picks.loc[picks["result"] == "lost", "week"].min()

W, H = 16, 5
fig = plt.figure(figsize=(W, H), dpi=100, facecolor=NAVY)
ax = fig.add_axes((0, 0, 1, 1))
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.axis("off")

# Field: yard lines every 5 yards, hash marks in between.
for i, x in enumerate([0.5 + k * 0.75 for k in range(21)]):
    ax.plot([x, x], [0, H], color=WHITE, alpha=0.10 if i % 2 else 0.18, lw=2 if i % 2 == 0 else 1)
    for y in (H - 0.2,):
        ax.plot([x + 0.375, x + 0.375], [y - 0.08, y + 0.08], color=WHITE, alpha=0.12, lw=1)

ax.add_artist(AnnotationBbox(OffsetImage(league_logo(team_table), zoom=0.42),
                             (1.2, 3.3), frameon=False))
ax.text(2.6, 3.75, "nfl-survivor", color=WHITE, fontsize=50, weight="bold", va="center")
ax.text(2.65, 2.95, "How far does picking the market's biggest favorite carry you?",
        color=WHITE, alpha=0.85, fontsize=19, va="center")
ax.text(2.65, 2.45,
        f"2026 season  ·  greedy market baseline  ·  {wins}-{len(played) - wins}"
        f"  ·  eliminated in week {first_loss}",
        color=WHITE, alpha=0.6, fontsize=13, va="center")

# Season strip: one chip per week, logo on a white disc, result underneath.
tag = {"won": ("W", GOOD), "lost": ("L", CRITICAL), "pending": ("", PENDING)}
step = (W - 1.2) / len(picks)
for i, row in enumerate(picks.itertuples()):
    cx = 0.6 + step * (i + 0.5)
    ax.add_patch(Circle((cx, 1.1), 0.44, color=WHITE, zorder=2))
    ax.add_artist(AnnotationBbox(OffsetImage(logo(row.pick, team_table), zoom=0.105),
                                 (cx, 1.1), frameon=False, zorder=3))
    letter, colour = tag[row.result]
    ax.add_patch(FancyBboxPatch((cx - 0.36, 0.21), 0.72, 0.28, boxstyle="round,pad=0,rounding_size=0.08",
                                color=colour, zorder=2))
    ax.text(cx, 1.78, f"WK {row.week}", color=WHITE, alpha=0.7, fontsize=10,
            weight="bold", ha="center", va="center")
    score = f"{int(row.pf)}–{int(row.pa)}" if row.result != "pending" else "next"
    ax.text(cx, 0.35, f"{letter} {score}" if row.result != "pending" else score,
            color=WHITE, fontsize=9, weight="bold", ha="center", va="center", zorder=3)

Path("charts").mkdir(exist_ok=True)
fig.savefig("charts/00_banner.png", dpi=100, facecolor=NAVY)

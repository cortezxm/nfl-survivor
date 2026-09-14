from datetime import datetime, timezone

import nflreadpy as nfl

pulled_at = datetime.now(timezone.utc)

schedule = nfl.load_schedules(seasons=[2026]).to_pandas()
schedule["pulled_at"] = pulled_at.isoformat(timespec="seconds")

path = f"data/snapshots/schedule_{pulled_at:%Y%m%dT%H%M%SZ}.csv"
schedule.to_csv(path, index=False)
print(f"{len(schedule)} games -> {path}")

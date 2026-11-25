SELECT
	game_id,
	home_moneyline,
	away_moneyline,
	CASE
		WHEN home_moneyline < away_moneyline THEN home_team
		WHEN away_moneyline < home_moneyline THEN away_team
	END AS favorite,
	CASE 
		WHEN home_moneyline < away_moneyline THEN home_moneyline
		WHEN away_moneyline < home_moneyline THEN away_moneyline 
	END AS fav_moneyline
FROM read_csv('data/snapshots/schedule_20260914T234550Z.csv')
WHERE week = 1
ORDER BY fav_moneyline ASC;

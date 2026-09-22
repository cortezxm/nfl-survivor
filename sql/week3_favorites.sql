WITH 
	used AS (
		SELECT pick FROM read_csv('picks.csv') WHERE season = 2026),

	favorites AS (
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
		FROM read_csv('data/snapshots/schedule_20260922T180918Z.csv')
		WHERE week = 3)

SELECT *
FROM favorites
WHERE favorite NOT IN (SELECT pick FROM used)
ORDER BY fav_moneyline ASC;

# Telegram Text-Based Adventure Game

This game is developed using Python and hooks into a Telegram bot using a Telegram TOKEN. The idea is to produce a text-based adventure game feel, but in Telegram.

## Random SQL query test
select  broker_house, 
	SUM(Positive) AS Lapse, 
		SUM(Negative) AS TotalProduction,
		(SUM(Positive) + SUM(Negative)) AS NetProduction, 
		( SUM(Positive) / (SUM(Positive) + SUM(Negative) ) * 100 ) AS PerPercent

FROM tbl_brokers,
		((SELECT SUM(CASE
					WHEN [Test].diff > 0 THEN 0
					WHEN [Test].diff < 0 THEN [Test].diff
				END) AS 'Negative',
				0 AS 'Positive'
		FROM tbl_brokers as [Test])
		UNION ALL
		(SELECT 0 AS 'Negative',
				SUM(CASE
					WHEN [Test2].diff < 0 THEN 0
					WHEN [Test2].diff > 0 THEN [Test2].diff
				END) AS 'Positive'
		FROM tbl_brokers as [Test2])) AS Total

GROUP BY broker_house

USE tempdb
GO
-- Don't forget to create input first
WITH SmallNums AS (
	SELECT nums.num
	FROM (VALUES (1), (1), (1), (1), (1), (1), (1), (1), (1), (1)) AS nums (num)
),
Numbers AS (
	SELECT ROW_NUMBER() OVER (ORDER BY N1.num) AS n
	FROM SmallNums AS N1
	CROSS JOIN SmallNums AS N2
	CROSS JOIN SmallNums AS N3
	CROSS JOIN SmallNums AS N4
),
ValidInput AS (
	SELECT
		StartTime,
		CAST(InputVal AS INT) AS InputVal
	FROM Dec13Input
	WHERE InputVal <> 'x'
)
SELECT TOP 1 InputVal * n AS Answer
FROM ValidInput
CROSS JOIN Numbers
WHERE (StartTime + Numbers.n) % InputVal = 0
ORDER BY n
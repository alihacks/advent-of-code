USE tempdb
GO
-- Run Dec09Input.sql first to setup input. This can be inlined but moved to a single file to keep code cleaner
WITH 
PreambleLength AS (SELECT 25 AS PreambleLength),
ValidNums AS (
	SELECT I.Num
	FROM Dec09Input AS I
	INNER JOIN Dec09Input AS P1
		ON P1.NumIndex < I.NumIndex
			AND P1.NumIndex >= I.NumIndex - (SELECT PreambleLength FROM PreambleLength)
			AND P1.num < I.num
	INNER JOIN Dec09Input AS P2
		ON P2.NumIndex < I.NumIndex
			AND P2.NumIndex >= I.NumIndex - (SELECT PreambleLength FROM PreambleLength)
			AND P2.num < I.num
			AND P2.NumIndex > P1.NumIndex -- Don't duplicate
	WHERE
		I.NumIndex > (SELECT PreambleLength FROM PreambleLength)
		AND I.Num = P1.Num + P2.Num
)
SELECT Num AS Answer
FROM Dec09Input AS I
WHERE Numindex > (SELECT PreambleLength FROM PreambleLength)
AND NOT EXISTS (SELECT 1 FROM ValidNums AS V WHERE V.num = I.num)
USE tempdb
GO
-- Run Dec09Input.sql first to setup input. This can be inlined but moved to a single file to keep code cleaner

-- This is a performance only hack as string split seems to be slow in a large set based operation
-- We can work w/o this step but it's much faster this way
DROP TABLE IF EXISTS #input
CREATE TABLE #input(NumIndex INT, Num BIGINT, INDEX IX1 CLUSTERED(NumIndex, Num))
INSERT #input SELECT * FROM dec09input;

WITH Part1Answer AS (SELECT 29221323 AS Answer), -- Pasted for efficiency, can use prior CTE,
Ranges AS (
	SELECT
		P.NumIndex AS StartIndex,
		I.NumIndex AS EndIndex,
		P.Num AS StartNum,
		I.Num AS EndNum
	FROM #input AS I
	INNER JOIN #input AS P
		ON P.NumIndex < I.NumIndex
),
RunningSums AS (
	SELECT *
	FROM Ranges
	CROSS APPLY (
		SELECT SUM(num) AS RangeSum
		FROM #input
		WHERE
			NumIndex BETWEEN StartIndex AND EndIndex
	) AS Sums
),
AnswerIndexes AS(
SELECT StartIndex, EndIndex
FROM RunningSums
WHERE RunningSums.RangeSum = (SELECT Part1Answer.Answer FROM Part1Answer)
)
SELECT MIN(Num) + MAX(Num) AS Answer
FROM AnswerIndexes A
CROSS APPLY #input I
WHERE I.numindex BETWEEN A.StartIndex AND A.EndIndex


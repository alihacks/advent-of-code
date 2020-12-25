USE tempdb
GO
-- Make sure to create input first

-- Performance hack, copy to table
DROP TABLE IF EXISTS #input
CREATE TABLE #input (Num BIGINT PRIMARY KEY CLUSTERED)
INSERT #input
SELECT Num
FROM dbo.Dec10Input;

DECLARE @List VARCHAR(MAX);

WITH X AS (
	SELECT
		CAST(0 AS BIGINT) AS PrevNum,
		I.Num,
		CAST(I.Num AS VARCHAR(MAX)) AS List
	FROM #input AS I
	WHERE
		I.Num IN ( 1 )
	UNION ALL
	SELECT
		X.Num AS PrevNum,
		I1.Num,
		X.List + '|' + CAST(I1.Num AS VARCHAR)
	FROM X
	CROSS APPLY (
		SELECT
			I1.Num,
			ROW_NUMBER() OVER (ORDER BY I1.Num) AS rn
		FROM #input AS I1
		WHERE
			I1.Num - X.Num BETWEEN 1 AND 3
	) AS I1 -- Hack because we can't do MIN() in recursive CTE
	WHERE I1.rn = 1
)
SELECT TOP 1 @List = X.List
FROM X
WHERE Num = (SELECT MAX(num) FROM #input)
OPTION (MAXRECURSION 200);

WITH ListParts AS (
	SELECT
		ROW_NUMBER() OVER (ORDER BY @List) AS NumIndex,
		CAST(value AS BIGINT) AS Num
	FROM STRING_SPLIT(@List, '|')
),
Differences AS (
	SELECT
		L1.NumIndex,
		L1.Num,
		L1.Num - ISNULL(LAG(L1.Num) OVER (ORDER BY L1.NumIndex), 0) AS DiffVal
	FROM ListParts AS L1
),
Islands AS (
	SELECT
		*,
		IIF(Differences.DiffVal = 1 AND ISNULL(LAG(Differences.DiffVal) OVER (ORDER BY Differences.NumIndex), 3) = 3, 1, 0) AS OneStart,
		IIF(
			Differences.DiffVal = 1
			   AND ISNULL(LEAD(Differences.DiffVal) OVER (ORDER BY Differences.NumIndex), 3) = 3,
			1,
			0) AS OneEnd
	FROM Differences
),
-- Find groups of 1 combinations
Groups AS (
	SELECT
		*,
		SUM(Islands.OneStart) OVER (PARTITION BY Islands.DiffVal
									ORDER BY Islands.NumIndex
									ROWS UNBOUNDED PRECEDING
							  ) AS grp
	FROM Islands
	WHERE Islands.DiffVal = 1
),
GroupCounts AS (SELECT Groups.grp, COUNT(*) AS cnt FROM Groups GROUP BY Groups.grp)
SELECT ROUND(EXP(SUM(LOG(mult.mult))), 0) AS Answer
FROM GroupCounts AS g
INNER JOIN (VALUES (4, 7), (3, 4), (2, 2), (1, 1)) AS mult (val, mult) -- Mapping of combinations each 1 sequence adds: 4 1s = x7, 3 1s = x3 etc
	ON mult.val = g.cnt
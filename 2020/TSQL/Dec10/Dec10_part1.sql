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
ORDER BY LEN(X.List) DESC
OPTION (MAXRECURSION 200);

WITH ListParts AS (
	SELECT
		ROW_NUMBER() OVER (ORDER BY @List) AS NumIndex,
		CAST(value AS BIGINT) AS Num
	FROM STRING_SPLIT(@List, '|')
),
Differences AS(
SELECT
	L1.Num - LAG(L1.Num) OVER (ORDER BY L1.NumIndex) AS DiffVal
FROM ListParts AS L1)
SELECT (SUM(IIF(DiffVal = 1,1,0)) + 1) * (1+ SUM(IIF(DiffVal = 3,1,0))) -- +1 to 1 for start, +1 to 3 for end
FROM Differences

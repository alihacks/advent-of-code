USE tempdb
GO
CREATE OR ALTER VIEW dbo.Dec13Input
AS
WITH Input AS (
	SELECT 1008832 AS StartTime, '23,x,x,x,x,x,x,x,x,x,x,x,x,41,x,x,x,x,x,x,x,x,x,449,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,13,19,x,x,x,x,x,x,x,x,x,29,x,991,x,x,x,x,x,37,x,x,x,x,x,x,x,x,x,x,17' AS InputString
),
InputLines AS (
	SELECT
		StartTime,
		CAST(ROW_NUMBER() OVER (ORDER BY Input.InputString) AS INT) AS InputIndex,
		CAST(value AS VARCHAR(20)) AS InputVal
	FROM Input
	CROSS APPLY STRING_SPLIT(Input.InputString, ',')
)
SELECT *
FROM InputLines
GO
USE tempdb
GO
CREATE OR ALTER VIEW dbo.Dec10Input
AS
WITH Input AS (
	SELECT '28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3' AS InputString
),
InputLines AS (
	SELECT
		ROW_NUMBER() OVER (ORDER BY Input.InputString) AS NumIndex,
		CAST(value AS BIGINT) Num
	FROM Input
	CROSS APPLY STRING_SPLIT(REPLACE(Input.InputString, CHAR(0xD) + CHAR(0xA), '^'), '^')
)
SELECT *
FROM InputLines
GO

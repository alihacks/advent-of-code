USE tempdb
GO
-- Run Dec06Input.sql first to setup input. This can be inlined but moved to a single file to keep code cleaner
WITH InputGroups AS (
	SELECT
		ROW_NUMBER() OVER (ORDER BY InputString) AS GroupId,
		REPLACE(REPLACE(value, CHAR(0xD) + CHAR(0xA), ''), ' ', '') AS ItemString
	FROM Dec06Input
	CROSS APPLY STRING_SPLIT(REPLACE(InputString, CHAR(0xD) + CHAR(0xA) + CHAR(0xD) + CHAR(0xA), '^'), '^')
),
MaxInputLen AS (SELECT MAX(LEN(InputGroups.ItemString)) AS MaxLen FROM InputGroups),
-- Generate enough numbers for our needs
Numbers AS (
	SELECT 1 AS num
	UNION ALL
	SELECT Numbers.num + 1
	FROM Numbers
	WHERE Numbers.num <= (SELECT MaxInputLen.MaxLen FROM MaxInputLen)
),
GroupsWithLetters AS (
	SELECT
		IG.GroupId,
		SUBSTRING(IG.ItemString, N.num, 1) AS Letter
	FROM InputGroups AS IG
	INNER JOIN Numbers AS N
		ON N.num <= LEN(IG.ItemString)
),
GroupCounts AS (
	SELECT
		GroupsWithLetters.GroupId,
		COUNT(DISTINCT GroupsWithLetters.Letter) AS GroupLetterCount
	FROM GroupsWithLetters
	GROUP BY GroupsWithLetters.Groupid
)
SELECT SUM(GroupCounts.GroupLetterCount) AS Answer
FROM GroupCounts
OPTION (MAXRECURSION 300)

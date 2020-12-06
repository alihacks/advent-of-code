USE tempdb
GO
-- Run Dec06Input.sql first to setup input. This can be inlined but moved to a single file to keep code cleaner
WITH InputGroups AS (
	SELECT
		ROW_NUMBER() OVER (ORDER BY InputString) AS Groupid,
		REPLACE(REPLACE(value, CHAR(0xD) + CHAR(0xA), ''), ' ', '') AS ItemString
	FROM Dec06Input
	CROSS APPLY STRING_SPLIT(REPLACE(InputString, CHAR(0xD) + CHAR(0xA) + CHAR(0xD) + CHAR(0xA), '^'), '^')
),
MaxInputLen AS(
SELECT MAX(LEN(ItemString)) AS MaxLen FROM InputGroups
),
Numbers AS (SELECT 1 AS num
        UNION ALL
        SELECT num + 1 
        FROM Numbers
        WHERE num <= (SELECT MaxLen FROM MaxInputLen)
       ),
GroupsWithLetters AS(
SELECT GroupId, SUBSTRING(IG.ItemString,num,1) AS Letter
FROM InputGroups AS IG
INNER JOIN Numbers AS N ON N.num <= LEN(IG.ItemString)
),
GroupCounts AS(
SELECT GroupId, COUNT(DISTINCT Letter) AS GroupLetterCount
FROM GroupsWithLetters
GROUP BY GroupId
)
SELECT SUM(GroupLetterCount) AS Answer
FROM GroupCounts
OPTION(MAXRECURSION 300)

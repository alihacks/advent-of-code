USE tempdb
GO
-- Run Dec06Input.sql first to setup input. This can be inlined but moved to a single file to keep code cleaner
WITH InputGroups AS (
	-- Note this is different compared to part1
	SELECT
		ROW_NUMBER() OVER (ORDER BY InputString) AS GroupId,
		value AS GroupString
	FROM Dec06Input
	CROSS APPLY STRING_SPLIT(REPLACE(InputString, CHAR(0xD) + CHAR(0xA) + CHAR(0xD) + CHAR(0xA), '^'), '^')
),
GroupedInput AS (
	SELECT
		InputGroups.GroupId,
		ROW_NUMBER() OVER (PARTITION BY InputGroups.GroupId ORDER BY InputGroups.GroupString) AS InputId,
		value AS InputValue
	FROM InputGroups
	CROSS APPLY STRING_SPLIT(REPLACE(InputGroups.GroupString, CHAR(0xD) + CHAR(0xA), '^'), '^')
),
MaxInputLen AS (SELECT MAX(LEN(GroupedInput.InputValue)) AS MaxLen FROM GroupedInput),
Numbers AS (
	SELECT 1 AS num
	UNION ALL
	SELECT Numbers.num + 1
	FROM Numbers
	WHERE Numbers.num <= (SELECT MaxInputLen.MaxLen FROM MaxInputLen)
),
GroupsWithLetters AS (
	SELECT
		GI.*,
		SUBSTRING(GI.InputValue, N.num, 1) AS Letter
	FROM GroupedInput AS GI
	INNER JOIN Numbers AS N
		ON N.num <= LEN(GI.InputValue)
),
-- Count number of passengers
GroupPassengerCounts AS (
	SELECT
		GroupsWithLetters.GroupId,
		COUNT(DISTINCT GroupsWithLetters.InputId) AS NumPassengers
	FROM GroupsWithLetters
	GROUP BY GroupsWithLetters.GroupId
),
-- Count number of occurrences of each letter in a group
GroupLetterCounts AS (
	SELECT
		GroupsWithLetters.GroupId,
		GroupsWithLetters.Letter,
		COUNT(*) AS NumLetters
	FROM GroupsWithLetters
	GROUP BY
		GroupsWithLetters.GroupId,
		GroupsWithLetters.Letter
)
SELECT COUNT(*) AS Answer
FROM GroupPassengerCounts AS GIC
INNER JOIN GroupLetterCounts AS GLC
	ON GIC.GroupId = GLC.GroupId
WHERE GIC.NumPassengers = GLC.NumLetters -- Each person selected the letter

USE tempdb 
GO
-- Run input.sql first
WITH Input AS (
	SELECT
		ROW_NUMBER() OVER (ORDER BY i.string) AS BoardingPassId,
		i.string
	FROM dbo.Dec05Input AS i
	-- Testing -- (VALUES ('FBFBBFFRLR'), ('BFFFBBFRRR'), ('FFFBBBFRRR'), ('BBFFBBFRLL')) AS i (string)
),
Places AS (
	SELECT
		nums.num,
		-- We only add to our valur if it's a Back or a Right
		IIF(nums.num BETWEEN 1 AND 7, 'B', 'R') AS PlaceChar,
		CASE
			-- First 7 chars are front/backs
			WHEN nums.num BETWEEN 1 AND 7 THEN
				POWER(2, 7 - nums.num) * 8 -- the value will be like (64, 32, 16..) * 8
			-- Rest is left/rights
			ELSE
				POWER(2, 10 - nums.num) -- and Rights seats add 4,2,1
		END AS PlaceValue

	-- This can be generated but for 10 I may just as well type it out
	FROM (VALUES (1), (2), (3), (4), (5), (6), (7), (8), (9), (10)) AS nums (num)
),
SeatNumbers AS (
	SELECT
		Input.BoardingPassId,
		SUM(Places.PlaceValue) AS SeatNumber
	FROM Input
	INNER JOIN Places
		ON SUBSTRING(Input.string, Places.num, 1) = Places.PlaceChar
	GROUP BY Input.BoardingPassId
)
SELECT MAX(SeatNumbers.SeatNumber)
FROM SeatNumbers
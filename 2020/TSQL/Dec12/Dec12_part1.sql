USE tempdb
GO
-- Don't forget to create input first
WITH Commands AS (
	SELECT
		*,
		LEFT(Command, 1) AS MoveType,
		CAST(SUBSTRING(Command, 2, LEN(Command)) AS INT) AS MoveAmount
	FROM Dec12Input
),
ParsedCommands AS (
	SELECT
		*,
		IIF(C.MoveType = 'F', C.MoveAmount, 0) AS ForwardMove,
		IIF(C.MoveType IN ( 'L', 'R' ), IIF(C.MoveType = 'L', C.MoveAmount * -1, C.MoveAmount), 0) AS Turn,
		IIF(C.MoveType IN ( 'N', 'S' ), IIF(C.MoveType = 'N', C.MoveAmount * -1, C.MoveAmount), 0) AS XMove,
		IIF(C.MoveType IN ( 'E', 'W' ), IIF(C.MoveType = 'W', C.MoveAmount * -1, C.MoveAmount), 0) AS YMove
	FROM Commands AS C
),
Moves AS (
	SELECT
		CAST(0 AS INT) AS CommandIndex,
		CAST('' AS VARCHAR(20)) AS Command,
		'' AS MoveType,
		0 AS MoveAmount,
		0 AS ForwardMove,
		0 AS Turn,
		0 AS Ymove,
		0 AS Xmove,
		0 AS CurrentX,
		0 AS CurrentY,
		90 AS CurrentD,
		0 AS NextX,
		0 AS NextY,
		90 AS NextD
	UNION ALL
	SELECT
		PC.CommandIndex,
		PC.Command,
		PC.MoveType,
		PC.MoveAmount,
		PC.ForwardMove,
		PC.Turn,
		PC.Ymove,
		PC.Xmove,
		M.NextX AS CurrentX,
		M.NextY AS CurrentY,
		M.NextD AS CurrentD, -- Start Facing East
		CASE
			WHEN PC.ForwardMove > 0 THEN
				-- Only 0 and 180 change X
				IIF(M.NextD IN (0,180), IIF(M.NextD = 0, M.NextX - PC.MoveAmount,M.NextX + PC.MoveAmount) ,M.NextX)
			WHEN PC.XMove <> 0 THEN
				M.NextX + PC.XMove
			ELSE
				M.NextX
		END AS NextX,
		CASE
			WHEN PC.ForwardMove > 0 THEN
				-- Only 90 and 270 change Y
				IIF(M.NextD IN (90,270), IIF(M.NextD = 90, M.NextY + PC.MoveAmount,M.NextY - PC.MoveAmount) ,M.NextY)
			WHEN PC.YMove <> 0 THEN
				M.NextY + PC.YMove
			ELSE
				M.NextY
		END AS NextY,
		CASE
			WHEN PC.Turn <> 0 THEN
				(M.NextD + PC.Turn + 360) % 360
			ELSE
				M.NextD
		END AS NextD
	FROM ParsedCommands AS PC
	INNER JOIN Moves AS M
		ON PC.CommandIndex = M.CommandIndex + 1
)
SELECT TOP 1 ABS(NextX) + ABS(NextY) AS Answer
FROM Moves
ORDER BY Moves.CommandIndex DESC
OPTION (MAXRECURSION 1000)

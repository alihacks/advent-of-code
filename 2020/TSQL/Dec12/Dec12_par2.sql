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
		IIF(C.MoveType IN ( 'L', 'R' ), (360 + IIF(C.MoveType = 'L', C.MoveAmount * -1, C.MoveAmount)) % 360 , 0) AS Turn,
		IIF(C.MoveType IN ( 'N', 'S' ), IIF(C.MoveType = 'N', C.MoveAmount * -1, C.MoveAmount), 0) AS RowMove,
		IIF(C.MoveType IN ( 'E', 'W' ), IIF(C.MoveType = 'W', C.MoveAmount * -1, C.MoveAmount), 0) AS ColMove
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
		0 AS ColMove,
		0 AS RowMove,
		0 AS CurrentRow,
		0 AS CurrentCol,
		0 AS WpRow,
		0 AS WpCol,
		0 AS NextRow,
		0 AS NextCol,
		-1 AS NextWpRow,
		10 AS NextWpCol
	UNION ALL
	SELECT
		PC.CommandIndex,
		PC.Command,
		PC.MoveType,
		PC.MoveAmount,
		PC.ForwardMove,
		PC.Turn,
		PC.ColMove,
		PC.RowMove,
		M.NextRow AS CurrentRow,
		M.NextCol AS CurrentCol,
		M.NextWpRow AS WpRow,
		M.NextWpCol AS WpCol,
		CASE
			WHEN PC.ForwardMove > 0 THEN
				M.NextRow + PC.MoveAmount * M.NextWpRow
			ELSE
				M.NextRow
		END AS NextRow,
		CASE
			WHEN PC.ForwardMove > 0 THEN
				M.NextCol + PC.MoveAmount * M.NextWpCol
			ELSE
				M.NextCol
		END AS NextCol,
		-- TODO
		CASE
			WHEN PC.Turn = 0 THEN
				M.NextWpRow + PC.RowMove
			ELSE
				-- Rotation
				CASE
					WHEN PC.Turn = 90 THEN
						 M.NextWpCol
					WHEN PC.Turn = 180 THEN
						-1 * M.NextWpRow
					WHEN PC.Turn = 270 THEN
						-1 * M.NextWpCol
				END
		END AS WpRow,
		CASE
			WHEN PC.Turn = 0 THEN
				M.NextWpCol + PC.ColMove
			ELSE
				-- Rotation
				CASE
					WHEN PC.Turn = 90 THEN
						-1 * M.NextWpRow
					WHEN PC.Turn = 180 THEN
						-1 * M.NextWpCol
					WHEN PC.Turn = 270 THEN
						M.NextWpRow
				END
		END AS WpCol
	FROM ParsedCommands AS PC
	INNER JOIN Moves AS M
		ON PC.CommandIndex = M.CommandIndex + 1
)
SELECT TOP 1
	ABS(Moves.NextRow) + ABS(Moves.NextCol) AS Answer
FROM Moves
ORDER BY Moves.CommandIndex DESC
OPTION (MAXRECURSION 1000)

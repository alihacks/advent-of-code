USE tempdb
GO
-- Run Dec08Input.sql first to setup input. This can be inlined but moved to a single file to keep code cleaner
-- Also today I moved parsing into the input as well, still all set based
WITH Numbers AS (
	SELECT 0 AS num
	UNION ALL
	SELECT Numbers.num + 1
	FROM Numbers
	WHERE Numbers.num <= 626
),
NumbersToFuzz AS (
	SELECT 0 AS num
	UNION ALL
	SELECT N.num
	FROM Numbers AS N
	INNER JOIN dbo.dec08input AS I
		ON (N.num = I.CommandIndex AND I.Command IN ( 'jmp', 'nop' ))
),
Fuzz AS (
	SELECT
		N.num AS FuzzIter,
		I.CommandIndex,
		CASE
			WHEN N.num = CommandIndex
				AND Command = 'nop' THEN
				'jmp'
			WHEN N.num = CommandIndex
				AND Command = 'jmp' THEN
				'nop'
			ELSE
				I.Command
		END AS Command,
		I.Argument
	FROM dbo.dec08input AS I
	CROSS JOIN NumbersToFuzz AS N
),
GameBoy AS (
	SELECT
		Fuzz.FuzzIter,
		1 AS Seq,
		CommandIndex,
		Fuzz.Command,
		Argument,
		0 AS Memory,
		CASE
			WHEN Fuzz.Command = 'jmp' THEN
				CommandIndex + Argument
			ELSE -- Not jumping go to next command
				CommandIndex + 1
		END AS NextIndex,
		CAST('|1|' AS VARCHAR(MAX)) AS VisitedIndices
	FROM Fuzz
	WHERE
		CommandIndex = 1
		-- I was running this in ranges at first since I'm not patient
		-- it does not change the outcome, only performance, uncomment next line for SPEED
		-- AND Fuzz.FuzzIter BETWEEN 300 AND 400
	UNION ALL
	SELECT
		C.FuzzIter,
		P.Seq + 1 AS Seq,
		C.CommandIndex,
		C.Command,
		C.Argument,
		CASE
			WHEN C.Command = 'acc' THEN
				P.Memory + C.Argument
			ELSE
				P.Memory
		END AS Memory,
		CASE
			WHEN C.Command = 'jmp' THEN
				C.CommandIndex + C.Argument
			ELSE -- Not jumping go to next command
				C.CommandIndex + 1
		END AS Nextindex,
		P.VisitedIndices + CAST(C.CommandIndex AS VARCHAR(MAX)) + '|' AS VisitedIndices
	FROM GameBoy AS P
	INNER JOIN Fuzz AS C
		ON C.FuzzIter = P.FuzzIter
			AND C.CommandIndex = P.NextIndex
			AND P.VisitedIndices NOT LIKE '%|' + CAST(C.CommandIndex AS VARCHAR(MAX)) + '|%'
),
WorkingFuzzIter AS (
	SELECT TOP 1 C.FuzzIter
	FROM GameBoy AS C
	WHERE C.NextIndex = (SELECT MAX(CommandIndex) + 1 FROM dbo.dec08input)
),
PatchedInput AS (
	SELECT
		Commandindex,
		CASE
			WHEN (SELECT WorkingFuzzIter.FuzzIter FROM WorkingFuzzIter) = CommandIndex THEN
				CASE
					WHEN 360 = CommandIndex
						AND Command = 'nop' THEN
						'jmp'
					WHEN 360 = CommandIndex
						AND Command = 'jmp' THEN
						'nop'
				END
			ELSE
				Command
		END AS Command,
		Argument
	FROM dec08input
),
PatchedGameBoy AS (
	SELECT
		1 AS Seq,
		CommandIndex,
		PatchedInput.Command,
		Argument,
		0 AS Memory,
		CAST('|1|' AS VARCHAR(MAX)) AS VisitedIndices
	FROM PatchedInput
	WHERE CommandIndex = 1
	UNION ALL
	SELECT
		P.Seq + 1 AS Seq,
		C.CommandIndex,
		C.Command,
		C.Argument,
		CASE
			WHEN C.Command = 'acc' THEN
				P.Memory + C.Argument
			ELSE
				P.Memory
		END AS Memory,
		P.VisitedIndices + CAST(C.CommandIndex AS VARCHAR(MAX)) + '|' AS VisitedIndices
	FROM PatchedGameBoy AS P
	INNER JOIN PatchedInput AS C
		ON C.CommandIndex = CASE
								WHEN P.Command = 'jmp' THEN
									P.CommandIndex + P.Argument
								ELSE -- Not jumping go to next command
									P.CommandIndex + 1
							END
			AND P.VisitedIndices NOT LIKE '%|' + CAST(C.CommandIndex AS VARCHAR(MAX)) + '|%'
)
SELECT TOP 1 Memory AS Answer
FROM PatchedGameBoy AS C
ORDER BY C.Seq DESC
OPTION (MAXRECURSION 1000)

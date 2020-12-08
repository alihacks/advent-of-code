USE tempdb
GO
-- Run Dec08Input.sql first to setup input. This can be inlined but moved to a single file to keep code cleaner
-- Also today I moved parsing into the input as well, still all set based
WITH GameBoy AS (
	SELECT
		1 AS Seq,
		CommandIndex,
		Command,
		Argument,
		0 AS Memory,
		CAST( '|1|' AS VARCHAR(MAX)) AS VisitedIndices
	FROM dbo.dec08input
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
	FROM GameBoy AS P
	INNER JOIN dbo.dec08input AS C
		ON C.CommandIndex = CASE
								WHEN P.Command = 'jmp' THEN
									P.CommandIndex + P.Argument
								ELSE -- Not jumping go to next command
									P.CommandIndex + 1
							END
	AND P.VisitedIndices NOT LIKE '%|' + CAST(C.CommandIndex AS VARCHAR(MAX)) + '|%'
			
)
SELECT TOP 1 C.Memory AS Answer
FROM GameBoy C
ORDER BY Seq DESC
OPTION(MAXRECURSION 1000)

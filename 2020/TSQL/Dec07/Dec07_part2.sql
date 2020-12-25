USE tempdb
GO
-- Run Dec07Input.sql first to setup input. This can be inlined but moved to a single file to keep code cleaner
-- Also today I moved parsing into the input as well, still all set based
WITH CastedInput AS (
	-- Just cast the ints here so we can do math below
	SELECT
		BagColor,
		CAST(IIF(ContainsBagCount = 'no', NULL, ContainsBagCount) AS INT) AS ContainsBagCount,
		ContainsBagCount AS mc,
		ContainsBagColor
	FROM Dec07Input
),
BagLinks AS (
	SELECT
		BagColor,
		CastedInput.ContainsBagCount,
		ContainsBagColor,
		ContainsBagCount AS TotalBags
	FROM CastedInput
	WHERE BagColor = 'shiny gold' -- this is reversed from part1
	UNION ALL
	SELECT
		I.BagColor,
		I.ContainsBagCount,
		I.ContainsBagColor,
		I.ContainsBagCount * L.TotalBags AS TotalBags
	FROM CastedInput AS I
	INNER JOIN BagLinks AS L
		ON I.BagColor = L.ContainsBagColor -- this is reversed from part1
)
SELECT SUM(BagLinks.TotalBags) AS Answer
FROM BagLinks

USE tempdb
GO
-- Run Dec07Input.sql first to setup input. This can be inlined but moved to a single file to keep code cleaner
-- Also today I moved parsing into the input as well, still all set based
WITH BagLinks AS (
	SELECT
		BagColor,
		ContainsBagCount,
		ContainsBagColor
	FROM Dec07Input
	WHERE ContainsBagColor = 'shiny gold'
	UNION ALL
	SELECT
		I.BagColor,
		I.ContainsBagCount,
		I.ContainsBagColor
	FROM Dec07Input AS I
	INNER JOIN BagLinks AS L
		ON  I.ContainsBagColor = L.BagColor
)
SELECT COUNT(DISTINCT BagColor) -- Unique bags that can end up containing shiny gold
FROM BagLinks

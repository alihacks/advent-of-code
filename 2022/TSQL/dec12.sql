-- Requires SQL Server 2022 for GENERATE_SERIES and STRING_SPLIT(..use_ordinal)
USE tempdb
GO
DECLARE @input VARCHAR(MAX) = 'abccccccccaaaaaaaccaaaaaaaaaaaaaaaaccccccccccccccccccccccccccccccccccccaaaaaa
abccccccccaaaaaaaccaaaaaaaaaaaaaaaaccccccccccccccccccccccccccccccccccccaaaaaa
abccccccccccaaaaaaccaaaaaaaaaaaaaaaaccccccccccccccccacccccccccccccccccccaaaaa
abcccccaaaacaaaaaaccaaaaaaaaaaaaaaaaacccccccccccccccaaaccccaccccccccccccccaaa
abccccaaaaacaaccccccaaaaaacaaacaacaaaaaaacccccccccccaaaacccaacccccccccccccaaa
abaaccaaaaaaccccaaacaaaacacaaacaaccaaaaaacccccccccccaklaccccccccccccccccccaac
abaaccaaaaaaccaaaaaacccccccaaacccaaaaaaaccccccccccckkkllllccccccccccccccccccc
abaaccaaaaaaccaaaaaacccccccaaaaacaaaaaaacccccccccckkkklllllcccccccaaaccaccccc
abacccccaacccccaaaaacccccccaaaaaccaaaaaaacccccccckkkkpppllllccccccaaaaaaccccc
abacccccccccccaaaaacccccccccaaaacccaaaaaaccccccckkkkpppppplllccccddddaaaccccc
abccccccccccccaaaaaccccccccccaaaccaaaccccccccccckkkppppppppllllldddddddaccccc
abccacccccccccccccccccccccccccccccaaccccccccccckkkopppupppplllmmmmdddddaacccc
abccaaacaaaccccccccccccccccccccaaaaaaaaccccccckkkkopuuuuupppllmmmmmmddddacccc
abccaaaaaaaccccccccccccccccccccaaaaaaaacccccjjkkkooouuuuuuppqqqqqmmmmddddcccc
abccaaaaaacccccccccccccccaaccccccaaaacccccjjjjjjoooouuxuuuppqqqqqqmmmmdddcccc
abcaaaaaaaacccccccccccccaaacccccaaaaaccccjjjjoooooouuuxxuuvvvvvqqqqmmmdddcccc
abaaaaaaaaaacccccccaaaaaaacaacccaacaaacccjjjooooouuuuxxxxvvvvvvvqqqmmmdddcccc
abaaaaaaaaaacccaaacaaaaaaaaaacccacccaaccjjjooootttuuuxxxyyvyyvvvqqqmmmeeecccc
abcccaaacaaacccaaaaaaacaaaaaccccccccccccjjjooottttxxxxxxyyyyyyvvqqqmmmeeccccc
abcccaaacccccccaaaaaacaaaaaccccaaccaacccjjjnnntttxxxxxxxyyyyyvvvqqqnneeeccccc
SbccccaacccccccaaaaaaaaacaaacccaaaaaacccjjjnnntttxxxEzzzzyyyyvvqqqnnneeeccccc
abcccccccccccccaaaaaaaaacaaccccaaaaaccccjjjnnnttttxxxxyyyyyvvvrrrnnneeecccccc
abcccaacccccccaaaaaaaaaccccccccaaaaaacccciiinnnttttxxxyyyyywvvrrrnnneeecccccc
abcccaaaaaaccaaaaaaaacccccccccaaaaaaaaccciiiinnnttttxyyywyyywvrrrnnneeecccccc
abcccaaaaaaccaaaaaaaacccccccccaaaaaaaacccciiinnnntttxwywwyyywwwrrnnneeecccccc
abcaaaaaaaccaaaaaaaaaccccccccccccaacccccccciiinnnttwwwwwwwwwwwwrrnnneeecccccc
abcaaaaaaaccaaaaaacccccccccccccccaaccccccaaiiiinnttwwwwwwwwwwwrrrnnnffecccccc
abcccaaaaaaccaaaaaccccccccccccccccccccaaaaaciiinnssswwwssssrwwrrrnnnfffcccccc
abaacaaccaaccaaaccccccccaacccccccccccccaaaaaiiinnssssssssssrrrrrronnfffcccccc
abaccaaccaacccccccccaaacaacccccccccccccaaaaaiiimmmssssssmoosrrrrooonffaaacccc
abaaaccccaaaaaaccccccaaaaaccccccccccccaaaaaccihmmmmsssmmmoooooooooofffaaacccc
abaaaccccaaaaaacccccccaaaaaacccccccccccccaacchhhmmmmmmmmmoooooooooffffaaccccc
abaacccaaaaaaaccccccaaaaaaaaccccaaccccccccccchhhhmmmmmmmgggggooofffffaaaccccc
abaacccaaaaaaaccccccaaaaaaaccccaaaaccccccccccchhhhmmmmhggggggggfffffaaaaccccc
abccccccaaaaaaacccccaacaaaaacccaaaaccccccccccchhhhhhhhggggggggggfffaacaaccccc
abccaacccaaaaaaccccccccaaaaaccaaaaacccccccccccchhhhhhhggaaaaaaccccccccccccccc
abccaaaccaaccccccccccccccaaaaaaaaaccccccccccccccchhhhaaaccaaaacccccccccccccaa
abaaaaaaaccccccccccccccccaaaaaaaaccccccccccccccccccccaaaccccaaccccccccccccaaa
abaaaaaaaccccccccaaaccccacaaaaaacccccccccccccccccccccaaaccccccccccccccccccaaa
abaaaaaacccccccaaaaacaaaaaaaaaaacccccccccccccccccccccaaccccccccccccccccaaaaaa
abaaaaaacccccccaaaaaaaaaaaaaaaaaaacccccccccccccccccccccccccccccccccccccaaaaaa
';

-- Can't do graph with temp tables
DROP TABLE IF EXISTS dbo.Heights;
DROP TABLE IF EXISTS dbo.Steps;
CREATE TABLE Heights (rn TINYINT, cn TINYINT, val CHAR(1), Height TINYINT) AS NODE;
CREATE TABLE Steps AS EDGE;

WITH Lines AS (
	SELECT
		TRIM(value) AS line,
		CAST(LEN(TRIM(value)) AS INT) AS line_len,
		ordinal AS rn
	FROM STRING_SPLIT(REPLACE(@input, CHAR(0x0d), ''), CHAR(0xA), 1) AS x -- work w/CR and CRLF 
),
Vals AS (
	SELECT
		lines.rn,
		col.value AS cn,
		SUBSTRING(lines.line, col.value, 1) AS val
	FROM lines
	CROSS APPLY GENERATE_SERIES(1, line_len) AS col
)
INSERT INTO dbo.Heights (rn, cn, val, Height)
SELECT
	rn,
	cn,
	val,
	ASCII(CASE
			  WHEN val = 'S' COLLATE SQL_Latin1_General_CP1_CS_AS THEN
				  'a'
			  WHEN val = 'E' COLLATE SQL_Latin1_General_CP1_CS_AS THEN
				  'z'
			  ELSE
				  val
		  END
	) - ASCII('a') AS height
FROM Vals;

INSERT INTO dbo.Steps
SELECT
	h.$node_id, h_next.$node_id
FROM dbo.Heights AS h
INNER JOIN dbo.Heights AS h_next
	ON h_next.Height <= h.Height + 1
		AND ((h_next.rn = h.rn - 1 AND h_next.cn = h.cn)
				OR (h_next.rn = h.rn + 1 AND h_next.cn = h.cn)
				OR (h_next.rn = h.rn AND h_next.cn = h.cn - 1)
				OR (h_next.rn = h.rn AND h_next.cn = h.cn + 1)
		);


SELECT levels AS part1 FROM(
SELECT
		h1.val AS StartNode,
		LAST_VALUE(h2.val) WITHIN GROUP (GRAPH PATH) AS EndNode,
		COUNT(h2.val) WITHIN GROUP (GRAPH PATH) AS levels
	FROM
		Heights AS h1,
		steps FOR PATH AS step,
		heights FOR PATH  AS h2
	WHERE MATCH(SHORTEST_PATH(h1(-(step)->h2)+))
	AND h1.val = 'S' COLLATE SQL_Latin1_General_CP1_CS_AS) AS Paths
WHERE EndNode = 'E' COLLATE SQL_Latin1_General_CP1_CS_AS;


SELECT MIN(levels) AS part2 FROM(
SELECT
		h1.val AS StartNode,
		LAST_VALUE(h2.val) WITHIN GROUP (GRAPH PATH) AS EndNode,
		COUNT(h2.val) WITHIN GROUP (GRAPH PATH) AS levels
	FROM
		Heights AS h1,
		steps FOR PATH AS step,
		heights FOR PATH  AS h2
	WHERE MATCH(SHORTEST_PATH(h1(-(step)->h2)+))
	AND h1.height = 0) AS Paths
WHERE EndNode = 'E' COLLATE SQL_Latin1_General_CP1_CS_AS;
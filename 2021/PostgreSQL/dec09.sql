DROP TABLE IF EXISTS dec09;

CREATE TABLE dec09 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    line TEXT);
\COPY dec09 (line) FROM '../Python/09/input.txt';

VACUUM ANALYZE dec09;
CREATE INDEX ON dec09 (line_number);

\timing off 
\pset footer off 


WITH RECURSIVE nums as(
    SELECT 
        line_number as ri,
        idx as ci,
        val::int
    FROM dec09, LATERAL unnest(regexp_split_to_array(line, '')) WITH ordinality AS vals(val, idx)
), lows AS(
    SELECT
        rank() OVER (ORDER BY ri,ci) AS id,
        ri,
        ci,
        val,
        least(
            LEAD(val) OVER (PARTITION BY ri ORDER BY ci),
            LEAD(val) OVER (PARTITION BY ci ORDER BY ri),
            LAG(val) OVER (PARTITION BY ri ORDER BY ci),
            LAG(val) OVER (PARTITION BY ci ORDER BY ri)
        ) as min_neighbor
        FROM nums
), basins AS(
    SELECT
        id,
        ri,
        ci,
        val
    FROM lows
    WHERE val < min_neighbor
    UNION ALL /* add smaller neighbors */
    SELECT
        id,
        neighbor.ri,
        neighbor.ci,
        neighbor.val
    FROM basins
    INNER JOIN nums AS neighbor
        ON neighbor.val >= basins.val
        AND neighbor.val < 9
        AND (
            (basins.ri = neighbor.ri - 1 AND basins.ci = neighbor.ci)
            OR (basins.ri = neighbor.ri + 1 AND basins.ci = neighbor.ci)
            OR (basins.ri = neighbor.ri AND basins.ci = neighbor.ci - 1)
            OR (basins.ri = neighbor.ri AND basins.ci = neighbor.ci + 1)
        )

), top3 AS(
    SELECT size, row_number() OVER (ORDER BY size DESC) as rn
    FROM (
        SELECT id, COUNT(DISTINCT (ri, ci)) as size
        FROM basins
        GROUP BY id
        ORDER BY size DESC
        LIMIT 3) AS t3
)
SELECT 
(SELECT SUM(1 + val) as answer_1 FROM lows WHERE val < min_neighbor) AS answer_1,
(SELECT size FROM top3 WHERE rn=1) * (SELECT size FROM top3 WHERE rn=2) * (SELECT size FROM top3 WHERE rn=3) AS answer_2;

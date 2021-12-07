DROP TABLE IF EXISTS dec05;

CREATE TABLE dec05 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    line TEXT);

\COPY dec05 (line) FROM '../Python/05/input.txt';

VACUUM ANALYZE dec05;
CREATE INDEX ON dec05 (line_number);

\timing off 
\pset footer off 

WITH RECURSIVE parsed AS(
    SELECT
        line_number,
        split_part(split_part(line,' -> ',1),',',1)::int AS x0,
        split_part(split_part(line,' -> ',1),',',2)::int AS y0,
        split_part(split_part(line,' -> ',2),',',1)::int AS x1,
        split_part(split_part(line,' -> ',2),',',2)::int AS y1
    FROM dec05
), deltas as(
    SELECT
        *,
        CASE WHEN x1 > x0 THEN 1 WHEN x1 < x0 THEN -1 ELSE 0 END AS dx,
        CASE WHEN y1 > y0 THEN 1 WHEN y1 < y0 THEN -1 ELSE 0 END AS dy,
        CASE WHEN x0 != x1 AND y0 != y1 THEN 1 ELSE 0 END as is_diag /* is this a diagonal line */
    FROM parsed
), pixels AS(
    SELECT is_diag, dx,dy, x0 AS x, y0 AS y, x1, y1 /* starting pixel, endind pixel */
    FROM deltas
    UNION ALL
    SELECT is_diag, dx, dy, x + dx, y + dy, x1, y1
    FROM pixels
    WHERE x <> x1 OR y <> y1
), part1 AS(
    SELECT 1
    FROM pixels
    WHERE is_diag = 0
    GROUP BY x,y
    HAVING COUNT(*) > 1
), part2 AS(
    SELECT 1
    FROM pixels
    GROUP BY x,y
    HAVING COUNT(*) > 1
)
SELECT
    (SELECT COUNT(*) FROM part1) AS answer_1,
    (SELECT COUNT(*) FROM part2) AS answer_2
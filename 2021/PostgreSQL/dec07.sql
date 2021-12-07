DROP TABLE IF EXISTS dec07;

CREATE TABLE dec07 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    line TEXT);
\COPY dec07 (line) FROM '../Python/07/input.txt';

VACUUM ANALYZE dec07;
CREATE INDEX ON dec07 (line_number);

\timing off 
\pset footer off 

WITH nums as(
    SELECT num::int
    FROM dec07, LATERAL unnest(STRING_TO_ARRAY(line, ',')) WITH ordinality AS vals(num)
    WHERE line_number = 1
),
num_range AS(
    SELECT i
    FROM generate_series( (SELECT MIN(num) FROM nums), (SELECT MAX(num) FROM nums)) as s(i)
),
costs AS(
    SELECT 
        i as meeting_loc, 
        abs(num-i) as cost1, 
        abs(num-i) * (abs(num-i) + 1) / 2 as cost2
    FROM num_range, nums
), part1 AS(
    SELECT meeting_loc, sum(cost1) AS cost
    FROM costs
    GROUP BY meeting_loc
    order by cost
    LIMIT 1
), part2 AS(
    SELECT meeting_loc, sum(cost2) AS cost
    FROM costs
    GROUP BY meeting_loc
    order by cost
    LIMIT 1
)
SELECT 
    (SELECT cost FROM part1) AS answer_1,
    (SELECT cost FROM part2) AS answer_2
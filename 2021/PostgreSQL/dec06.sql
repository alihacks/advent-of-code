DROP TABLE IF EXISTS dec06;

CREATE TABLE dec06 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    line TEXT);
\COPY dec06 (line) FROM '../Python/06/input.txt';

VACUUM ANALYZE dec06;
CREATE INDEX ON dec06 (line_number);

\timing off 
\pset footer off 

/* Part 1 */
WITH RECURSIVE buckets AS(
    SELECT *
    FROM crosstab(
        $$
        WITH nums as(
        SELECT num::int
        FROM dec06, LATERAL unnest(STRING_TO_ARRAY(line, ',')) WITH ordinality AS vals(num) 
        WHERE line_number = 1
    )
    
      select '',num, COUNT(*) FROM nums GROUP BY num ORDER BY num
      $$, 
      $$ VALUES (0),(1),(2),(3),(4),(5),(6),(7),(8)
      $$
      ) AS ct(name text, f0 bigint, f1 bigint, f2 bigint, f3 bigint, f4 bigint, f5 bigint, f6 bigint, f7 bigint, f8 bigint)
), iter AS(
    SELECT 0 as i,
    COALESCE(f0,0) as f0,
    COALESCE(f1,0) as f1,
    COALESCE(f2,0) as f2,
    COALESCE(f3,0) as f3,
    COALESCE(f4,0) as f4,
    COALESCE(f5,0) as f5,
    COALESCE(f6,0) as f6,
    COALESCE(f7,0) as f7,
    COALESCE(f8,0) as f8
    FROM buckets
    UNION ALL
    SELECT 
        i + 1,
        f1 AS f0,
        f2 AS f1,
        f3 AS f2,
        f4 AS f3,
        f5 AS f4,
        f6 AS f5,
        f0 + f7 AS f6,
        F8 AS f7,
        f0 AS f8
    FROM iter
    WHERE i < 256
),
iter_counts AS(
    SELECT *, f0 + f1 + f2 + f3 + f4 + f5 + f6 + f7 + f8 as fish_count
    FROM iter
),
part1 AS(
    SELECT fish_count
    FROM iter_counts
    WHERE i <= 80
    order by i DESC
    LIMIT 1),
part2 AS(
    SELECT fish_count
    FROM iter_counts
    order by i DESC
    LIMIT 1)
SELECT 
    (SELECT fish_count FROM part1) AS answer_1,
    (SELECT fish_count FROM part2) AS answer_2
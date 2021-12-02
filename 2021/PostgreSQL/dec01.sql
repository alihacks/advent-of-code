DROP TABLE IF EXISTS dec01;
CREATE TABLE dec01 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    value bigint NOT NULL
);

\COPY dec01 (value) FROM '../Python/01/input.txt';
VACUUM ANALYZE dec01;

CREATE INDEX ON dec01 (value, line_number);

\timing off
\pset footer off

/* First Star */
WITH increases AS( 
    SELECT
        CASE WHEN value - LAG(value,1) OVER (ORDER BY line_number) > 0 
            THEN 1 
        END AS is_increase
    FROM dec01
)
SELECT SUM(is_increase) AS answer_1
FROM increases;

/* Second Star */

WITH triplesums AS(
    SELECT
        line_number,
        SUM(value) OVER (ORDER BY line_number ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS triplesum
    FROM dec01
), increases AS( 
    SELECT
        CASE WHEN triplesum - LAG(triplesum,1) OVER (ORDER BY line_number) > 0 
            THEN 1 
        END AS is_increase
    FROM triplesums
    where line_number > 3
)
SELECT SUM(is_increase) as answer_2
FROM increases;
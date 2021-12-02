DROP TABLE IF EXISTS dec02;

CREATE TABLE dec02 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    direction VARCHAR(10),
    value bigint NOT NULL);

\COPY dec02 (direction, value) FROM '../Python/02/input.txt' WITH DELIMITER ' ';

VACUUM ANALYZE dec02;
CREATE INDEX ON dec02 (value, line_number);

\timing off 
\pset footer off 

/* First Star */ 
SELECT
    -- Depth
    SUM(CASE direction 
        WHEN 'up' THEN value * -1
        WHEN 'down' THEN value 
    END) *
    -- horizontal
    SUM(CASE direction
        WHEN 'forward' THEN value
    END) as answer_1
    FROM dec02;

/* Second Star */
WITH deltas AS(
    SELECT 
        *,
        CASE direction
            WHEN 'up' THEN value * -1
            WHEN 'down' THEN value
        END AS aim_delta,
        CASE WHEN direction = 'forward' THEN value END AS h_delta
        
    FROM dec02
),
aims AS(
SELECT
    *, SUM(aim_delta) OVER(ORDER BY line_number ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as aim
FROM deltas
),
d_delta AS(
    SELECT *, CASE WHEN direction = 'forward' THEN aim * value END as d_delta
    FROM aims
)
SELECT SUM(d_delta) * SUM(h_delta) AS answer_2
FROM d_delta;
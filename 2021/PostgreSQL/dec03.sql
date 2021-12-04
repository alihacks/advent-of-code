DROP TABLE IF EXISTS dec03;

CREATE TABLE dec03 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    num VARCHAR(16));

\COPY dec03 (num) FROM '../Python/03/input.txt' WITH DELIMITER ' ';

VACUUM ANALYZE dec03;
CREATE INDEX ON dec03 (line_number);

\timing off 
\pset footer off 

/* Part 1 */
WITH vals AS(
    SELECT *
    FROM dec03, LATERAL unnest(string_to_array(num, NULL)) with ordinality as vals(val, idx)
), val_counts AS(SELECT idx, val, count(*) as val_count
FROM vals
GROUP BY idx, val),
ranks AS(
    SELECT idx, val, val_count,ROW_NUMBER() OVER (PARTITION BY idx ORDER BY val_count DESC) as rnk
    from val_counts
), gamma AS(
    SELECT string_agg(val,'' ORDER BY idx) as val FROM ranks where rnk=1
), epsilon AS(
    SELECT string_agg(val,'' ORDER BY idx) as val FROM ranks where rnk=2
)
SELECT (lpad(gamma.val,32,'0')::bit(32))::integer * (lpad(epsilon.val,32,'0')::bit(32))::integer AS answer_1
FROM gamma, epsilon;

/* Part 2 */
WITH RECURSIVE
vals AS(
        SELECT num, (lpad(num,32,'0')::bit(32))::integer as val, char_length(num) as len
        FROM dec03
    ),
o2 AS(
    SELECT len, 1 as idx, val, COUNT(*) OVER () as cnt
    FROM vals
    UNION ALL
    (WITH o2copy AS (TABLE o2)
    SELECT len, idx + 1, val, COUNT(*) OVER () as cnt
    FROM o2copy AS o
    WHERE val & (1 << (len - idx)) = (
        SELECT mode() WITHIN GROUP (ORDER BY o2copy.val & (1 << (o.len - o.idx)) DESC)
        FROM o2copy
    )
    and o.cnt > 1
    )
),co2 AS(
    SELECT len, 1 as idx, val, COUNT(*) OVER () as cnt
    FROM vals
    UNION ALL
    (WITH co2copy AS (TABLE co2)
    SELECT len, idx + 1, val, COUNT(*) OVER () as cnt
    FROM co2copy AS c
    WHERE val & (1 << (len - idx)) <> (
        SELECT mode() WITHIN GROUP (ORDER BY co2copy.val & (1 << (c.len - c.idx)) DESC)
        FROM co2copy
    )
    and c.cnt > 1
    
    )
)
SELECT o2.val * co2.val as answer_2
FROM co2, o2
WHERE co2.cnt = 1
AND o2.cnt = 1;
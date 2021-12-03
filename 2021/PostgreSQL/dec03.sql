DROP TABLE IF EXISTS dec03;

CREATE TABLE dec03 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    num VARCHAR(16));

\COPY dec03 (num) FROM '../Python/03/input.txt' WITH DELIMITER ' ';

VACUUM ANALYZE dec03;
CREATE INDEX ON dec03 (line_number);

\timing off 
\pset footer off 

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
SELECT (lpad(gamma.val,24,'0')::bit(24))::integer * (lpad(epsilon.val,24,'0')::bit(24))::integer AS answer_1
FROM gamma, epsilon;
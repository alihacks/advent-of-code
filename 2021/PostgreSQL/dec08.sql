DROP TABLE IF EXISTS dec08;

CREATE TABLE dec08 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    lpart TEXT,
    rpart TEXT);
\COPY dec08 (lpart, rpart) FROM '../Python/08/input.txt' WITH DELIMITER '|';

VACUUM ANALYZE dec08;
CREATE INDEX ON dec08 (line_number);

\timing off 
\pset footer off 

WITH lparts AS(
    SELECT
        line_number,
        regexp_split_to_array(part,'') AS part
    FROM dec08,
    LATERAL unnest(string_to_array(trim(lpart), ' ')) as part
), rparts AS(
    SELECT
        line_number,
        idx,
        regexp_split_to_array(part,'') AS part
    FROM dec08,
    LATERAL unnest(string_to_array(trim(rpart), ' ')) WITH ORDINALITY as p(part, idx)
), digits0 AS( /* easy 4 digits with unique segment counts */
    SELECT 
        line_number,
        part, 
        CASE cardinality(part)
            WHEN 2 THEN 1
            WHEN 4 THEN 4
            WHEN 3 THEN 7
            WHEN 7 THEN 8
        END as digit
    FROM lparts
    WHERE cardinality(part) IN (2,4,3,7)
), digits1 AS( /* next set of 3 digits that are all 6 segment */
    SELECT
        digits0.line_number,
        lparts.part,
        CASE COUNT(*) FILTER (WHERE lparts.part @> digits0.part)
            WHEN 0 THEN 6 /* 6 does not contain 1, 4 or 7 */ 
            WHEN 2 THEN 0 /* 0 contains 1 and 7 */
            WHEN 3 THEN 9 /* 9 contains 1,4,7 fully */
        END as digit
    FROM digits0
    INNER JOIN lparts
        ON digits0.line_number = lparts.line_number
    WHERE cardinality(lparts.part) = 6
    AND cardinality(digits0.part) <> 8
    GROUP BY 
        digits0.line_number,
        lparts.part
), digits2 AS ( /* remaining 3 digits: 3, 5, 2, all are 5 segment. */
    SELECT 
        lparts.line_number,
        lparts.part,
        CASE
            WHEN lparts.part @> num1.part THEN 3 /* only 3 contains all of 1 */
            WHEN lparts.part || num1.part @> num9.part THEN 5 /* if you add segments of 5 and 1 that's a 9 */
            ELSE 2 /* we're done!! */
        END AS digit
    FROM lparts
    INNER JOIN digits1 AS num9
        ON lparts.line_number = num9.line_number
        AND num9.digit = 9
    INNER JOIN digits0 as num1
        ON lparts.line_number = num1.line_number
        AND num1.digit = 1
    WHERE cardinality(lparts.part) = 5
), all_digits AS(
    SELECT line_number, part, digit FROM digits0 UNION ALL
    SELECT line_number, part, digit FROM digits1 UNION ALL
    SELECT line_number, part, digit FROM digits2
),
line_values AS(
    SELECT rparts.line_number, STRING_AGG(digit::text,'' ORDER BY idx)::int lineval
    FROM rparts
    INNER JOIN all_digits
        ON rparts.line_number = all_digits.line_number
        AND rparts.part @> all_digits.part AND all_digits.part @> rparts.part
    GROUP BY rparts.line_number
)
SELECT
    (SELECT COUNT(*) FROM rparts WHERE cardinality(rparts.part) IN(2,4,3,7)) AS answer_1,
    (SELECT SUM(lineval) FROM line_values) as answer_2;
DROP TABLE IF EXISTS dec04;

CREATE TABLE dec04 (
    line_number bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    line TEXT);

\COPY dec04 (line) FROM '../Python/04/input.txt';

VACUUM ANALYZE dec04;
CREATE INDEX ON dec04 (line_number);

\timing off 
\pset footer off 

/* Part 1 */
WITH nums as(
    SELECT idx, num
    FROM dec04, LATERAL unnest(STRING_TO_ARRAY(line, ',')) WITH ordinality AS vals(num, idx) 
    WHERE line_number = 1
),
num_lists AS(
    SELECT idx, array_agg(num) OVER (ORDER BY idx) as nums
    FROM nums
),
windex(i1,i2,i3,i4, i5) as( /* win indexes represents bingo rows or cols 8 */
    SELECT 1,2,3,4,5
    UNION ALL SELECT 6,7,8,9,10
    UNION ALL SELECT 11,12,13,14,15
    UNION ALL SELECT 16,17,18,19,20
    UNION ALL SELECT 21,22,23,24,25
    UNION ALL SELECT 1,6,11,16,21
    UNION ALL SELECT 2,7,12,17,22
    UNION ALL SELECT 3,8,13,18,23
    UNION ALL SELECT 4,9,14,19,24
    UNION ALL SELECT 5,10,15,20,25
),
boards AS(
    SELECT 
        STRING_TO_ARRAY(
            TRIM(STRING_AGG(REPLACE(TRIM(line),'  ',' '), ' ' ORDER BY line_number)), ' '
        ) AS board,
        MIN((line_number - 3) / 6) as board_no
    FROM dec04
    WHERE line_number > 1
    GROUP BY (line_number - 3) / 6 /* 6 since we have empty line first */
),
board_wins AS(
SELECT board_no,board, array[board[i1], board[i2], board[i3], board[i4], board[i5]] as win
FROM boards, windex),
win_orders AS(
SELECT 
    board_no,
    board,
    MIN(idx) as win_order
FROM board_wins, num_lists
WHERE num_lists.nums @> board_wins.win
group by board_no, board
),
winners as(
    (SELECT 'part1' as part, board, nums
    FROM win_orders
    INNER JOIN num_lists on win_orders.win_order =  num_lists.idx
    order by win_order
    LIMIT 1)
    UNION ALL
    (SELECT 'part2' as part, board, nums
    FROM win_orders
    INNER JOIN num_lists on win_orders.win_order =  num_lists.idx
    order by win_order DESC
    LIMIT 1)
)
SELECT part, board_sum * nums[cardinality(nums)]::int as answer
FROM winners,
LATERAL (SELECT sum(val::int) as board_sum
        FROM unnest(board) AS b(val)
        WHERE val <> ALL (nums)) sums
GROUP BY part, board_sum, nums
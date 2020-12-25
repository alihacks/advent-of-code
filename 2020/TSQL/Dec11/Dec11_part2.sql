DECLARE
	@r INT = 10,
	@c INT = 10,
	@str VARCHAR(MAX),
	@nextstr VARCHAR(MAX) = ''
SELECT
	@str = Input,
	@r	= Rc,
	@c	= Cols
FROM dbo.Dec11Input;
DROP TABLE IF EXISTS #seats;
CREATE TABLE #seats (n INT, rown INT, coln INT, SeatVal VARCHAR(8), INDEX ix1 CLUSTERED(rown,coln));


WHILE 1 = 1 BEGIN
	DELETE #seats;

	WITH SmallNums AS (
		SELECT nums.num
		FROM (VALUES (1), (1), (1), (1), (1), (1), (1), (1), (1), (1)) AS nums (num)
	),
	Numbers AS (
		SELECT ROW_NUMBER() OVER (ORDER BY N1.num) AS n
		FROM SmallNums AS N1
		CROSS JOIN SmallNums AS N2
		CROSS JOIN SmallNums AS N3
		CROSS JOIN SmallNums AS N4
	),
	NumRowCol AS (
		SELECT
			Numbers.n,
			(Numbers.n - 1) % @c + 1 AS ColN,
			(Numbers.n - 1) / @c + 1 AS RowN
		FROM Numbers
		WHERE Numbers.n <= @r * @c
	),
	Seats AS (SELECT *, SUBSTRING(@str, NumRowCol.n, 1) AS SeatVal FROM NumRowCol)
	INSERT #seats(n, rown, coln, SeatVal) SELECT n, rown, coln, Seats.SeatVal FROM Seats;

	--SELECT * FROM #seats;
	/*
	WITH SmallNums AS (
		SELECT nums.num
		FROM (VALUES (1), (1), (1), (1), (1), (1), (1), (1), (1), (1)) AS nums (num)
	),
	Numbers AS (
		SELECT ROW_NUMBER() OVER (ORDER BY N1.num) AS n
		FROM SmallNums AS N1
		CROSS JOIN SmallNums AS N2
		CROSS JOIN SmallNums AS N3
		CROSS JOIN SmallNums AS N4
	),
	NumRowCol AS (
		SELECT
			Numbers.n,
			(Numbers.n - 1) % @c + 1 AS ColN,
			(Numbers.n - 1) / @c + 1 AS RowN
		FROM Numbers
		WHERE Numbers.n <= @r * @c
	),
	Seats AS (SELECT *, SUBSTRING(@str, NumRowCol.n, 1) AS SeatVal FROM NumRowCol),*/
	WITH Seats AS (SELECT * FROM #seats),
	VisibleNeighbors AS (
		SELECT
			*,
			(
				SELECT TOP 1 S2.SeatVal
				FROM seats AS S2
				WHERE
					S1.ColN - S2.ColN = S1.RowN - S2.RowN
					AND S2.ColN < S1.ColN
					AND S2.RowN < S1.RowN
					AND S2.SeatVal <> '.'
				ORDER BY ColN DESC
			) AS SeatA,
			(
				SELECT TOP 1 S2.SeatVal
				FROM seats AS S2
				WHERE
					S2.ColN = S1.ColN
					AND S2.RowN < S1.RowN
					AND S2.SeatVal <> '.'
				ORDER BY RowN DESC
			) AS SeatB,
			(
				SELECT TOP 1 S2.SeatVal
				FROM seats AS S2
				WHERE
					S2.ColN - S1.ColN = S1.RowN - S2.RowN
					AND S2.ColN > S1.ColN
					AND S2.RowN < S1.RowN
					AND S2.SeatVal <> '.'
				ORDER BY ColN ASC
			) AS SeatC,
			(
				SELECT TOP 1 S2.SeatVal
				FROM seats AS S2
				WHERE
					S2.RowN = S1.RowN
					AND S2.ColN < S1.ColN
					AND S2.SeatVal <> '.'
				ORDER BY ColN DESC
			) AS SeatD,
			(
				SELECT TOP 1 S2.SeatVal
				FROM seats AS S2
				WHERE
					S2.RowN = S1.RowN
					AND S2.ColN > S1.ColN
					AND S2.SeatVal <> '.'
				ORDER BY ColN ASC
			) AS SeatE,
			(
				SELECT TOP 1 S2.SeatVal
				FROM seats AS S2
				WHERE
					S1.ColN - S2.ColN = S2.RowN - S1.RowN
					AND S2.ColN < S1.ColN
					AND S2.RowN > S1.RowN
					AND S2.SeatVal <> '.'
				ORDER BY ColN DESC
			) AS SeatF,
			(
				SELECT TOP 1 S2.SeatVal
				FROM seats AS S2
				WHERE
					S2.ColN = S1.ColN
					AND S2.SeatVal <> '.'
					AND S2.RowN > S1.RowN
				ORDER BY RowN ASC
			) AS SeatG,
			(
				SELECT TOP 1 S2.SeatVal
				FROM seats AS S2
				WHERE
					S2.ColN - S1.ColN = S2.RowN - S1.RowN
					AND S2.ColN > S1.ColN
					AND S2.RowN > S1.RowN
					AND S2.SeatVal <> '.'
				ORDER BY RowN ASC
			) AS SeatH
		FROM seats AS S1
	)
	/*SELECT * FROM VisibleNeighbors */
	,
	NeighborCounts AS (
		SELECT
			*,
			CASE
				WHEN VisibleNeighbors.SeatVal IN ( '#', 'L' ) THEN
					IIF(VisibleNeighbors.SeatA = '#', 1, 0) + IIF(VisibleNeighbors.SeatB = '#', 1, 0) + IIF(VisibleNeighbors.SeatC = '#', 1, 0) + IIF(VisibleNeighbors.SeatD = '#', 1, 0) + IIF(VisibleNeighbors.SeatE = '#', 1, 0) + IIF(VisibleNeighbors.SeatF = '#', 1, 0) + IIF(VisibleNeighbors.SeatG = '#', 1, 0) + IIF(VisibleNeighbors.SeatG = '#', 1, 0)
			END AS NeighborCount
		FROM VisibleNeighbors
	),
	NextState AS (
		SELECT
			*,
			CASE
				WHEN NeighborCounts.SeatVal = 'L'
					AND NeighborCounts.NeighborCount = 0 THEN
					'#'
				WHEN NeighborCounts.SeatVal = '#'
					AND NeighborCounts.NeighborCount >= 5 THEN
					'L'
				ELSE
					NeighborCounts.SeatVal
			END AS NewVal
		FROM NeighborCounts
	)
	SELECT @nextstr += NextState.NewVal
	FROM NextState
	ORDER BY NextState.n

	PRINT @str
	PRINT 'Loop'
	PRINT @nextstr
	IF (@nextstr = @str) BEGIN
		BREAK
	END
	SELECT
		@str = @nextstr,
		@nextstr = ''
END
SELECT LEN(@str) - LEN(REPLACE(@str, '#', '')) AS Answer -- Number of #s

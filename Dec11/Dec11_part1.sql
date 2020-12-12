
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

WHILE 1 = 1 BEGIN

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
	/*
	Adjacent nodes
	a b c
	d _ e
	f g h
	*/
	Neighbors AS (
		SELECT
			*,
			IIF(NumRowCol.RowN > 1 AND NumRowCol.ColN > 1, NumRowCol.n - @c - 1, NULL) AS a,
			IIF(NumRowCol.RowN > 1, NumRowCol.n - @c, NULL) AS b,
			IIF(NumRowCol.RowN > 1 AND NumRowCol.ColN < @c, NumRowCol.n - @c + 1, NULL) AS c, --
			IIF(NumRowCol.ColN > 1, NumRowCol.n - 1, NULL) AS d,
			IIF(NumRowCol.ColN < @c, NumRowCol.n + 1, NULL) AS e,
			IIF(NumRowCol.RowN < @r AND NumRowCol.ColN > 1, NumRowCol.n + @c - 1, NULL) AS f,
			IIF(NumRowCol.RowN < @r, NumRowCol.n + @c, NULL) AS g,
			IIF(NumRowCol.RowN < @r AND NumRowCol.ColN < @c, NumRowCol.n + @c + 1, NULL) AS h
		FROM NumRowCol
	),
	NeighborValues AS (
		SELECT
			SUBSTRING(@str, Neighbors.n, 1) AS nv,
			SUBSTRING(@str, Neighbors.a, 1) AS av,
			SUBSTRING(@str, Neighbors.b, 1) AS bv,
			SUBSTRING(@str, Neighbors.c, 1) AS cv,
			SUBSTRING(@str, Neighbors.d, 1) AS dv,
			SUBSTRING(@str, Neighbors.e, 1) AS ev,
			SUBSTRING(@str, Neighbors.f, 1) AS fv,
			SUBSTRING(@str, Neighbors.g, 1) AS gv,
			SUBSTRING(@str, Neighbors.h, 1) AS hv,
			*
		FROM Neighbors
	),
	NeighborCounts AS (
		SELECT
			*,
			IIF(NeighborValues.av = '#', 1, 0) + IIF(NeighborValues.bv = '#', 1, 0) + IIF(NeighborValues.cv = '#', 1, 0) + IIF(NeighborValues.dv = '#', 1, 0) + IIF(NeighborValues.ev = '#', 1, 0) + IIF(NeighborValues.fv = '#', 1, 0) + IIF(NeighborValues.gv = '#', 1, 0) + IIF(NeighborValues.hv = '#', 1, 0) AS NeighborCount
		FROM NeighborValues
	),
	NextState AS (
		SELECT
			*,
			CASE
				WHEN NeighborCounts.nv = 'L'
					AND NeighborCounts.NeighborCount = 0 THEN
					'#'
				WHEN NeighborCounts.nv = '#'
					AND NeighborCounts.NeighborCount >= 4 THEN
					'L'
				ELSE
					NeighborCounts.nv
			END AS NewVal
		FROM NeighborCounts
	)
	SELECT @nextstr += NextState.NewVal
	FROM NextState
	ORDER BY NextState.n

	PRINT 'Loop'
	PRINT @nextstr
	IF (@nextstr = @str) BEGIN
		BREAK
	END
	SELECT @str = @nextstr, @nextstr = ''
END
SELECT LEN(@str) - LEN(REPLACE(@str,'#','')) AS Answer -- Number of #s
USE tempdb
GO
-- Don't forget to create input first
-- Forget Set based, it'll never end This is terribly slow let's do it this way
DECLARE
	@InputIndex INT = 1,
	@InputVal INT,
	@Answer BIGINT = 1,
	@lcm BIGINT = 1
-- For each bus
WHILE @InputIndex IS NOT NULL BEGIN

	SELECT @InputVal = CAST(InputVal AS INT)
	FROM Dec13Input
	WHERE
		InputVal <> 'x'
		AND InputIndex = @InputIndex
	
	-- Make current bus work (-1 for 1 based index)
	WHILE (@Answer + @InputIndex - 1) % @InputVal <> 0 BEGIN
		SELECT @Answer += @lcm
	END

	SELECT @lcm *= @InputVal

	SELECT @InputIndex = MIN(InputIndex)
	FROM Dec13Input
	WHERE
		InputVal <> 'x'
		AND InputIndex > @InputIndex
END

SELECT @Answer AS Answer

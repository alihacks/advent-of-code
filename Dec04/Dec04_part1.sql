-- Run input.sql first to setup input. This can be inlined but moved to a single file to keep code cleaner
-- both files can be run in tempdb
WITH Passports AS (
	SELECT value AS PassportText
	FROM STRING_SPLIT(REPLACE(dbo.GetDec04Input(), CHAR(0xD) + CHAR(0xA) + CHAR(0xD) + CHAR(0xA), '^'), '^')
)
SELECT *
FROM Passports
WHERE Passports.PassportText LIKE '%byr:%'
AND Passports.PassportText LIKE '%iyr:%'
AND Passports.PassportText LIKE '%eyr:%'
AND Passports.PassportText LIKE '%hgt:%'
AND Passports.PassportText LIKE '%hcl:%'
AND Passports.PassportText LIKE '%ecl:%'
AND Passports.PassportText LIKE '%pid:%'
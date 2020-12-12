-- Run input.sql first to setup input. This can be inlined but moved to a single file to keep code cleaner
-- both files can be run in tempdb
WITH Passports AS (
	SELECT REPLACE(REPLACE(value, CHAR(0xD) + CHAR(0xA), ' '), '  ', ' ') + ' ' AS PassportText
	FROM STRING_SPLIT(REPLACE(dbo.GetDec04Input(), CHAR(0xD) + CHAR(0xA) + CHAR(0xD) + CHAR(0xA), '^'), '^')
),
CompletePassports AS (
	SELECT
		--ROW_NUMBER() OVER (ORDER BY Passports.PassportText) AS PassportId,
		Passports.PassportText
	FROM Passports
	WHERE
		Passports.PassportText LIKE '%byr:%'
		AND Passports.PassportText LIKE '%iyr:%'
		AND Passports.PassportText LIKE '%eyr:%'
		AND Passports.PassportText LIKE '%hgt:%'
		AND Passports.PassportText LIKE '%hcl:%'
		AND Passports.PassportText LIKE '%ecl:%'
		AND Passports.PassportText LIKE '%pid:%'
),
Fields AS (
	SELECT *
	FROM (
		VALUES ('byr:'),
			('iyr:'),
			('eyr:'),
			('hgt:'),
			('hcl:'),
			('ecl:'),
			('pid:')
	) AS a (fieldname)
),
ParsedPassports AS (
	SELECT
		P.PassportText,
		SUBSTRING(P.PassportText, CHARINDEX('byr:', P.PassportText) + 4, CHARINDEX(' ', P.PassportText, CHARINDEX('byr:', P.PassportText)) - CHARINDEX('byr:', P.PassportText) - 4) AS byr,
		SUBSTRING(P.PassportText, CHARINDEX('iyr:', P.PassportText) + 4, CHARINDEX(' ', P.PassportText, CHARINDEX('iyr:', P.PassportText)) - CHARINDEX('iyr:', P.PassportText) - 4) AS iyr,
		SUBSTRING(P.PassportText, CHARINDEX('eyr:', P.PassportText) + 4, CHARINDEX(' ', P.PassportText, CHARINDEX('eyr:', P.PassportText)) - CHARINDEX('eyr:', P.PassportText) - 4) AS eyr,
		SUBSTRING(P.PassportText, CHARINDEX('hgt:', P.PassportText) + 4, CHARINDEX(' ', P.PassportText, CHARINDEX('hgt:', P.PassportText)) - CHARINDEX('hgt:', P.PassportText) - 4) AS hgt,
		SUBSTRING(P.PassportText, CHARINDEX('hcl:', P.PassportText) + 4, CHARINDEX(' ', P.PassportText, CHARINDEX('hcl:', P.PassportText)) - CHARINDEX('hcl:', P.PassportText) - 4) AS hcl,
		SUBSTRING(P.PassportText, CHARINDEX('ecl:', P.PassportText) + 4, CHARINDEX(' ', P.PassportText, CHARINDEX('ecl:', P.PassportText)) - CHARINDEX('ecl:', P.PassportText) - 4) AS ecl,
		SUBSTRING(P.PassportText, CHARINDEX('pid:', P.PassportText) + 4, CHARINDEX(' ', P.PassportText, CHARINDEX('pid:', P.PassportText)) - CHARINDEX('pid:', P.PassportText) - 4) AS pid
	FROM CompletePassports AS P
)
SELECT
	*
FROM ParsedPassports
WHERE
	1 = 1
	--byr (Birth Year) - four digits; at least 1920 and at most 2002.
	AND ParsedPassports.byr BETWEEN '1920' AND '2002'
	--iyr (Issue Year) - four digits; at least 2010 and at most 2020.
	AND ParsedPassports.iyr BETWEEN '2010' AND '2020'
	--eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
	AND ParsedPassports.eyr BETWEEN '2020' AND '2030'
	--hgt (Height) - a number followed by either cm or in:
	AND 1 = CASE
				--If cm, the number must be at least 150 and at most 193.
				WHEN RIGHT(ParsedPassports.hgt, 2) = 'cm' THEN
					IIF(LEFT(ParsedPassports.hgt, LEN(ParsedPassports.hgt) - 2) BETWEEN '150' AND '193', 1, 0)
				--If in, the number must be at least 59 and at most 76.
				WHEN RIGHT(ParsedPassports.hgt, 2) = 'in' THEN
					IIF(LEFT(ParsedPassports.hgt, LEN(ParsedPassports.hgt) - 2) BETWEEN '59' AND '76', 1, 0)
			END
	--hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
	AND ParsedPassports.hcl LIKE '#' + REPLICATE('[0-9a-f]', 6)
	--ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
	AND ParsedPassports.ecl IN ( 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth' )
	--pid (Passport ID) - a nine-digit number, including leading zeroes.
	AND ParsedPassports.pid LIKE REPLICATE('[0-9]', 9)

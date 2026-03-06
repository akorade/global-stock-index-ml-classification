-- Data Analysis : Missing Trading Days identification

WITH RECURSIVE DateSequence(date) AS (
    -- Start date (anchor member)
    SELECT date('2003-01-09')
    UNION ALL
    -- Recursive member: add one day until the end date is reached
    SELECT date(date, '+1 day')
    FROM DateSequence
    WHERE date < '2021-05-29' -- End date condition
)
-- Select all dates from the sequence
--SELECT date FROM DateSequence;

--SELECT min(date), max(date) FROM DateSequence;


SELECT
    ds.date,
    IFNULL(t.date, 0) AS filled_value -- Replace NULL with 0
FROM
    DateSequence ds
LEFT JOIN
    indexProcessed t ON ds.date = date(t.date)
	where IFNULL(t.date, 0)  =0
ORDER BY
    ds.date;
	
/*	
Result: Identified no volume on weekends and New year days
Data set is clean and no irregularities or irregular patterns found
*/

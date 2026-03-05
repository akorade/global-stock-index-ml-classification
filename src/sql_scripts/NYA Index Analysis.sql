/* Processed file
 Same data as indexData.csv but with null values removed and an extra column for closing prices in terms of USD */

SELECT distinct IndexName from indexProcessed;
-- IndexName
-- HSI
-- NYA
-- IXIC
-- 000001.SS
-- N225
-- N100
-- 399001.SZ
-- GSPTSE
-- NSEI
-- GDAXI
-- SSMI
-- TWII
-- J203.JO


/* Index Name Records */
SELECT  IndexName,count(*) from indexProcessed 
group by IndexName
order by 2 DESC
-- IndexName	count(*)
-- NYA	13947
-- N225	13874
-- IXIC	12690
-- GSPTSE	10526
-- HSI	8492
-- GDAXI	8438
-- SSMI	7671
-- TWII	5869
-- 000001.SS	5791
-- 399001.SZ	5760
-- N100	5474
-- NSEI	3346
-- J203.JO	2346




/* For New York - identifying Non Zero Volume records */
SELECT  * from indexProcessed where IndexName='NYA'
AND Volume <>'0.0'
order by Volume ASC


/* Starting with Jan 3 2001, we have first time trading recorded for New York NYA index	*/
SELECT  min(date), max(date) from indexProcessed where IndexName='NYA'
AND Volume <>'0.0'
order by Volume ASC
--min(date)	max(date)
--2001-01-03	2021-05-28


/* For New York - identifying Min and Max Volume  traded  */
SELECT  min(Volume), max(Volume) from indexProcessed where IndexName='NYA'
-- min(Volume)	max(Volume)
-- 0.0	11456230000.0



/* For New York - identifying records with flat OHLC  */
SELECT * from indexProcessed where IndexName='NYA'
and Open=Close and High=Low
order by Date ASC

/* For New York - identifying flat OHC timeline  */
SELECT min(Date),max(Date) from indexProcessed where IndexName='NYA'
and Open=Close 
order by Date ASC
-- min(Date)	max(Date)
--1965-12-31	2003-01-08


-- Data Analysis
SELECT  *from indexProcessed where IndexName='NYA'
AND Date >=  '2015-01-01'  and Volume='0.0'
order by Volume ASC


-- Data Analysis for understanding flat OHLC
SELECT  *from indexProcessed where IndexName='NYA'
AND Date >=  '2001-01-01'  and Volume<>'0.0' and Open=High and Low=Close and High=Low
order by DATE ASC


-- Data Analysis : Reviewing 504 records with flat OHLC fand having traded Volume
SELECT  *from indexProcessed where IndexName='NYA'
AND Date >=  '2001-01-01'  and Volume<>'0.0'  and High=Low
order by DATE ASC


-- Data Analysis : Understanding timeline since year 2004 with records having 0 traded volume
SELECT  *from indexProcessed where IndexName='NYA'
AND Date >=  '2004-01-01'  and Volume='0.0'  
order by DATE ASC


-- Data Analysis : Reviewing flat OHLC records after  2004 with records
SELECT  *from indexProcessed where IndexName='NYA'
AND Date >=  '2004-01-01'   and High=Low
order by DATE ASC
-- zero volume with flat OHLC

-- Data Analysis : Reviewing flat OHLC records after Jan 8  2003 with records
SELECT  *from indexProcessed where IndexName='NYA'
AND Date >=  '2003-01-07'   and High=Low
order by DATE ASC
-- zero volume with flat OHLC since Jan 9 2003

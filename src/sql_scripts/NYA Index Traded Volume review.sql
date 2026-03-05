-- Identifying zero volume trading dates Min and Max dates
SELECT count(*) , min(Date), Max(Date)  from indexProcessed where IndexName='NYA'
AND Volume =0.0
-- count(*)	min(Date)	Max(Date)
-- 8832	1965-12-31	2018-12-06

/* Identifying date and timeline for traded volume Min and Max dates
 New York NYA index (NON ZERO VOLUME) Records */
SELECT count(*) , min(Date), Max(Date)  from indexProcessed where IndexName='NYA'
AND Volume <>0.0
/*
Total	Min Date	Max Date
5115	2001-01-03	2021-05-28
*/

/*
NYA Index Total Records	
Date timeline for traded volume */
SELECT  count(*) , min(Date), Max(Date)  from indexProcessed where IndexName='NYA'
-- count(*)	min(Date)	Max(Date)
-- 13947	1965-12-31	2021-05-28



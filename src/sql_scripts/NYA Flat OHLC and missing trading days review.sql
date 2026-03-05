-- Data Analysis
SELECT  count(*) , min(Date), Max(Date)  from indexProcessed where IndexName='NYA'
and date>= '2001-01-03' 
-- count(*)	min(Date)	Max(Date)
-- 5133	2001-01-03	2021-05-28


-- Since Jan 3 2001, we have 5133 records of which 5115 are non zero and 18 Zero Volume records
SELECT  count(*) , min(Date), Max(Date)  from indexProcessed where IndexName='NYA'
and date>= '2001-01-03'  and Volume <>0.0
-- count(*)	min(Date)	Max(Date)
-- 5115	2001-01-03	2021-05-28

-- Data Analysis: 18 Zero Volume records trading dates timeline
SELECT  count(*) , min(Date), Max(Date)  from indexProcessed where IndexName='NYA'
and date>= '2001-01-03'  and Volume = 0.0
-- count(*)	min(Date)	Max(Date)
-- 18	2006-06-23	2018-12-06


-- Data Analysis: 18 Zero Volume records Quick review
SELECT  *  from indexProcessed where IndexName='NYA'
and date>= '2001-01-03'  and Volume =0.0
order by date 
-- IndexName	Date	Open	High	Low	Close	Adj Close	Volume	CloseUSD
-- NYA	2006-06-23	7920.220215	7965.649902	7889.839844	7924.620117	7924.620117	0.0	7924.620117
-- NYA	2006-08-16	8296.030273	8362.820313	8296.030273	8357.400391	8357.400391	0.0	8357.400391
-- NYA	2006-12-19	9105.019531	9150.780273	9070.719727	9139.44043	9139.44043	0.0	9139.44043
-- NYA	2006-12-29	9172.759766	9176.780273	9133.200195	9139.019531	9139.019531	0.0	9139.019531
-- NYA	2007-01-04	9132.25	9132.25	9070.110352	9113.160156	9113.160156	0.0	9113.160156
-- NYA	2007-03-16	9005.339844	9052.269531	8966.759766	8983.009766	8983.009766	0.0	8983.009766
-- NYA	2007-03-20	9091.089844	9158.94043	9081.379883	9158.269531	9158.269531	0.0	9158.269531
-- NYA	2008-05-02	9395.080078	9496.349609	9395.080078	9451.169922	9451.169922	0.0	9451.169922
-- NYA	2009-12-04	7157.080078	7285.669922	7124.899902	7182.709961	7182.709961	0.0	7182.709961
-- NYA	2010-09-10	7034.370117	7075.609863	7034.370117	7067.509766	7067.509766	0.0	7067.509766
-- NYA	2010-12-22	7906.109863	7934.890137	7906.109863	7931.759766	7931.759766	0.0	7931.759766
-- NYA	2011-12-12	7502.879883	7502.879883	7308.540039	7363.490234	7363.490234	0.0	7363.490234
-- NYA	2012-06-01	7368.410156	7368.419922	7286.779785	7292.22998	7292.22998	0.0	7292.22998
-- NYA	2016-05-12	10375.87988	10399.9502	10283.48047	10334.37988	10334.37988	0.0	10334.37988
-- NYA	2017-05-01	11550.41016	11569.4502	11525.16016	11536.49023	11536.49023	0.0	11536.49023
-- NYA	2017-05-17	11522.96973	11530.51953	11422.58008	11423.53027	11423.53027	0.0	11423.53027
-- NYA	2017-06-01	11616.20996	11699.83008	11603.41016	11699.79004	11699.79004	0.0	11699.79004
-- NYA	2018-12-06	12032.49023	12144.5	11852.83008	12144.41016	12144.41016	0.0	12144.41016




-- Identifying flat OHLC dates timeline
SELECT min(date) ,max(date) from indexProcessed where IndexName='NYA'
and Open=Close and High=Low
order by Date ASC
-- min(date)	max(date)
-- 1965-12-31	2003-01-08

-- Reviewing 504 records  From Jan 3 2001 till Jan 8 2003							
SELECT count(*) ,  min(date) ,max(date) from indexProcessed where IndexName='NYA'
and date>= '2001-01-03'
and Open=Close and High=Low
order by Date ASC
-- count(*)	min(date)	max(date)
-- 504	2001-01-03	2003-01-08


-- Run down analysis for these ABOVE 504 RECORDS	 
SELECT * from indexProcessed where IndexName='NYA'
and date>= '2001-01-03'
and Open=Close and High=Low
order by Date ASC

-- Run down analysis for these ABOVE 504 RECORDS with Open=Close 
SELECT * from indexProcessed where IndexName='NYA'
and date>= '2001-01-03'
and Open=Close 
order by Date ASC

-- Run down analysis for these ABOVE 504 RECORDS with High=Low
SELECT * from indexProcessed where IndexName='NYA'
and date>= '2001-01-03'
and High=Low
order by Date ASC


--Run down analysis for records Above Jan 8, 2023 with Open=Close 
SELECT * from indexProcessed where IndexName='NYA'
and date>'2003-01-08'
and Open=Close 
order by Date ASC
-- No records


--Run down analysis for records Above Jan 8, 2023 with High=Low
SELECT * from indexProcessed where IndexName='NYA'
and date>'2003-01-08'
and High=Low
order by Date ASC
-- No records
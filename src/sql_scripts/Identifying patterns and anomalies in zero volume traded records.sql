-- Data Analysis: Identifying patterns in zero volume traded records after Jan 8 2003
SELECT * from indexProcessed where IndexName='NYA'
and date>'2003-01-08' and Volume=0.0
--and High=Low
order by date


-- Data Analysis: Mapping Weekday COLUMN to the trading date to identify anomalies 
SELECT 
IndexName,	Date, strftime('%w', Date) Day, substr('SunMonTueWedThuFriSat',strftime('%w',Date)*3+1,3) as Weekday,	Open,	High,	Low,	Close,	"Adj Close",	Volume,	CloseUSD 
from indexProcessed where IndexName='NYA'
and date>'2003-01-08'   
--and Volume=0.0
order by date

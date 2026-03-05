
-- Identifying correlation between traded volume with respect to open close and high low for the given day
SELECT *, open-Close, high-low FROM indexProcessed
where IndexName='NYA' and date>'2003-01-08'   
order by date 

SELECT *, open-Close, high-low FROM indexProcessed
where IndexName='NYA' and date>'2003-01-08'   
order by volume DESC 
SELECT 
	name 
FROM 
	sys.dm_exec_describe_first_result_set
	('SELECT  
TOP 50	* 
FROM future.MarketPrices mp 

LEFT JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId

LEFT JOIN future_ind.IchimokuSignal ich_sign ON mp.MarketPriceId = ich_sign.MarketPriceId WHERE mp.symbol = `BTCBUSD` ;', NULL, 0) ;
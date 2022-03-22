SELECT 
	* 
FROM future.MarketPrices mp 

LEFT JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId

LEFT JOIN future_ind.IchimokuSignal ich_sign ON mp.MarketPriceId = ich_sign.MarketPriceId 

WHERE mp.Symbol = 'BTCBUSD';
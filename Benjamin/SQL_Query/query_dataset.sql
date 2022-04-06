SELECT 
	* 
FROM future.MarketPrices mp 

LEFT OUTER JOIN future_ind.Ichimoku ich ON mp.MarketPriceId = ich.MarketPriceId

LEFT OUTER JOIN future_ind.IchimokuSignal ich_sign ON mp.MarketPriceId = ich_sign.MarketPriceId 

WHERE mp.Symbol = 'BTCBUSD' AND mp.Interval = '15m';

-- Doublon avec cette requete : ex MarketPriceId = 122/124/126 : Pas les mêmes valeurs pour les Ichimoku Signals
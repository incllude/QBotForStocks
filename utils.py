def catch_changes(portfolio_before, portfolio_after):
    
    wallet_before = portfolio_before.get_stock_list()
    wallet_after = portfolio_after.get_stock_list()
    
    wallet_merged = set(wallet_after + wallet_before)
    wallet_before = set(wallet_before)
    
    return list(wallet_merged - wallet_before)

def get_prices(portfolio, stocks):
    
    prices = []
    
    for stock in stocks:
        prices.append(portfolio.get_stock_price(stock))
        
    return prices

def get_actions(positions_normal, dataframes):

    timestamps = sorted(list(positions_normal.keys()))
    portfolio = positions_normal[timestamps[0]]
    market_actions = []

    for timestamp in timestamps[1:]:

        next_portfolio = positions_normal[timestamp]

        purchased_stocks = catch_changes(portfolio, next_portfolio)
        sold_stocks = catch_changes(next_portfolio, portfolio)

        purchased_prices = get_prices(next_portfolio, purchased_stocks)
        sold_prices = get_prices(next_portfolio, sold_stocks)

        purchased_stocks = [{'ticker': stock, 'price': price} for stock, price in zip(purchased_stocks, purchased_prices)]
        sold_stocks = [{'ticker': stock, 'price': price} for stock, price in zip(sold_stocks, sold_prices)]

        market_actions.append(
            {
                'timestamp': timestamp.to_pydatetime().date(),
                'bought': purchased_stocks,
                'sold': sold_stocks
            }
        )
        portfolio = next_portfolio
    
    return market_actions

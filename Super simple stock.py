#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import datetime,timedelta
import math

class Stockdata:
    def __init__(self,stock_symbol,stock_type,last_dividend,fixed_dividend,par_value):
        self.stock_symbol=stock_symbol
        self.stock_type=stock_type
        self.last_dividend=last_dividend
        self.fixed_dividend=fixed_dividend
        self.par_value=par_value
        self.trade=[]
        
    def calc_dividend_yield(self,price,stock_type=None):
        if stock_type is None:
            stock_type=input("Enter the stock type as Common or Preferred")
        if (stock_type=='Common' or stock_type=='common') and (self.stock_type=='Common' or self.stock_type=='common'):
            if price != 0:
                return self.last_dividend/price
            else:
                return 0
        elif(stock_type=='Preferred' or stock_type=='preferred') and (self.stock_type=='Preferred' or self.stock_type=='preferred'):
            if price !=0:
                return (self.fixed_dividend/100)*self.par_value/price
            else:
                return 0
        else:
            print("Invalid stock type .Please recheck and enter again")
            return None
        
    def calc_pe_ratio(self,price):
        if self.last_dividend !=0:
            return price/self.last_dividend
        else:
            return 0
        
    def trade_record(self,quantity,buy_or_sell,price):
        timestamp=datetime.now()
        trades={'timestamp': timestamp, 'quantity': quantity, 'buy_or_sell': buy_or_sell, 'price': price}
        self.trade.append(trades)
        
    def calc_volume_weighted_stock_price(self):
        current_time=datetime.now()
        diff_five_min=current_time-timedelta(minutes=5)
        obtained_trade=[i for i in self.trade if i['timestamp']>=diff_five_min]
        
        if not obtained_trade:  
            return 0
        
        total_price=0
        total_quantity=0
        for trade in obtained_trade:
            total_price=total_price+trade['price']*trade['quantity']
            total_quantity=total_quantity+trade['quantity']
        
        return total_price/total_quantity
    
    def display_trades(self):
        if not self.trade:
            print("No trades is recorded for this stock.")
            return

        print(f"Trades for {self.stock_symbol}:")
        for trades in self.trade:
            timestamp=trades['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            print(f"Timestamp:{timestamp},Quantity:{trades['quantity']},Buy/Sell:{trades['buy_or_sell']},Price:{trades['price']}")
        
    @classmethod
    def create_common_stock(clas,stock_symbol,last_dividend,par_value):
        return clas(stock_symbol,"Common", last_dividend, None, par_value)

    @classmethod
    def create_preferred_stock(clas,stock_symbol,last_dividend,fixed_dividend,par_value):
        return clas(stock_symbol,"Preferred", last_dividend, fixed_dividend, par_value)
    

class GBCE:
    def __init__(self):
        self.stocks=[]
    
    def add_stock(self,stock):
        self.stocks.append(stock)
    
    def calc_mean(self):
        stock_prices=[stock.calc_volume_weighted_stock_price() for stock in self.stocks]
        non_zero_prices=[price for price in stock_prices if price != 0]
        if not non_zero_prices:
            return 0
        product=math.prod(non_zero_prices)
        geometric_mean= product ** (1 / len(non_zero_prices))
        return geometric_mean
    
def display_menu():
    print("Menu:")
    print("1.Calculate Dividend Yield")
    print("2.Calculate P/E Ratio")
    print("3.Record a trade with details")
    print("4.Calculate Volume weighted Stock Price")
    print("5.Calculate GBCE All Share Index")
    print("6.Display Trade Details")
    print("7.Quit the task")
    

tea=Stockdata.create_common_stock("TEA", 0, 100)
pop=Stockdata.create_common_stock("POP", 8, 100)
ale=Stockdata.create_common_stock("ALE", 23, 60)
gin=Stockdata.create_preferred_stock("GIN", 8, 2, 100)
joe=Stockdata.create_common_stock("JOE", 13, 250)

gbce=GBCE()
gbce.add_stock(tea)
gbce.add_stock(pop)
gbce.add_stock(ale)
gbce.add_stock(gin)
gbce.add_stock(joe)


while True:
    display_menu()
    choice=int(input("Enter your choice from the options:"))
    
    if choice==1:
        stock_symbol=input("Enter the stock symbol:")
        price=float(input("Enter the stock price:"))
        stock=next((s for s in gbce.stocks if s.stock_symbol==stock_symbol),None)
        if stock:
            dividend_type=input("Enter 'Common' or 'Preferred' stock type (default is Common):")
            result=stock.calc_dividend_yield(price,dividend_type)
            if result is not None:
                print(f"Dividend Yield for {stock_symbol} ({dividend_type}):{result}")
        else:
            print(f"Stock {symbol} not found.")
        print("----------------------------------------------------------------------")
    
    elif choice==2:
        stock_symbol=input("Enter the stock symbol:")
        price=float(input("Enter the stock price:"))
        stock=next((s for s in gbce.stocks if s.stock_symbol==stock_symbol),None)
        if stock:
            pe_ratio=stock.calc_pe_ratio(price)
            print(f"P/E Ratio for {stock_symbol}:{pe_ratio}")
        else:
            print(f"Stock {stock_symbol} not found.")
            
        print("----------------------------------------------------------------------")
        
    elif choice==3:
        stock_symbol=input("Enter the stock symbol:")
        quantity=int(input("Enter the quantity:"))
        buy_or_sell=input("Enter 'buy' or 'sell':")
        price=float(input("Enter the trade price:"))
        stock=next((s for s in gbce.stocks if s.stock_symbol==stock_symbol),None)
        if stock:
            stock.trade_record(quantity,buy_or_sell,price)
            print("Trade recorded successfully.")
        else:
            print(f"Stock {stock_symbol} not found.")
            
        print("----------------------------------------------------------------------")
        
    elif choice==4:
        stock_symbol=input("Enter the stock symbol: ")
        stock=next((s for s in gbce.stocks if s.stock_symbol==stock_symbol),None)
        if stock:
            result=stock.calc_volume_weighted_stock_price()
            print(f"Volume Weighted Stock Price for {stock_symbol}:{result}")
        else:
            print(f"Stock {stock_symbol} not found.")
            
        print("----------------------------------------------------------------------")
        
    elif choice==5:
        gbce_index=gbce.calc_mean()
        print(f"GBCE All Share Index:{gbce_index}")
        
        print("----------------------------------------------------------------------")
        
    elif choice==6:
        stock_symbol=input("Enter the stock symbol to display trades: ")
        stock=next((s for s in gbce.stocks if s.stock_symbol==stock_symbol), None)
        if stock:
            stock.display_trades()
        else:
            print(f"Stock {stock_symbol} not found.")
            
        print("----------------------------------------------------------------------")
        
    elif choice==7:
        break
    
    else:
        print("Invalid choice enter a value option between 1-6")
        print("------------------------------------------------")
        
        

        

        
    
        
        
        
        

        
        
        
    

    
        
          


# In[ ]:





# In[ ]:





# In[ ]:





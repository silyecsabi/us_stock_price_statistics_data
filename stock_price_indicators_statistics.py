import pandas as pd
df = pd.read_csv('us_stock_historical_data.csv')


def query_for_a_day(on=False):
    # get datas for a day
    if on:
        print("Press enter to exit from the query!\nAvailable date range: [2017.08.08 ; 2022.08.05]\n")
        while True:
            year = input("Year: ")
            if year == "":
                break
            month = input("Month: ")
            if month == "":
                break
            day = input("Day: ")
            if day == "":
                break
            try:
                year, month, day = int(year), int(month), int(day)
            except ValueError:
                print("Invalid input!\n")
                continue
            query_idx = f"{year}-{month}-{day}"
            try:
                print(df.loc[query_idx])
            except KeyError:
                print("No data found on this day.")

            print()

df.drop('Volume', axis = 1, inplace = True)     # irrelevant column
df.rename(columns = {'Close/Last' : 'Close'}, inplace = True)

df.set_index('Date', inplace = True)
df.index = pd.to_datetime(df.index)

# Daily Maximum and Minimum values are the same as the 'High' and 'Low' for the day
df['Daily High'] = df['High']
df['Daily Low'] = df['Low']

# Weeks
df['Weekly High'] = df[['High']].resample('W-mon', closed = 'left').max().resample('d').ffill()
df['Weekly Low'] = df[['Low']].resample('W-mon', closed = 'left').min().resample('d').ffill()

# Months
df['Monthly High'] = df[['High']].resample('M', closed = 'left').max().resample('d').ffill()
df['Monthly Low'] = df[['Low']].resample('M', closed = 'left').max().resample('d').ffill()

# Quarters

df['Quarterly High'] = df[['High']].resample('Q', closed = 'left').max().resample('d').ffill()
df['Quarterly Low'] = df[['Low']].resample('Q', closed = 'left').max().resample('d').ffill()

# Form check

df.to_csv('us_stock_price_indicators_statistics.csv')
df.to_excel('us_stock_price_indicators_statistics.xlsx', sheet_name = 'Stock Price Statistics Data')

query_for_a_day(on = True)
import pandas as pd
import matplotlib.pyplot as plt

def check_week(index, mode):
    # collect all prices from the week
    week_prices = []

    for item in df.index:
        if item.year == index.year and item.week == index.week:
            if mode == 'max':
                week_prices.append(df.loc[item]['High'])
            elif mode == 'min':
                week_prices.append(df.loc[item]['Low'])
    if mode == 'max':
        return max(week_prices)
    elif mode == 'min':
        return min(week_prices)

def check_month(item, mode):
    # collect all prices from the month
    month_prices = []

    for index in df.index:
        if index.year == item.year and index.month == item.month:
            if mode == 'max':
                month_prices.append(df.loc[index]['High'])
            elif mode == 'min':
                month_prices.append(df.loc[index]['Low'])
    if mode == 'max':
        return max(month_prices)
    elif mode == 'min':
        return min(month_prices)

def check_quarter(item, mode):
    # collect all prices from the quarter
    quarter_prices = []

    for index in df.index:
        if index.year == item.year and index.quarter == item.quarter:
            if mode == 'max':
                quarter_prices.append(df.loc[index]['High'])
            elif mode == 'min':
                quarter_prices.append(df.loc[index]['Low'])
    if mode == 'max':
        return max(quarter_prices)
    elif mode == 'min':
        return min(quarter_prices)


def query_for_a_day(on = False):
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


df = pd.read_csv('us_stock_historical_data.csv')

df.drop('Volume', axis = 1, inplace = True)     # irrelevant column
df.rename(columns = {'Close/Last' : 'Close'}, inplace = True)
df.set_index('Date', inplace = True)
df.index = pd.to_datetime(df.index)

df.insert(loc = 4, column = 'Daily Max High', value = df['High'])
df.insert(loc = 5, column = 'Daily Min Low', value = df['Low'])

# WEEKLY VALUES

weekly_max = []
for item in df.index:
    for index in df.index:
        if index.year == item.year and index.month == item.month and index.day == item.day:
            if item.dayofweek == 4:
                weekly_max.append(check_week(index, mode = 'max'))
            else:
                weekly_max.append(None)     # not friday, will be backfilled

weekly_min = []
for item in df.index:
    for index in df.index:
        if index.year == item.year and index.month == item.month and index.day == item.day:
            if item.dayofweek == 4:
                weekly_min.append(check_week(index, mode = 'min'))
            else:
                weekly_min.append(None)     # not friday, will be backfilled

df.insert(loc = 6, column = 'Weekly Max High', value = weekly_max)
df.insert(loc = 7, column = 'Weekly Min Low', value = weekly_min)
df.fillna(method = 'bfill', inplace = True)     # backfill the NaN values, because it will be the same as the previous week, if it is not friday

# MONTHLY VALUES
# finding month leaps that are in the database

month_prices_max = []
for i in range (0, len(df.index) - 1):
    if df.index[i].month != df.index[i + 1].month:      # If true, there is a month leap
        month_prices_max.append(check_month(df.index[i + 1], mode = 'max'))
    else:
        month_prices_max.append(None)   # there is not, will be backfilled

month_prices_min = []
for i in range (0, len(df.index) - 1):
    if df.index[i].month != df.index[i + 1].month:
        month_prices_min.append(check_month(df.index[i + 1], mode = 'min'))
    else:
        month_prices_min.append(None)

# because the range run for len(df.index) - 1, and the last data is not any leap, so it is not important
month_prices_max.append(None)
month_prices_min.append(None)

# duplicate the first weekdays of the month for the previous month's last day

idx_of_not_none = []
for i in range (len(month_prices_max)):
    if month_prices_max[i] != None:
        idx_of_not_none.append(i)
for i in range (len(idx_of_not_none)):
    idx_of_not_none[i] =+ 1
for x in idx_of_not_none:
    month_prices_max[x] = month_prices_max[x - 1]
    month_prices_min[x] = month_prices_min[x - 1]

df.insert(loc = 8, column = 'Monthly Max High', value = month_prices_max)
df.insert(loc = 9, column = 'Monthy Min Low', value = month_prices_min)
df.fillna(method = 'bfill', inplace = True)     # backfill the same way as the weekly values


# QUARTER VALUES

quarter_prices_max = []
for i in range (0, len(df.index) - 1):
    if df.index[i].quarter != df.index[i + 1].quarter:      # there is a quarter leap
        quarter_prices_max.append(check_quarter(df.index[i + 1], mode = 'max'))
    else:
        quarter_prices_max.append(None)     # There is not, will be backfilled

quarter_prices_min = []
for i in range (0, len(df.index) - 1):
    if df.index[i].quarter != df.index[i + 1].quarter:
        quarter_prices_min.append(check_quarter(df.index[i + 1], mode = 'min'))
    else:
        quarter_prices_min.append(None)

# because the range run for len(df.index) - 1, and the last data is not any leap, so it is not important
quarter_prices_max.append(None)
quarter_prices_min.append(None)

# duplicate the first weekdays of the month for the previous month's last day
idx_of_not_none = []
for i in range (len(quarter_prices_max)):
    if quarter_prices_max[i] != None:
        idx_of_not_none.append(i)
for i in range (len(idx_of_not_none)):
    idx_of_not_none[i] += 1
for x in idx_of_not_none:
    quarter_prices_max[x] = quarter_prices_max[x - 1]
    quarter_prices_min[x] = quarter_prices_min[x - 1]

df.insert(loc = 10, column = 'Quarter Max', value = quarter_prices_max)
df.insert(loc = 11, column = 'Quarter Min', value = quarter_prices_min)
df.fillna(method = 'bfill', inplace = True)     # backfill the NaN values in the same way as the weekly and monthy values

df.to_csv('us_stock_price_statistics_data.csv')
df.to_excel('us_stock_price_statistics_data.xlsx', sheet_name = 'Stock Price Statistics Data')

# Query for daily statistics
query_for_a_day(on = True)

# plotting

x1 = df.index
y1 = df['Weekly Max High']
y2 = df['Quarter Max']

x2 = df.index[df.index.year == 2021]
y3 = df['Daily Max High'][df.index.year == 2021]
y4 = df['Daily Min Low'][df.index.year == 2021]

fig, ax = plt.subplots(1, 2, figsize = (20, 8))
ax[0].plot(x1, y1, color = 'g', label = 'Weekly Max High', linewidth = 1)
ax[0].plot(x1, y2, color = 'c', label = 'Quarter Max High', linewidth = 0.5, linestyle = '-.')

ax[0].set_xlabel('Years')
ax[0].set_ylabel('Prices')
ax[0].set_title('Weekly vs Quarter Maximum High')
ax[0].legend()


ax[1].plot(x2, y3, color = 'g', label = 'Daily Max High', linewidth = 1)
ax[1].plot(x2, y4, color = 'r', label = 'Daily Min Low', linewidth = 0.5)

ax[1].set_xlabel('Date')
ax[1].set_ylabel('Prices')
ax[1].set_title('Daily Maximum High vs Minimum Low in 2021')
ax[1].legend()

plt.show()

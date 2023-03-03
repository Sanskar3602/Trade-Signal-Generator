import pandas as pd

# Training Data Calculations

df = pd.read_csv('Train_data.csv')      # reading data from a file
df.columns = ['date', 'open', 'high' ,'low', 'close', 'volume']

# Calculating 10:30 movement
ten_thirty = []
no_of_days = int(len(df)/75)    # 75 candles of 5 min in one day
for day in range(no_of_days):
    temp = 0
    uptrend = 0         # green candle
    downtrend = 0       # red candle
    for candle in range(15):
        a = df.iloc[day*75+candle].open
        b = df.iloc[day*75+candle].close
        # if we are getting continuous uptrends, increase their value, same for downtrend
        if(a<b):
            if(uptrend):
                uptrend += 0.1
            else:
                uptrend=1
                downtrend = 0
        else:
            if(downtrend):
                downtrend += 0.1
            else:
                downtrend = 1
                uptrend = 0
        temp += (uptrend+downtrend)*(b-a)
    ten_thirty.append(temp)

# Calculating how much the market has gone from 10:30 to 3:30 in either upward 
# or downward direction
output = []
for day in range(no_of_days):
    reqd = df.iloc[day*75+73].close - df.iloc[day*75+14].open
    output.append(reqd)

# Calculating trends as upward, downward or cannot say(no trend)

# We assumed that if the day end price has gone more than 100 in upward 
# direction w.r.t 10:30 price, we will assume upward trend, same for downward 
# trend, and if it lies in between, we cannot say anything for sure. 
bar = 100
observed_trend = [] # array to store trends for everyday after 10:30am
for day in range(no_of_days):
    if(output[day]<(-bar)):
        observed_trend.append(0)           # downtrend
    elif(output[day]>bar):
        observed_trend.append(0.66)        # uptrend
    else:
        observed_trend.append(0.33)        # no trend


# Test Day Calculations


df1 = pd.read_csv('Test_data.csv')
df1.columns = ['date', 'open', 'high' ,'low', 'close', 'Adj cLose', 'volume']

test_total = 0
uptrend = 0
downtrend = 0
test_day_no = int(input("Choose any day between 0-6 to test the Neural Network:\n"))
for candle in range(test_day_no*75, test_day_no*75+15):
    a = df1.iloc[candle].open
    b = df1.iloc[candle].close
    if(a<b):
        if(uptrend):
            uptrend += 0.1
        else:
            uptrend=1
            downtrend = 0
    else:
        if(downtrend):
            downtrend += 0.1
        else:
            downtrend = 1
            uptrend = 0
    test_total += (uptrend+downtrend)*(b-a)
print("The value of the day is calculated as: %.2f" %test_total)
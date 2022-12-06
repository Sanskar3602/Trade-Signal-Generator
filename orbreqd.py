import pandas as pd

df = pd.read_csv('bn_2021_to_2022_sep.csv')
df.columns = ['date', 'open', 'high' ,'low', 'close', 'volume']

tenthirty = []
output = []
no_of_days = int(len(df)/75) #75 candles of 5 min = 1 day
for day in range(no_of_days):
    #calculating 10:30 movement
    total = 0
    for candle in range(15):
        pos = 0
        neg = 0
        a = df.iloc[day*75+candle].open
        b = df.iloc[day*75+candle].close
        if(a<b):
            if(pos):
                pos+=0.1
            else:
                pos+=1
                neg = 0
        else:
            if(neg):
                neg+=0.1
            else:
                neg += 1
                pos = 0
        total += (pos+neg)*(b-a)
    tenthirty.append(total)

for day in range(no_of_days):
    #calculating output
    reqd = df.iloc[day*75+73].close - df.iloc[day*75+14].open
    output.append(reqd)

ans = []
count0 = 0
count1 = 0
count2 = 0
bar = 100
for day in range(no_of_days):
    if(output[day]<(-bar)):
        ans.append(0)
        count2 += 1
    elif(output[day]>bar):
        ans.append(0.66)
        count1 += 1
    else:
        ans.append(0.33)
        count0 += 1

df1 = pd.read_csv('data.csv')
df1.columns = ['date', 'open', 'high' ,'low', 'close', 'Adj cLose', 'volume']

total = 0
for candle in range(15):
    pos = 0
    neg = 0
    a = df1.iloc[candle].open
    b = df1.iloc[candle].close
    if(a<b):
        if(pos):
            pos+=0.1
        else:
            pos+=1
            neg = 0
    else:
        if(neg):
            neg+=0.1
        else:
            neg += 1
            pos = 0
    total += (pos+neg)*(b-a)
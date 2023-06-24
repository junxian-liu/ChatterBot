from polygon import RESTClient
import numpy as np
import json
from typing import cast
from urllib3 import HTTPResponse
from chatterbot.conversation import Statement
import random

tickers = np.array([])

# Mean, max and min
def stats(ticker):
    API_KEY = 'Ao9fHerRTi5M9GteFUozhRdOasDXUXfN'
    client = RESTClient(API_KEY)
    aggs = cast(
        HTTPResponse,
        client.get_aggs(
            ticker, 
            1,
            'day', 
            '2022-05-20', 
            '2022-11-11', 
            raw = True
        )
    ) 
    data = json.loads(aggs.data)

    for item in data:
            if item == 'results':
                rawData = data[item]

    closingPrice = []
    for bar in rawData:
        for category in bar:
            if category == 'c':
                closingPrice.append(bar[category])

    lengthOfClosingPrice = len(closingPrice)
    sumOfClosingPrice = 0
    max = 0
    min = 999999
    for i in range(lengthOfClosingPrice):
        sumOfClosingPrice += closingPrice[i]
        if(closingPrice[i] > max):
            max = closingPrice[i]
        if(closingPrice[i] < min):
            min = closingPrice[i]
        
    mean = sumOfClosingPrice / lengthOfClosingPrice

    statistics = np.array([mean, max, min])
    return statistics

# Add new ticker to array to hold
def addTick(newTick):
    global tickers
    tickers = np.append(tickers, newTick)
    print(tickers)

# Obtain the array of tickers
def getTick():
    return tickers

# Comparisons
def comparisons(newTick, oldTick):
    oldTick = stats(oldTick)
    newTick = stats(newTick)
    growthOld = (oldTick[1] - oldTick[2]) / oldTick[2]
    growthNew = (newTick[1] - newTick[2]) / newTick[2]
    growth = growthNew - growthOld

    return growth

# Return statement
def getStatements(num):
    confidence = random.uniform(0, 1)
    if num == 0:
        tickStats = stats(tickers[-1])
        selected_statement = Statement(text = 'For the ticker ${}, the mean price was {}, the max price was {}, and the min price was {}'.format(tickers[-1], tickStats[0], tickStats[1], tickStats[2]))
        selected_statement.confidence = confidence
        return selected_statement
    else:
        growth = comparisons(tickers[-1], tickers[-2])
        selected_statement = Statement(text = 'The ticker ${} saw a potential growth of {} percent compared to the ticker ${}'.format(tickers[-1], growth, tickers[-2]))
        selected_statement.confidence = confidence
        return selected_statement
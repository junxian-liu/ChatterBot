#Generate responses regarding stock
from chatterbot.logic import LogicAdapter
from polygon import RESTClient
import random
import json
from typing import cast
from urllib3 import HTTPResponse

class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        s = 'stock'
        d = '$'
        if statement.text.startswith(d): 
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        # Randomly select a confidence between 0 and 1
        confidence = random.uniform(0, 1)

        # Make call to Polygon API
        API_KEY = 'Ao9fHerRTi5M9GteFUozhRdOasDXUXfN'
        client = RESTClient(API_KEY)
        aggs = cast(
            HTTPResponse, 
            client.get_aggs(
                'APPL', 
                1,
                'day', 
                '2022-05-20', 
                '2022-11-11', 
                raw = True
            )
        )

        data = json.loads(aggs.data)

        # Getting closing prices of stock
        for item in data:
            print('HI')
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
        # For this example, we will just return the input as output
        input_statement = "For the ticker $APPL, the mean price was {mean}, the max price was {max}, and the min price was {min}"
        selected_statement = input_statement.format(mean = mean, max = max, min = min)
        selected_statement.confidence = confidence

        return selected_statement
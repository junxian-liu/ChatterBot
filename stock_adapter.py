#Generate responses regarding stock
from chatterbot.logic import LogicAdapter
from polygon import RESTClient
import random
from comparison import getTick, addTick, getStatements

class MyLogicAdapter(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        s = 'stock'
        d = '$'
        if d in statement.text: 
            return True
        else:
            return False

    def process(self, input_statement, additional_response_selection_parameters):
        num = 0

        # Get ticker from input
        input = input_statement.text.split()
        for word in input:
            if word.startswith('$'):
                ticker = word[1:]
                if ticker not in getTick():
                    addTick(ticker)
        
        # Process input
        if "compare" in input:
            num = 1
        
        # For this example, we will just return the input as output
        selected_statement = getStatements(num)
        return selected_statement
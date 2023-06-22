# bot.py

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from cleaner import clean_corpus

CHAT = "chat.txt"

chatbot = ChatBot(
    "Junxian's Bot",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch"
        },
        {
            "import_path": "chatterbot.logic.MathematicalEvaluation"
        },
        {
            "import_path": "stock_adapter.MyLogicAdapter"
        }
    ]
)

#TRAINING
trainer = ListTrainer(chatbot)

trainer.train([
    "Hi",
    "Welcome, friend 🤗",
])
trainer.train([
    "How are you today?",
    "I am doing good, what about you?",
])

#CHAT
exit_conditions = (":q", "quit", "exit")
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print(f"Junxian's Bot: {chatbot.get_response(query)}")

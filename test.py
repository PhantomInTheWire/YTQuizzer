import json

with open("quiz.json", 'r') as file:
    questions = json.load(file)

for question in questions:
    print(question)

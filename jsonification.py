import json
import prompt
import transcriptor

def lists_of_lists_to_json(data, filename):
    questions_data = []
    for question_info in data:
        question = question_info[0]
        answer = question_info[1]
        wrong_answer1 = question_info[2]
        wrong_answer2 = question_info[3]
        questions_data.append({
            "question": question,
            "answer": answer,
            "wrong_answer1": wrong_answer1,
            "wrong_answer2": wrong_answer2
        })

    with open(filename, "w") as json_file:
        json.dump(questions_data, json_file, indent=4)
print(lists_of_lists_to_json(prompt.get_quiz(transcriptor.get_transcript("https://www.youtube.com/watch?v=b4DPj0XAfSg")), "quiz.json"))

import ast
import google.generativeai as genai
import os
import transcriptor


def string_to_list(s):
    return ast.literal_eval(s)


def get_quiz(transcript):

    genai.configure(api_key=os.environ("GOOGLE_API_KEY"))

    template = f""" You are a helpful assistant programmed to generate questions based on any text provided. For every 
    chunk of text you receive, you're tasked with designing 10 distinct questions. Each of these questions will be 
    accompanied by 3 possible answers: one correct answer and two incorrect ones.

    To ensure clarity and ease of processing, please structure your response in the following format, emulating a Python 
    list of lists:

    1. Create an outer list that contains 10 inner lists. 2. Each inner list represents a set of question and answers, 
    and should contain exactly 4 strings in the following order: - The generated question. - The correct answer. - The 
    first incorrect answer. - The second incorrect answer.

    Please ensure your output mirrors this structure:
    [
        ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2"],
        ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2"],
        ...
    ]
    Make sure that your output is in english even if prompted in hindi or any other language
    You must adhere to this format as it's optimized for further Python processing.
    """
    model = genai.GenerativeModel("gemini-pro")
    ans = (model.generate_content(template + transcript)).text
    return ans

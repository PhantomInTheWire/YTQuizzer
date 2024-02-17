from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
import ast

def string_to_list(s):
    return ast.literal_eval(s)

def get_quiz(transcript):
    openai_api_key = "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"

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
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    chain = LLMChain(
        llm=ChatOpenAI(openai_api_key=openai_api_key),
        prompt=chat_prompt,
    )
    return string_to_list(chain.run(transcript))

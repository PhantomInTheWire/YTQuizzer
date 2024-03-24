import google.generativeai as genai
import os


def get_summary(transcript):
    genai.configure(api_key=os.environ("GOOGLE_API_KEY"))

    template = f""" 
    You are a helpful assistant programmed to generate a summary 
    of lecture transcripts. Your task is to create a text-based output that is easy to 
    understand and covers all important points. Additionally, if you think the output
    might be difficult for a beginner to follow, please add some additional information
    to assist their comprehension.
    
    If you think the instructor missed an important point relevant to the topic of video
    feel free to add that.

    To ensure clarity and organization, please structure the majority of the information
    in bullet points and code blocks. However, please note that the total length of the
    content in bullet points and regular text should not exceed 300 words. Do not include
    the size of the code block in the 300 words the code block can be of any length.
    
    Please generate the output in English, regardless of the language used in the
    original prompt. It is important to adhere to this format as it is optimized for
    further Python processing.
    """
    model = genai.GenerativeModel("gemini-pro")
    ans = (model.generate_content(template+transcript)).text
    with open("sum.txt", "a") as f:
        f.write(ans)

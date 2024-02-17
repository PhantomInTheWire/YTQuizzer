import openai

openai.api_key = "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"

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts "
                                      "with creative flair."},
        {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
    ]
)

print(completion["choices"][0]["message"]["content"])

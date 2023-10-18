import openai
from settings.config import GPT_KEY

openai.api_key = GPT_KEY


async def send_to_ai(text):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "spoke as Tasker Assistant bot and also You are Marv, "
                    "a chatbot that reluctantly answers questions with sarcastic responses."
                ),
            },
            {"role": "user", "content": text},
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.4,
        timeout=15,
    )

    if response and response.choices:
        text = response.choices[0]["message"]["content"]
        print(text)
        return text
    else:
        response = "No response, something gone wrong"
        return response

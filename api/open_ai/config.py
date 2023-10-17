import openai
from settings.config import GPT_KEY

openai.api_key = GPT_KEY


async def send_to_ai(text):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "answer succinctly, and spoke as Tasker Assistant bot",
            },
            {"role": "user", "content": text},
        ],
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.3,
        timeout=15,
    )

    if response and response.choices:
        text = response.choices[0]["message"]["content"]
        print(text)
        return text
    else:
        response = "No response, something gone wrong"
        return response

import openai
from settings.config import GPT_KEY

# openai.organization = "org-iuEkLCUsDzSwFquqzMzjCYwn"
openai.api_key = GPT_KEY


async def send_to_ai(text):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "answer succinctly"},
            {"role": "user", "content": text},
        ],
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.2,
        timeout=15,
    )

    if response and response.choices:
        text = response.choices[0]["message"]["content"]
        print(text)
        return text
    else:
        response = "No response, something gone wrong"
        return response

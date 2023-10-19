import openai
from settings.config import GPT_KEY

openai.api_key = GPT_KEY


async def send_to_ai(
    question: str,
    previous_answer: str = None,
    previous_question: str = None,
) -> str:
    system_content = get_system_content(
        previous_answer=previous_answer,
        previous_question=previous_question,
    )
    response = await openai.ChatCompletion.acreate(
        model="gpt-4-0613",
        messages=[
            {
                "role": "system",
                "content": system_content,
            },
            {"role": "user", "content": question},
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.4,
        timeout=15,
    )

    if response and response.choices:
        text = response.choices[0]["message"]["content"]
        return text
    else:
        response = "No response, something gone wrong"
        return response


def get_system_content(
    previous_answer: str = None,
    previous_question: str = None,
) -> str:
    system_content = (
        f"You are Tasker assistant, a chatbot that reluctantly answers questions with sarcastic.",
    )
    if previous_answer is not None:
        system_content = (
            f"You are Tasker assistant, a chatbot that reluctantly answers questions with sarcastic. "
            f"my previous question:{previous_question}, "
            f"take this data into account"
        )

        if previous_question is not None:
            system_content = (
                f"You are Tasker assistant, a chatbot that reluctantly answers questions with sarcastic. "
                f"My previous question:{previous_question}, "
                f"your previous answer:{previous_answer}, "
                f"take this data into account"
            )
    return str(system_content)

import openai

from bot.admin.info import list_commands
from settings.config import GPT_KEY

openai.api_key = GPT_KEY


async def check_by_ai(text: str) -> str:
    commands = list_commands(default=True)
    clear_function_names = ",".join(commands)

    system_content = (
        "Answer with only one command from this names: "
        + clear_function_names
        + ". If not found send 404"
    )
    text = "Find a match in the following text: " + text

    command = await send(
        system_content=system_content,
        question=text,
    )
    command = command.choices[0]["message"]["content"]
    return command


async def send_to_ai(
    question: str,
    previous_answer: str = None,
    previous_question: str = None,
) -> str:
    system_content = get_system_content(
        previous_answer=previous_answer,
        previous_question=previous_question,
    )
    response = await send(system_content=system_content, question=question)

    if response and response.choices:
        text = response.choices[0]["message"]["content"]
        return text
    else:
        response = "No response, something gone wrong"
        return response


async def send(system_content: str, question: str):
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
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

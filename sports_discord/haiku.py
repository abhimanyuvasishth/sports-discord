from openai import OpenAI


def get_haiku(player_name):
    prompt = f"Generate a funny haiku about {player_name}, a cricket player."
    messages = [
        {'role': 'user', 'content': prompt},
    ]

    response = OpenAI().chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100
    )

    return response.choices[0].message.content

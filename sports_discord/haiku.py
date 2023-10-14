import openai


def get_haiku(player_name, api_key):
    prompt = f"Generate a funny haiku about {player_name}, a cricket player."

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        api_key=api_key
    )

    return response.choices[0].text

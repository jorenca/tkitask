from openai import OpenAI


def ask_gpt(prompt: str) -> str:
    client = OpenAI()
    prompt_messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            'role': 'user',
            'content': [
                { 'type': 'text', 'text': prompt }
            ]
        }
    ]

    response = client.chat.completions.create(
        messages=prompt_messages,
        model='gpt-4o-mini',
        response_format={'type': 'text'}
    )

    return response.choices[0].message.content
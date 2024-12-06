from openai import OpenAI
import os

# GPT API credentials
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()
client.api_key = OPENAI_API_KEY


def get_response(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    test_input = "Hello, how are you?"
    print("Testing GPT response...")
    print(get_response(test_input))

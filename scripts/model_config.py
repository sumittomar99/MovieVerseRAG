import openai


def get_openai_client(api_key):
    openai.api_key = api_key
    return openai

def generate_response(prompt, api_key):
    try:
        client = get_openai_client(api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a creative assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        generated_story = response.choices[0].message.content
        return generated_story, None
    except openai.AuthenticationError:
        return None, "The provided API key is invalid. Please check your API key and try again."
    except openai.RateLimitError:
        return None, "You have hit the rate limit for OpenAI API requests. Please wait and try again later."
    except openai.OpenAIError as e:
        return None, f"An OpenAI error occurred: {str(e)}"
    except Exception as e:
        return None, f"An unexpected error occurred: {str(e)}"
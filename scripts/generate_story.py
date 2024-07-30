from scripts.model_config import generate_response, get_openai_client
from scripts.prompt_generation import generate_prompts

def generate_mixed_story(user_story, movie_descriptions, openai_api_key):

    prompts = generate_prompts(user_story, movie_descriptions)

    combined_prompt = " ".join(prompts)
    system_prompt = """Your a great Movie script writer and Story writer. Your task is to generate well formulated and structured story with each details to support story. Make it readable to the users with different sections of the story. Use Markdown to make it appealing.
    Rules to follow:
    1. Title must be given
    2. Not necessarily the story should have converstaion
    """
    generated_story, error_message  = generate_response(system_prompt + combined_prompt, openai_api_key)
    
    return generated_story, error_message 

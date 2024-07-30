from scripts.model_config import generate_response, get_openai_client
from scripts.prompt_generation import generate_prompts

def generate_mixed_story(user_story, movie_descriptions, openai_api_key):

    prompts = generate_prompts(user_story, movie_descriptions)

    combined_prompt = " ".join(prompts)
    system_prompt = """Your a great Movie script writer and Story writer. Your task is to generate well formulated and structured story with each details to support story. Make it readable to the users with different sections of the story.
    Rules to follow:
    1. Title Name must be given with bold format and biggest in size,only title name should be there.
    2. Not necessarily the story should have converstaion.
    3. Generated story should be in story format, don't need to highlight everything.
    4. Don't highlight anything bold in the story content.

    Response generation should generated beautifully using Markdown code format
    """
    generated_story, error_message  = generate_response(system_prompt + combined_prompt, openai_api_key)
    
    return generated_story, error_message 

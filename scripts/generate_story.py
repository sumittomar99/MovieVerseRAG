from scripts.model_config import generate_response, get_openai_client
from scripts.prompt_generation import generate_prompts

def generate_mixed_story(user_story, movie_descriptions, openai_api_key):

    prompts = generate_prompts(user_story, movie_descriptions)

    combined_prompt = " ".join(prompts)
    generated_story, error_message  = generate_response(combined_prompt, openai_api_key)
    
    return generated_story, error_message 
import re
import spacy

def generate_prompts(user_story, movie_descriptions):
    prompts = []
    
    # Load spaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Function to replace character names
    def replace_character_names(description):
        doc = nlp(description)
        name_replacements = {}
        replaced_description = description
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                if ent.text not in name_replacements:
                    name_replacements[ent.text] = f"Character{len(name_replacements) + 1}"
        
        for original_name, new_name in name_replacements.items():
            replaced_description = replaced_description.replace(original_name, new_name)
        
        return replaced_description

    # Replace names in movie descriptions
    cleaned_descriptions = [replace_character_names(description) for description in movie_descriptions]

    # Basic prompt
    prompt_basic = f"User's story: {user_story}\n\nCombine this story with the following movie plots to create a new story:\n"
    for description in cleaned_descriptions:
        prompt_basic += f"\n- {description}"
    prompts.append(prompt_basic)

    # Prompt focusing on characters
    prompt_characters = f"User's story: {user_story}\n\nBlend the main characters from the following movie plots with the user's story to create an engaging narrative:\n"
    for description in cleaned_descriptions:
        prompt_characters += f"\n- {description}"
    prompts.append(prompt_characters)

    # Prompt focusing on setting
    prompt_setting = f"User's story: {user_story}\n\nIntegrate the settings from the following movie plots with the user's story to craft a vivid and immersive new tale:\n"
    for description in cleaned_descriptions:
        prompt_setting += f"\n- {description}"
    prompts.append(prompt_setting)

    # Prompt focusing on themes
    prompt_themes = f"User's story: {user_story}\n\nWeave the themes from the following movie plots with the user's story to create a compelling and cohesive narrative:\n"
    for description in cleaned_descriptions:
        prompt_themes += f"\n- {description}"
    prompts.append(prompt_themes)

    # Prompt focusing on plot twists
    prompt_plot_twists = f"User's story: {user_story}\n\nMerge the plot twists from the following movie plots with the user's story to craft a surprising and engaging new story:\n"
    for description in cleaned_descriptions:
        prompt_plot_twists += f"\n- {description}"
    prompts.append(prompt_plot_twists)

    # Prompt focusing on emotional depth
    prompt_emotional_depth = f"User's story: {user_story}\n\nWrite a heartwarming short story that blends the user's story with the emotional depth from the following movie plots:\n"
    for description in cleaned_descriptions:
        prompt_emotional_depth += f"\n- {description}"
    prompts.append(prompt_emotional_depth)

    # Prompt focusing on dialogue
    prompt_dialogue = f"User's story: {user_story}\n\nCreate a dialogue-driven narrative that combines the user's story with elements from the following movie plots:\n"
    for description in cleaned_descriptions:
        prompt_dialogue += f"\n- {description}"
    prompts.append(prompt_dialogue)

    # Prompt focusing on suspense
    prompt_suspense = f"User's story: {user_story}\n\nCraft a suspenseful story that integrates the user's story with the tension and suspense from the following movie plots:\n"
    for description in cleaned_descriptions:
        prompt_suspense += f"\n- {description}"
    prompts.append(prompt_suspense)

    # Prompt focusing on humor
    prompt_humor = f"User's story: {user_story}\n\nCombine the user's story with the humor and comedic elements from the following movie plots to create a funny and engaging narrative:\n"
    for description in cleaned_descriptions:
        prompt_humor += f"\n- {description}"
    prompts.append(prompt_humor)

    # Prompt focusing on fantasy
    prompt_fantasy = f"User's story: {user_story}\n\nMerge the user's story with the fantastical elements from the following movie plots to create a magical and imaginative tale:\n"
    for description in cleaned_descriptions:
        prompt_fantasy += f"\n- {description}"
    prompts.append(prompt_fantasy)

    # Prompt focusing on horror
    prompt_horror = f"User's story: {user_story}\n\nCreate a horror story that blends the user's story with the scary and eerie elements from the following movie plots:\n"
    for description in cleaned_descriptions:
        prompt_horror += f"\n- {description}"
    prompts.append(prompt_horror)

    # Additional prompts for Atmosphere and Emotional Depth
    prompt_atmosphere = f"User's story: {user_story}\n\nEnhance the atmosphere of the user's story by blending it with the mysterious and ambient elements from the following movie plots:\n"
    for description in cleaned_descriptions:
        prompt_atmosphere += f"\n- {description}"
    prompts.append(prompt_atmosphere)

    prompt_emotional_journeys = f"User's story: {user_story}\n\nWeave in the deep emotional journeys from the following movie plots to add layers of emotional depth to the user's story:\n"
    for description in cleaned_descriptions:
        prompt_emotional_journeys += f"\n- {description}"
    prompts.append(prompt_emotional_journeys)

    prompt_vivid_setting = f"User's story: {user_story}\n\nBlend the rich atmospheric settings and vivid descriptions from the following movie plots with the user's story to create a deeply immersive narrative:\n"
    for description in cleaned_descriptions:
        prompt_vivid_setting += f"\n- {description}"
    prompts.append(prompt_vivid_setting)

    prompt_emotional_connections = f"User's story: {user_story}\n\nMerge the profound emotional connections between characters from the following movie plots with the user's story to enhance its emotional resonance:\n"
    for description in cleaned_descriptions:
        prompt_emotional_connections += f"\n- {description}"
    prompts.append(prompt_emotional_connections)

    prompt_atmospheric_mood = f"User's story: {user_story}\n\nIncorporate atmospheric elements from the following movie plots to create a distinct mood that enhances the user's story:\n"
    for description in cleaned_descriptions:
        prompt_atmospheric_mood += f"\n- {description}"
    prompts.append(prompt_atmospheric_mood)

    prompt_emotional_climax = f"User's story: {user_story}\n\nBuild up to an emotional climax by integrating the intense emotional moments from the following movie plots with the user's story:\n"
    for description in cleaned_descriptions:
        prompt_emotional_climax += f"\n- {description}"
    prompts.append(prompt_emotional_climax)

    prompt_symbolic_atmosphere = f"User's story: {user_story}\n\nEnhance the atmosphere of the user's story by weaving in symbolic elements from the following movie plots:\n"
    for description in cleaned_descriptions:
        prompt_symbolic_atmosphere += f"\n- {description}"
    prompts.append(prompt_symbolic_atmosphere)

    return prompts

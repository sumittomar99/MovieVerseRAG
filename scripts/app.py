__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os
import sys


if not os.path.exists("chromadb_storage"):
    import scripts.insert_data as insert_data

print("Data has been inserted successfully !")

from scripts.query_data import query_data

# Streamlit app configuration
st.set_page_config(page_title="StoryWeaver AI", page_icon="✍️", layout="wide")

# Function to load CSS from a file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the custom CSS
load_css("./scripts/styles.css")

# Sidebar
with st.sidebar:
    st.header("Settings")
    openai_api_key = st.text_input("Enter your OpenAI API key:", type="password", key="api-key")

# Title and subtitle
st.markdown('<div class="title">StoryWeaver AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Craft unique stories by blending your ideas with captivating narratives</div>', unsafe_allow_html=True)

# Form for user input
with st.form(key='story_form'):
    user_story = st.text_area("Enter a short explanation about the story you have in mind (max 100 words)", max_chars=100)
    submit_button = st.form_submit_button(label='Search')

# Error message if inputs are missing
if submit_button:
    if not openai_api_key and not user_story:
        st.markdown('<div class="error-message"><p>Error: OpenAI API key and Story prompt both are required.</p></div>', unsafe_allow_html=True)
    elif not openai_api_key:
        st.markdown('<div class="error-message"><p>Error: OpenAI API key is required.</p></div>', unsafe_allow_html=True)
    elif not user_story:
        st.markdown('<div class="error-message"><p>Error: Story prompt is required.</p></div>', unsafe_allow_html=True)

    if user_story and openai_api_key:
        # Set explicit values for score and similarity_top_k
        min_score = 70
        similarity_top_k = 20

        # Construct filters based on explicit values
        filters = [{"key": "score", "operator": ">=", "value": min_score}]

        # Pass the OpenAI API key to the query_data function
        results, mixed_story, error_message = query_data("", filters, similarity_top_k, user_story, openai_api_key)

        # Display the generated mixed story
        if mixed_story:
            # Remove any potential sub-headings and newlines
            cleaned_story = mixed_story.replace("##", "").replace("**", "").replace("\n", " ").strip()
            st.markdown('<h2 class="results-header">Generated Story : </h2>', unsafe_allow_html=True)
             # Extract and format the title from the mixed story if it exists
            # if "Title:" in mixed_story:
            #     title_start = mixed_story.find("Title:") + len("Title:")
            #     title_end = mixed_story.find("\n", title_start)
            #     story_title = mixed_story[title_start:title_end].strip()
            #     story_title = story_title.replace("**","")
            #     mixed_story = mixed_story[:title_start - len("Title:")] + mixed_story[title_end:]
            #     st.markdown(f'<div class="story-title">{story_title}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="results-content">{mixed_story}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        elif error_message:
            st.markdown(f'<div class="error-message"><p>{error_message}</p></div>', unsafe_allow_html=True)

__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os
import sys


if not os.path.exists("chromadb_storage"):
    import scripts.insert_data as insert_data

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

    # Dropdown for selecting OpenAI models
    model_options = ["gpt-4o", "gpt-4o-mini"]
    selected_model = st.selectbox("Select OpenAI Model:", model_options)

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
        min_score = 70
        similarity_top_k = 20
    
        filters = [{"key": "score", "operator": ">=", "value": min_score}]
    
        results, mixed_story, error_message = query_data("", selected_model, filters, similarity_top_k, user_story, openai_api_key)
    
        st.markdown(mixed_story)
        if error_message:
            st.markdown(f'<div class="error-message"><p>{error_message}</p></div>', unsafe_allow_html=True)

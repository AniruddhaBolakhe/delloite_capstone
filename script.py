import streamlit as st
import google.generativeai as genai

# Configure Gemini API with your key
API_KEY = "AIzaSyC2MP2KLqImXqIiPhLeiaRqT3_oVhArFuI"
genai.configure(api_key=API_KEY)

# Select the correct model
MODEL_NAME = "gemini-1.5-pro"  
model = genai.GenerativeModel(MODEL_NAME)

def generate_script(topic, style):
    """Generates a well-structured YouTube script with an engaging format."""
    prompt = f"""
    Write a structured YouTube script for a video about '{topic}' in a '{style}' style. 
    The script should have the following sections:

    1. **Hook**: Start with an engaging hook to grab attention.
    2. **Intro**: Introduce the topic and what viewers will learn.
    3. **Main Content**: Provide engaging information in short, snappy sentences.
    4. **Engagement Prompt**: Ask viewers a question to encourage comments.
    5. **Call to Action (CTA)**: Encourage likes, subscribes, or further actions.
    
    The tone should match the chosen style. Format the script using Markdown for readability.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, 'text') else "No script generated."
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.title("Script Generator")
st.write("Generate structured and engaging scripts!")

# User input
topic = st.text_input("Enter your video topic:")
style = st.selectbox("Select script style:", ["Informative", "Casual", "Dramatic", "Humorous"])

if st.button("Generate Script"):
    if topic:
        with st.spinner("Generating script..."):
            script = generate_script(topic, style)
        st.subheader("🎬 Generated Script")
        st.markdown(script)  # Using markdown for better formatting
    else:
        st.warning("Please enter a topic.")

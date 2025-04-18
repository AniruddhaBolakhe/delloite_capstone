import streamlit as st
import google.generativeai as genai
from huggingface_hub import InferenceApi
from PIL import Image
from io import BytesIO

# Configure your API key for Hugging Face and Gemini (Google)
HF_API_TOKEN = "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"  # Replace with your Hugging Face API token
API_KEY = "AIzaSyC2MP2KLqImXqIiPhLeiaRqT3_oVhArFuI"  # Replace with your Google API key

# Initialize the Google Gemini model
genai.configure(api_key=API_KEY)
MODEL_NAME = "gemini-1.5-pro"  
model = genai.GenerativeModel(MODEL_NAME)

# Function to generate image from Hugging Face API
def generate_image(prompt, token):
    """Generates an image from a text prompt using Hugging Face's API"""
    inference = InferenceApi(repo_id="stabilityai/stable-diffusion-3.5-large", token=token)
    
    try:
        # Call Hugging Face Inference API with raw_response=True
        response = inference(inputs=prompt, raw_response=True)

        # Check if the response contains valid image data
        if response.status_code == 200:
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            return image
        else:
            st.error(f"Failed to generate image: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error generating image: {e}")
        return None

def generate_script(topic, style):
    """Generates a structured educational script in Markdown format."""

    prompt = f"""
You are an expert educator with deep knowledge across disciplines. Create a clear, concise, and engaging explanation on the topic: "{topic}" in a "{style}" tone.

The explanation should be suitable for a 4–5 minute spoken script (around 600–700 words). Avoid any YouTube-like phrases such as "Welcome to my channel" or "Don’t forget to subscribe". Instead, focus on clarity, precision, and delivering real value like a skilled teacher would.

Use the following Markdown structure:

### Hook
Begin with a striking fact, question, or idea that grabs attention and sets up the importance of the topic.

### Intro
Briefly outline what the explanation will cover. Set expectations for what the learner will understand by the end.

### Main Explanation
Break down the topic into its key components. Use clear, concise language and examples where appropriate. Avoid fluff—get to the point while maintaining flow and engagement.

### Reflection Prompt
Pose a thoughtful question to help the learner reflect or apply the concept. This should feel like a teacher encouraging deeper understanding.

### Summary
Wrap up the main points concisely. Reinforce the significance or application of the topic in real-world or academic settings.

Maintain an expert tone, avoid repetition, and make the script feel like a mini-lesson from a trusted professor.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, 'text') else "No script generated."
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.title("AI Content Generator")

# Sidebar for choosing the functionality
option = st.sidebar.selectbox(
    "Select an option:",
    ["Image Generator", "Script Generator"]
)

# Image Generator Section
if option == "Image Generator":
    st.header("Image Generator")
    prompt = st.text_input("Enter your image prompt:")
    if st.button("Generate Image"):
        if prompt:
            with st.spinner("Generating image..."):
                image = generate_image(prompt, HF_API_TOKEN)
            if image:
                st.image(image, caption="Generated Image", use_container_width=True)
            else:
                st.error("Error generating image.")
        else:
            st.warning("Please enter an image prompt.")

# Script Generator Section
elif option == "Script Generator":
    st.header("YouTube Script Generator")
    topic = st.text_input("Enter your video topic:")
    style = st.selectbox("Select script style:", ["Informative", "Casual", "Dramatic", "Humorous"])

    if st.button("Generate Script"):
        if topic:
            with st.spinner("Generating script..."):
                script = generate_script(topic, style)
            st.subheader("📝 Generated Script")
            st.markdown(script)
        else:
            st.warning("Please enter a topic.")

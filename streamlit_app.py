import streamlit as st
import openai
from PIL import Image
import io

# Show title and description.
st.title("🩺 Smart Healthcare Advisor")
st.write(
    "Input your symptoms, duration, and any additional information below. "
    "Optionally, you can upload an image. The app will analyze the information and provide health advice using GPT. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Initialize OpenAI API
    openai.api_key = openai_api_key

    # Input fields for symptoms, duration, and additional information
    symptoms = st.text_input("Symptoms", placeholder="Enter your symptoms")
    duration = st.text_input("Duration", placeholder="Enter duration of symptoms")
    additional_info = st.text_area(
        "Additional Information",
        placeholder="Enter any additional information"
    )

    # Optional image upload
    uploaded_image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])

    # Generate health advice based on input
    if st.button("Analyze Symptoms"):
        if not symptoms or not duration or not additional_info:
            st.warning("Please fill out all fields.")
        else:
            # Process the uploaded image if provided
            if uploaded_image:
                image = Image.open(uploaded_image)
                buffered = io.BytesIO()
                image.save(buffered, format="JPEG")
                img_str = buffered.getvalue()

                # Send the image to OpenAI with the input text
                prompt = (
                    f"Analyze the following symptoms: {symptoms} for {duration}. "
                    f"Additional info: {additional_info}. Also, consider the attached image for diagnosis."
                )

                # Generate an answer using the OpenAI API
                try:
                    response = openai.Image.create(
                        model="image-alpha-001",
                        prompt=prompt,
                        n=1,
                        images=img_str,
                        max_tokens=1000,
                        temperature=0.7,
                    )

                    # Display the response
                    st.subheader("Health Advice")
                    st.write(response.choices[0].text.strip())
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                # Create the prompt without image
                prompt = (
                    f"Analyze the following symptoms: {symptoms} for {duration}. "
                    f"Additional info: {additional_info}."
                )

                # Generate an answer using the OpenAI API
                try:
                    response = openai.Completion.create(
                        engine="text-davinci-003",
                        prompt=prompt,
                        max_tokens=1000,
                        temperature=0.7,
                    )

                    # Display the response
                    st.subheader("Health Advice")
                    st.write(response.choices[0].text.strip())
                except Exception as e:
                    st.error(f"An error occurred: {e}")

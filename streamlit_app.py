
import streamlit as st
import openai
from PIL import Image
import base64
import io

slides = [
    {
        "title": "Problem Statement",
        "content": "In healthcare, patients often need quick, reliable advice on their symptoms and health concerns. "
                   "Traditional healthcare systems can be slow and sometimes inaccessible, leading to delays in diagnosis and treatment.",
        "image": "problem.jpg"  # Replace with a relevant image path
    },
    {
        "title": "Our Solution",
        "content": "We developed a Smart Healthcare Advisor using GPT-4 and Streamlit to provide immediate, reliable health advice based on user inputs and optional image uploads. "
                   "This helps users get preliminary health advice quickly, guiding them on whether to seek further medical attention.",
        "image": "solution.jpg"  # Replace with a relevant image path
    },
    {
        "title": "How We Implemented It",
        "content": "We used Streamlit to create a user-friendly interface where users can input their symptoms, duration, additional information, and optionally upload an image. "
                   "The app uses OpenAI's GPT-4 to analyze the inputs and provide health advice.",
        "image": "implementation.jpg"  # Replace with a relevant image path
    },
    {
        "title": "Streamlit Integration",
        "content": "Streamlit allowed us to quickly develop and deploy our application. "
                   "We utilized various Streamlit components such as text inputs, file uploaders, and sliders to create an interactive and intuitive user experience.",
        "image": "streamlit.jpg"  # Replace with a relevant image path
    },
    {
        "title": "Conclusion",
        "content": "Our Smart Healthcare Advisor demonstrates the potential of combining AI with user-friendly interfaces to improve accessibility and efficiency in healthcare advice. "
                   "Future developments could include more advanced image analysis and integration with healthcare databases.",
        "image": "conclusion.jpg"  # Replace with a relevant image path
    }
]

# Create a slider to navigate through the slides
slide_number = st.slider("Navigate through the slides", 1, len(slides), 1)

# Display the selected slide
slide = slides[slide_number - 1]
st.title(slide["title"])
st.write(slide["content"])
if slide["image"]:
    st.image(slide["image"])
    
# Show title and description.
st.title("🩺 Smart Healthcare Advisor")
st.write(
    "Input your symptoms, severity, duration, and any additional information below. "
    "Optionally, you can upload an image. The app will analyze the information and provide health advice. "
    "As a reminder, this is not proffessional Medical Advice, and if you are unsure. It is always best to vist a doctor."
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
    severity = st.select_slider(
    "How Severe Are Your Symptoms?",
    options = [
        "1. Very Mild",
        "2. Mild",
        "3. Mild-Moderate",
        "4. Moderate",
        "5. Moderate-Severe",
        "6. Severe",
        "7. Very Severe",
        "8. Extremely Severe",
    ])    
    if (severity == "8. Extremely Severe"):
        st.write("We Reccommend That You See a Doctor Immediatly, The Smart Healthcare Advisor Does Not Have The Same Expertise As A Doctor and Cannot Give Out Professional Medical Advice")
  
    duration = st.text_input("Duration", placeholder="Enter duration of symptoms")
    additional_info = st.text_area(
        "Additional Information",
        placeholder="Enter any additional information"
    )

    # Optional image upload
    uploaded_image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])

    # Function to encode image to base64
    def encode_image(image):
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str

    # Generate health advice based on input
    if st.button("Analyze Symptoms"):
        if not symptoms or not duration or not additional_info:
            st.warning("Please fill out all fields.")
        else:
            messages = [
                {"role": "system", "content": "You are now a helpful medical assistant designed to aid users in identifying medical issues and suggesting steps to manage them. Your role is to analyze user inputs about their health concerns and offer informative, supportive advice. When responding, follow this structured input and output format: Input Format for Users: 1. Symptoms: Users should describe their symptoms clearly and thoroughly. 2. Duration: Users need to specify how long they have been experiencing these symptoms. 3. Additional Information: This includes any relevant personal health history, recent exposures, changes in lifestyle, current medications, and any other context that might affect their condition. 4. Image (if applicable): If there’s a visible manifestation of their issue (like a rash or swelling), users can upload an image to provide visual context. Your Response Should Include: 1. Identification of the Issue (if possible from the description): Based on the symptoms and duration, suggest possible medical issues. 2. Severity and Urgency: Assess and communicate the potential severity of the symptoms and the urgency with which medical attention might be needed. 3. Duration the Symptoms May Last: Provide an estimate on how long the symptoms might persist, based on the identified issue or similar conditions. 4. Self-Care Recommendations: Suggest actionable steps the user can take at home to ease symptoms or facilitate recovery. This could include lifestyle adjustments, over-the-counter medications, or simple home remedies. 5. Guidance on Daily Activities: Advise whether the symptoms are severe enough that the user should consider taking time off from work or school. 6. When to See a Doctor: Clearly state if and when it would be advisable to seek professional medical evaluation, particularly if symptoms are severe, worsening, or persist longer than typical for the suspected issue. 7. Reminder of Limitations: Remind users that the advice provided is based on the information they submitted and is not professional medical advice. Users should seek direct medical evaluation for a definitive diagnosis and treatment, especially for serious or life-threatening conditions. Additional Guidelines for Your Responses: - Empathy and Support: Always communicate in a tone that is empathetic and supportive, recognizing the concerns and anxieties that health issues can provoke. - Privacy and Sensitivity: Ensure that responses respect user privacy and handle sensitive health information with care. - Encourage Professional Help: Consistently encourage users to seek professional medical advice for a definitive diagnosis and treatment, especially if the situation could potentially be serious."},
                {"role": "user", "content": f"Analyze the following symptoms: {symptoms} for {duration}, with a severity of {severity}. Additional info: {additional_info}."}
            ]

            if uploaded_image:
                image = Image.open(uploaded_image)
                encoded_image = encode_image(image)
                messages.append(
                    {
                        "role": "user", 
                        "content": [
                            {"type": "text", "text": "Please analyze the following image for further information."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                        ]
                    }
                )
            # Generate an answer using the OpenAI API
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7,
                )

                # Display the response
                st.subheader("Health Advice")
                st.write(response.choices[0].message.content.strip())
            except Exception as e:
                st.error(f"An error occurred: {e}")
    st.write("In case of an emergency, please contact your local medical facility or call your country's emergency number.")

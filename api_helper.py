import base64
import json
import smtplib
from email.mime.text import MIMEText
import openai
import replicate
import streamlit as st
from PIL import Image
from io import BytesIO
import requests
import boto3
AWS_ACCESS_KEY_ID = st.secrets.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = st.secrets.AWS_SECRET_ACCESS_KEY
AWS_DEFAULT_REGION = st.secrets.AWS_DEFAULT_REGION

def save_content_aws(file_content, file_key, bucket_name):
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_DEFAULT_REGION)


    s3.put_object(Bucket=bucket_name, Key=file_key, Body=file_content)



# Set OpenAI API key
openai.api_key = st.secrets.okey

def open_ai_image_sizes():
    model_category = {":blue[Dalle-3]": "dall-e-3", ":blue[Dalle-2]": "dall-e-2"}
    selected_model = st.radio(
        ":blue[**Select the Image Models**]", list(model_category.keys())
    )
    model = model_category[selected_model]
    if model == "dall-e-2":
        size_category = {
            ":blue[Small image size]": "256x256",
            ":blue[Medium image size]": "512x512",
            ":blue[Standard image size]": "1024x1024",
        }
    else:
        size_category = {
            ":blue[Standard image size]": "1024x1024",
            ":blue[Wide image size]": "1792x1024",
            ":blue[Tall image size]": "1024x1792",
        }

    quality_category = {":blue[High Definition]": "hd", ":blue[Standard]": "standard"}

    style_category = {":red[Dramatic Image]": "vivid", ":green[Natural]": "natural"}

    col1, col2, col3 = st.columns(3)

    selected_size = col1.radio(
        ":blue[**Select preferred sizes**]", list(size_category.keys())
    )
    selected_quality = col2.radio(
        ":blue[**Select preferred quality**]", list(quality_category.keys())
    )
    selected_style = col3.radio(
        ":blue[**Select preferred style**]", list(style_category.keys())
    )
    size = size_category[selected_size]
    quality = quality_category[selected_quality]
    style = style_category[selected_style]
    return model, size, quality, style


def generate_prompt_from_openai(user_prompt):
    completion_prompt = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106", messages=[{"role": "user", "content": user_prompt}]
    )
    result = completion_prompt.choices[0].message.content.strip()
    return result


def generate_image_from_openai(model, image_prompt, size, quality, style):
    response = openai.images.generate(
        model=model,
        prompt=image_prompt,
        size=size,
        quality=quality,
        style=style,
        n=1,
    )
    image_url = response.data[0].url
    return image_url


# Generate image using OpenDALL·E
# selected_quality = quality[selected_quality]
def generate_image_from_replicate(image_prompt, width, height, selected_quality):
    replicates = replicate.Client(api_token=st.secrets.REPLICATE_API_TOKEN)
    image_output = replicates.run(
        "lucataco/open-dalle-v1.1:1c7d4c8dec39c7306df7794b28419078cb9d18b9213ab1c21fdc46a1deca0144",
        input={
            "prompt": image_prompt,
            "width": width,
            "height": height,
            "scheduler": "KarrasDPM",
            "num_outputs": 1,
            "guidance_scale": 9,
            "apply_watermark": True,
            "negative_prompt": "worst quality, low quality",
            "prompt_strength": 0.8,
            "num_inference_steps": selected_quality,
        },
    )
    return image_output[0]


def save_image(output_url):
    response = requests.get(output_url)
    output_image = Image.open(BytesIO(response.content))
    image_bytes = BytesIO()
    output_image.save(image_bytes, format="PNG")
    return image_bytes


def image_sizes():
    if "image_sizes_state" not in st.session_state:
        st.session_state.image_sizes_state = {
            "selected_platform": "Instagram",
            "selected_size_key": "Square",
            "selected_quality": "High Quality",
        }
    col1, col2 = st.columns(2)
    platforms = [
        ":blue[Pinterest]",
        ":blue[Instagram]",
        ":blue[Facebook]",
        ":blue[Twitter]",
        ":blue[Blog]",
    ]
    selected_platform = col1.radio(
        ":blue[**Select a Platform:**]", platforms, key="platforms"
    )
    size_options = {
        ":blue[Instagram]": {
            ":blue[Square]": (1080, 1080),
            ":blue[Landscape]": (1080, 566),
            ":blue[Vertical]": (1080, 1350),
        },
        ":blue[Pinterest]": {
            ":blue[Recommended]": (1000, 1500),
            ":blue[Size1]": (600, 900),
            ":blue[Size2]": (1200, 1800),
        },
        ":blue[Twitter]": {
            ":blue[Size1]": (1080, 1080),
            ":blue[Size2]": (1080, 1350),
        },
        ":blue[Facebook]": {
            ":blue[Square]": (2048, 2048),
            ":blue[Portrait]": (2048, 3072),
            ":blue[Landscape]": (2048, 1149),
        },
        ":blue[Blog]": {
            ":blue[Standard]": (1200, 630),
            ":blue[Landscape]": (1200, 900),
            ":blue[Portrait]": (900, 1200),
        },
    }

    st.session_state.image_sizes_state[
        ":blue[**selected_platform**]"
    ] = selected_platform

    # width, height, selected_quality = 0, 0, 0
    if selected_platform in size_options:
        selected_size_key = col2.radio(
            ":blue[**Select Image Size:**]",
            size_options[selected_platform].keys(),
            key="imagesize",
        )
        st.session_state.image_sizes_state["selected_size_key"] = selected_size_key

        # Retrieve the selected size tuple based on the key
        selected_size = size_options[selected_platform][selected_size_key]
        width, height = selected_size
        width = (width // 8) * 8
        height = (height // 8) * 8
    else:
        width, height = 0, 0

    quality = {":blue[High Quality]": 70, ":blue[Standard]": 25}
    selected_quality = st.radio(":blue[**Select Image Quality:**]", quality.keys())
    selected_quality_value = quality[selected_quality]
    st.session_state.image_sizes_state["selected_quality"] = selected_quality
    return width, height, selected_quality_value


def labeled_text_input(
    label, placeholder, font_size=16, padding="0px 0px 1rem", color="rgb(0, 104, 201)"
):
    label_html = f"<h5 style='font-size: {font_size}px; padding: {padding}; color: {color};'>{label}</h5>"
    st.markdown(label_html, unsafe_allow_html=True)
    return st.text_input(
        label="***", placeholder=placeholder, label_visibility="collapsed"
    )


def send_email(sender_email, subject, message):
    receiver_email = "thoufeeqllm@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "thoufeeqllm@gmail.com"
    smtp_password = st.secrets.smtp_password

    # Create MIMEText object
    email_body = f"Sender's Email: {sender_email}\n\n{message}"
    msg = MIMEText(email_body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Send the email
    server.sendmail(sender_email, receiver_email, msg.as_string())

    # Close the connection
    server.quit()


def display_generated_image_feedback():
    st.success(
        """Image successfully generated!\n
                  How is the image? Do you like it?\n
                  If not, try again and give me feedback on the Welcome Page."""
    )


def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.ibb.co/YRHYhv0/brian-logo.png);
                background-repeat: no-repeat;
                padding-top: 50px;
                background-position: 0px 0px;
                background-position: 0x 0px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "AI IMAGE GENE";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 20px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )



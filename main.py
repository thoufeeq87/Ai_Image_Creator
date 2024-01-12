import os
import openai
import replicate
import streamlit as st
from pymongo import MongoClient
from io import BytesIO
from PIL import Image
import numpy as np
from urllib.parse import quote_plus

# Set OpenAI API key
openai.api_key = st.secrets.okey

# Set Replicate API token
replicate_token = st.secrets.REPLICATE_API_TOKEN

st.title("Realistic Image Creator")

text = st.text_input("Enter what image you want to create!", "")

# Generate user prompt for image
user_prompt_image = f"""Act as a prompt generator for Dall-E. Generate a prompt that will yield the best response from Dall-E 
    for a prompt to create a personalized picture based on a description. 
    The prompt should be detailed and comprehensive, incorporating what makes a good prompt that will generate good, contextual responses.
    \nPrompt: Create a personalized profile picture based on the following description: [{text}]"""

# Generate user prompt for file name
user_prompt_file_name = f"""Create a file name for [{text}].
    File Name: {{prompt_name}}
    """

if st.button("Generate Image"):
    # Generate image prompt using OpenAI API
    completion_image = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": user_prompt_image}]
    )
    image_prompt = completion_image['choices'][0]['message']['content']

    # Generate file name using OpenAI API
    completion_file_name = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": user_prompt_file_name}]
    )
    generated_file_name = completion_file_name['choices'][0]['message']['content'].strip()

    # Escape username and password using quote_plus
    username = quote_plus("thoufeeq87")
    password = quote_plus("Heera@1521")

    # Construct the MongoDB URI
    mongodb_uri = f"mongodb+srv://{username}:{password}@imagecreatercluster.971ye5w.mongodb.net/"

    # Create MongoClient using the constructed URI
    client = MongoClient(mongodb_uri)
    db = client["images"]
    collection = db["collectionJan24"]

    # Generate image using OpenDALL·E
    replicates = replicate.Client(api_token=replicate_token)
    output = replicates.run(
        "lucataco/open-dalle-v1.1:1c7d4c8dec39c7306df7794b28419078cb9d18b9213ab1c21fdc46a1deca0144",
        input={
            "prompt": image_prompt,
            "width": 1024,
            "height": 1024,
            "scheduler": "KarrasDPM",
            "num_outputs": 1,
            "guidance_scale": 7.5,
            "apply_watermark": True,
            "negative_prompt": "worst quality, low quality",
            "prompt_strength": 0.8,
            "num_inference_steps": 60
        },
    )

    # Convert the output to a NumPy array
    output_array = np.array(output)

    # Reshape the array if necessary
    # output_array = output_array.reshape((height, width, 3))  # Replace height and width with actual dimensions

    # Convert to PIL Image
    image = Image.fromarray(output_array.astype('uint8'))

    # Display the generated image
    st.image(image, caption="Generated Image", use_column_width=True)

    # Convert PIL Image to BytesIO
    img_bytes_io = BytesIO()
    image.save(img_bytes_io, format="PNG")
    img_binary = img_bytes_io.getvalue()

    # Save data to MongoDB
    prompt_data = {
        "user_prompt_image": image_prompt,
        "file_name": generated_file_name,
        "image": img_binary,
    }

    result = collection.insert_one(prompt_data)
    st.success(f"User prompts and generated image saved with ObjectID: {result.inserted_id}")

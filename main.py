import openai
import replicate
import streamlit as st
import sqlite3

# Set OpenAI API key
openai.api_key = st.secrets.okey

# Set Replicate API token
replicate_token = st.secrets.REPLICATE_API_TOKEN

# Connect to SQLite database
conn = sqlite3.connect('image_generator.db')
cursor = conn.cursor()

# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS generated_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_prompt_image TEXT,
        file_name TEXT,
        image BLOB
    )
''')
conn.commit()

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
    image_prompt = completion_image.choices[0].message.content

    # Generate file name using OpenAI API
    completion_file_name = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "user", "content": user_prompt_file_name}]
    )
    generated_file_name = completion_file_name.choices[0].message.content.strip()

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

    # Save data to SQLite database
    cursor.execute('''
        INSERT INTO generated_images (user_prompt_image, file_name, image)
        VALUES (?, ?, ?)
    ''', (image_prompt, generated_file_name, output))
    conn.commit()

    st.image(output, caption=generated_file_name, use_column_width=True)
    st.success("User prompts and generated image saved successfully.")

# Close the database connection
conn.close()

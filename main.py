import openai
import replicate
import requests
import streamlit as st
from PIL import Image
from io import BytesIO
from google.cloud import storage


# Set up Google Cloud Storage client
storage_client = storage.Client.from_service_account_json("/Users/mohamedthoufeeq/Downloads/ai-image-generator-411113-36ad04447fb0.json")
bucket_name = "my-ai-images"
bucket = storage_client.get_bucket(bucket_name)
# Set OpenAI API key
openai.api_key = st.secrets.okey

# Set Replicate API token
replicate_token = st.secrets.REPLICATE_API_TOKEN

st.title("Realistic Image Creator")

text = st.text_input("Enter what image you want to create!", "")
col1, col2 = st.columns(2)
platforms = ["Pinterest", "Instagram", "Facebook", "Twitter", "Blog"]
selected_platform = col1.radio("Select a Platform:", platforms)
size_options = {
    "Instagram": {
        "Square": (1080, 1080),
        "Landscape": (1080, 566),
        "Vertical": (1080, 1350),
    },
    "Pinterest": {
        "Recommended": (1000, 1500),
        "Size1": (600, 900),
        "Size2": (1200, 1800),
    },
    "Twitter": {
        "Size1": (1080, 1080),
        "Size2": (1080, 1350),
    },
    "Facebook": {
        "Square": (2048, 2048),
        "Portrait": (2048, 3072),
        "Landscape": (2048, 1149),
    },
    "Blog": {
        "Standard": (1200, 630),
        "Landscape": (1200, 900),
        "Portrait": (900, 1200),
    },
}

if selected_platform in size_options:
    selected_size_key = col2.radio("Select Image Size:", size_options[selected_platform].keys())
    # Retrieve the selected size tuple based on the key
    selected_size = size_options[selected_platform][selected_size_key]
    width, height = selected_size
    width = (width // 8) * 8
    height = (height // 8) * 8


quality ={"High Quality" : 70,
          "Standard" : 25}
selected_quality = st.radio("Select Image Quality:", quality.keys())



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
            "width": width,
            "height": height,
            "scheduler": "KarrasDPM",
            "num_outputs": 1,
            "guidance_scale": 9,
            "apply_watermark": True,
            "negative_prompt": "worst quality, low quality",
            "prompt_strength": 0.8,
            "num_inference_steps": quality[selected_quality]
        },
    )
    st.image(output, caption=generated_file_name, use_column_width=True)

    response = requests.get(output[0])

    output_image = Image.open(BytesIO(response.content))
        # Save the image to a BytesIO object
    image_bytes = BytesIO()
    output_image.save(image_bytes, format='PNG')
    # Upload the image to Google Cloud Storage
    blob = bucket.blob(f"images/{generated_file_name}.png")
    blob.upload_from_string(image_bytes.getvalue(), content_type='image/png')

    st.success(f"Image uploaded to GCS: gs://{bucket_name}/images/{generated_file_name}.png")

    st.download_button(
            label="Download Image",
            data=image_bytes.getvalue(),
            file_name=f"{generated_file_name}.png",
            key="download_button",
            help="Click to download the generated image."
        )
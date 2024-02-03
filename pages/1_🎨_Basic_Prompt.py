from io import BytesIO

import streamlit as st
from api_helper import (
    image_sizes,
    generate_prompt_from_openai,
    generate_image_from_replicate,
    open_ai_image_sizes,
    generate_image_from_openai,
    save_image,
    labeled_text_input,
    display_generated_image_feedback,
    add_logo, save_content_aws,
)
from prompts import basic_prompt, file_name

st.header(":blue[🎨 Basic Prompt]")
add_logo()
help_toggle = st.toggle("Display Help")
if help_toggle:

    st.markdown("""🎨 **Description:**
        \n🌅 The Basic Prompt tool produces images based on your specific requests. For instance, 
        if you input, "Create a vibrant sunset with mountains and a serene lake," the tool will generate a 
        pleasing image featuring a colorful sunset, mountains, and a tranquil lake. This tool is capable of providing 
        high-quality images, resembling the work of a skilled graphic designer. 🎨
        """)

    st.markdown(""" 🎨 **Instructions:**
        \n1. **Input:** Enter your desired text, like "boy is playing chess."
        \n2. **Model:** Choose a model - Dale or Replicate.
        \n3. **Size:** Select the image size - Standard, Tall, or Wide.
        \n4. **Style:** Pick the Style - Dramatic or Natural.
        \n5. **Generate:** Click the "Generate Image" button.
        \nLet your imagination run wild! 🚀✨""")
    st.write(" ")
    st.video("https://youtu.be/jSw0w8TLvWw")

else:

    st.markdown("""
    ***Basic Prompt crafts realistic images from everyday plain English input. 
    Enter your input in the text box, select model, size, and quality. 
    The magic tool creates amazing images—click download to save. 
    If the result isn't perfect, try again. Your feedback is valued.***
    """)

    text = labeled_text_input(
        label="Enter what image you want to create!",
        placeholder="Type anything you want to create of a image",
    )

    selected_model = st.radio(
        ":blue[**Select the Model**]", [":blue[Dalle]", ":blue[Replicate]"]
    )
    if selected_model == ":blue[Replicate]":
        width, height, selected_quality = image_sizes()
        if st.button(":blue[Generate Image]"):
            with st.spinner("Please wait, the image is being created..."):
                image_prompt = generate_prompt_from_openai(
                    basic_prompt.basic_prompt.format(text=text)
                )
                file_name = generate_prompt_from_openai(
                    file_name.user_prompt_file_name.format(text=text)
                )
                image_output = generate_image_from_replicate(
                    image_prompt, width, height, selected_quality
                )
                st.image(image_output, caption=file_name, use_column_width=True)
                with open(image_output, 'rb') as img_file:
                    image_bytes = BytesIO(img_file.read())

                # Save prompt and image data to AWS S3 as JSON
                json_file_url = save_content_aws(text, image_bytes, file_name)

                st.success(f"Prompt and image data saved to AWS S3 as JSON. [View JSON file]({json_file_url})")
                image_bytes = save_image(image_output)
                st.download_button(
                    label="Download Image",
                    data=image_bytes.getvalue(),
                    file_name=f"{file_name}.png",
                    key="download_button",
                    help="Click to download the generated image",
                )
                display_generated_image_feedback()

    else:
        model, size, quality, style = open_ai_image_sizes()
        if st.button(":blue[Generate Image]"):
            with st.spinner("Please wait, the image is being created..."):
                image_prompt = generate_prompt_from_openai(
                    basic_prompt.basic_prompt.format(text=text)
                )
                file_name = generate_prompt_from_openai(
                    file_name.user_prompt_file_name.format(text=text)
                )
                image_output = generate_image_from_openai(
                    model, image_prompt, size, quality, style
                )

                st.image(image_output, caption=file_name, use_column_width=True)

                image_bytes = save_image(image_output)
                st.download_button(
                    label="Download Image",
                    data=image_bytes.getvalue(),
                    file_name=f"{file_name}.png",
                    key="download_button",
                    help="Click to download the generated image",
                )
                display_generated_image_feedback()
                image_bytes = BytesIO()
                image_output.save(image_bytes, format='PNG')
                image_bytes.seek(0)

                # Save prompt and image data to AWS S3 as JSON
                json_file_url = save_content_aws(text, image_bytes, file_name)

                st.success(f"Prompt and image data saved to AWS S3 as JSON. [View JSON file]({json_file_url})")
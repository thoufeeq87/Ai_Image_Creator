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
    add_logo,
)
from prompts import closeup_food_photos_prompt, file_name

st.header(":blue[🍲 Close Up Food Photo]")
add_logo()
st.write(
    """***Food Prompts enable you to create food pictures. Enter the desired food to generate an image. 
Choose the model, size, and quality. The magic tool creates a realistically yummy food—click download to save. 
If the result isn't perfect, try again. Your feedback is valued.***"""
)
# Food
food = labeled_text_input(
    label="Enter your desired food:", placeholder="Type for ex. spaghetti bolognese"
)
selected_model = st.radio(
    ":blue[**Select the Model**]", [":blue[Dalle]", ":blue[Replicate]"]
)
if selected_model == ":blue[Replicate]":
    width, height, selected_quality = image_sizes()
    if st.button(":blue[Generate Image]"):
        with st.spinner("Please wait, the image is being created..."):
            image_prompt = closeup_food_photos_prompt.closeup_food_photos_prompt.format(
                food=food
            )

            file_name = generate_prompt_from_openai(
                file_name.user_prompt_file_name.format(text=food)
            )
            image_output = generate_image_from_replicate(
                image_prompt, width, height, selected_quality
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
else:
    model, size, quality, style = open_ai_image_sizes()
    if st.button(":blue[Generate Image]"):
        with st.spinner("Please wait, the image is being created..."):
            image_prompt = closeup_food_photos_prompt.closeup_food_photos_prompt.format(
                food=food
            )

            file_name = generate_prompt_from_openai(
                file_name.user_prompt_file_name.format(text=food)
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

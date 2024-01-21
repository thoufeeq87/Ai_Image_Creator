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
from prompts import human_portrait_generation_prompt, file_name

st.header(":blue[👤 Human Portrait]")
add_logo()
st.write(
    """***Human Portrait crafts realistic Human portrait images from the simple input. Follow the instructions and 
input your desired text in the text box. Choose the model, size, and quality. 
The magic tool creates a realistic image—click download to save. 
If the result isn't perfect, try again. Your feedback is valued.***
"""
)

# Time Period
Time_Period = labeled_text_input(
    label="Enter the time period of the person you want to create:",
    placeholder="Type for ex. Renaissance, 1920s, Future",
    padding="0px 0px 0rem",
)

# Gender
Gender = labeled_text_input(
    label="Enter if the person is male or female:",
    placeholder="Type male or female",
    padding="0px 0px 0rem",
)

# Subject Description
Subject_Description = labeled_text_input(
    label="Enter the description of a person you want to create:",
    placeholder="Type subject description for ex. a wise philosopher, a flapper dancer, a cyberpunk hacker",
    padding="0px 0px 0rem",
)

# Clothing Description
Clothing_Description = labeled_text_input(
    label="Enter the description of clothing for a person:",
    placeholder="Type clothing description for Ex. traditional velvet robes, fringe and sequin dress, a cyberpunk hacker",
    padding="0px 0px 0rem",
)

# Art Style
Art_Style = labeled_text_input(
    label="Enter the art style you want to represent for the person:",
    placeholder="Type art style for ex. classical realism, art deco, neon cyberpunk",
    padding="0px 0px 0rem",
)

# Pose
Pose = labeled_text_input(
    label="Enter the pose of a person:",
    placeholder="Type pose for ex. sitting contemplatively with a quill, striking a dynamic dancing pose",
    padding="0px 0px 0rem",
)

# Background
Background = labeled_text_input(
    label="Enter background of a human portrait:",
    placeholder="Type background for ex. a dimly lit study with ancient scrolls, a jazz-filled speakeasy",
    padding="0px 0px 0rem",
)

# Additional Elements
Additional_Elements = labeled_text_input(
    label="Enter any additional element property for a human portrait:",
    placeholder="Type additional element for ex. none, an old book and a candle, a vintage microphone and jazz band",
    padding="0px 0px 0rem",
)

# Realism
realism = labeled_text_input(
    label="Enter realism for a human portrait:",
    placeholder="Type realism for ex. photorealistic, social realism, naturalism",
    padding="0px 0px 0rem",
)
selected_model = st.radio(
    ":blue[**Select the Model**]", [":blue[Dalle]", ":blue[Replicate]"]
)
if selected_model == ":blue[Replicate]":
    width, height, selected_quality = image_sizes()
    if st.button(":blue[Generate Image]"):
        with st.spinner("Please wait, the image is being created..."):
            image_prompt = human_portrait_generation_prompt.human_portrait_generation_prompt.format(
                Time_Period=Time_Period,
                Gender=Gender,
                Subject_Description=Subject_Description,
                Clothing_Description=Clothing_Description,
                Art_Style=Art_Style,
                Pose=Pose,
                Background=Background,
                Additional_Elements=Additional_Elements,
                realism=realism,
            )
            file_name = generate_prompt_from_openai(
                file_name.user_prompt_file_name.format(text=Subject_Description)
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
            image_prompt = human_portrait_generation_prompt.human_portrait_generation_prompt.format(
                Time_Period=Time_Period,
                Gender=Gender,
                Subject_Description=Subject_Description,
                Clothing_Description=Clothing_Description,
                Art_Style=Art_Style,
                Pose=Pose,
                Background=Background,
                Additional_Elements=Additional_Elements,
                realism=realism,
            )
            file_name = generate_prompt_from_openai(
                file_name.user_prompt_file_name.format(text=Subject_Description)
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

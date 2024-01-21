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
from prompts import realistic_images_anything_prompt, file_name

st.header(":blue[🌍 Realistic Images Anything]")
add_logo()
st.write(
    """***Realistic Images Anything crafts any image in a realistic version from the entered simple input. 
Follow the instructions and input your desired text in the text box. 
Choose the model, size, and quality. The magic tool creates a realistic image—click download to save. 
If the result isn't perfect, try again. Your feedback is valued.***
"""
)

# Subject
subject = labeled_text_input(
    label="Enter the subject:",
    placeholder="Type for ex. a woman, a couple, a bustling city street",
)

# Background or Place
background_or_place = labeled_text_input(
    label="Enter the background or place:",
    placeholder="Type for ex. in a swimming pool, in Starbucks, during rush hour",
)

# Situation or Action of the Subject
situation_action = labeled_text_input(
    label="Enter the situation or action of the subject:",
    placeholder="Type for ex. posing, drinking a coffee, people commuting",
)

# Time if Required
time = labeled_text_input(
    label="Enter the time if required:",
    placeholder="Type for ex. day time, dusk, afternoon",
)

# Custom Lighting
custom_lighting = labeled_text_input(
    label="Enter custom lighting:",
    placeholder="Type for ex. dark lighting, city lights, warm sunlight",
)

# Shot Type
shot_type = labeled_text_input(
    label="Enter the shot type:",
    placeholder="Type for ex. medium shot, wide shot, close-up",
)
selected_model = st.radio(
    ":blue[**Select the Model**]", [":blue[Dalle]", ":blue[Replicate]"]
)
if selected_model == ":blue[Replicate]":
    width, height, selected_quality = image_sizes()
    if st.button(":blue[Generate Image]"):
        with st.spinner("Please wait, the image is being created..."):
            image_prompt = realistic_images_anything_prompt.realistic_images_anything_prompt.format(
                subject=subject,
                background_or_place=background_or_place,
                situation_action=situation_action,
                time=time,
                custom_lighting=custom_lighting,
                shot_type=shot_type,
            )

            file_name = generate_prompt_from_openai(
                file_name.user_prompt_file_name.format(text=subject)
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
            image_prompt = realistic_images_anything_prompt.realistic_images_anything_prompt.format(
                subject=subject,
                background_or_place=background_or_place,
                situation_action=situation_action,
                time=time,
                custom_lighting=custom_lighting,
                shot_type=shot_type,
            )

            file_name = generate_prompt_from_openai(
                file_name.user_prompt_file_name.format(text=subject)
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

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
from prompts import realistic_textsign_images_prompt, file_name

st.header(":blue[✒️Realistic Text Sign Images]")
add_logo()

help_toggle = st.toggle("Display Help")
if help_toggle:
    st.markdown("""🎨 **Description:**
    \n🎨 Employ the Realistic Text Sign Images tool to generate captivating visuals of any subject holding a text sign! 
    Simply input the subject, such as a boy, specify the background like a bustling city, add the desired text, 
    for example, "Imagine," set the time (e.g., day), define the lighting, like warm sunlight, and indicate the type of shot, 
    perhaps a wide shot. Subsequently, receive lifelike images featuring your subject holding the "Imagine" sign. 
    Explore a video tutorial to grasp the tool's functionality! 🌟
    """)

    st.markdown(""" 🎨 **Instructions:**
    
    1. **Input**: Enter the subject, such as a cat, mountain, or boy.
    
    2. **Input**: Specify the background or place, like a city, a cozy cafe, or an urban street.
    
    3. **Input**: Enter your desired text, for example, "Imagine," "Explore," or "'Sip and enjoy.'"
    
    4. **Input**: Specify the time, choosing from options like day, dusk, or afternoon.
    
    5. **Input**: If applicable, enter custom lighting details, such as morning light, soft moonlight, or warm sunlight.
    
    6. **Input**: Specify the shot type, like a medium shot, wide shot, or close-up.
    
    7. **Model**: Choose a model - Dale or Replicate.
    
    8. **Size**: Select the image size - Standard, Tall, or Wide.
    
    9. **Style**: Pick the Style - Dramatic or Natural.
    
    10. **Generate**: Finally, click the "Generate Image" button.
    
    Let your imagination run wild! 🚀✨""")
    st.write(" ")
    st.video("https://youtu.be/dZHiouBdVjM")
else:
    st.write(
        """***Realistic Text Sign Images crafts an image with a text sign or board from the entered simple input. 
    Follow the instructions and input your desired text in the text box. Choose the model, size, and quality. 
    The magic tool creates a text sign image—click download to save. 
    If the result isn't perfect, try again. Your feedback is valued.***
    """
    )
    # Subject
    subject = labeled_text_input(
        label="Enter the subject:", placeholder="Type for ex. cat, mountain, boy"
    )

    # Background or Place
    background_or_place = labeled_text_input(
        label="Enter the background or place:",
        placeholder="Type for ex. a city, a cozy cafe, an urban street",
    )

    # Your Text
    your_text = labeled_text_input(
        label="Enter your text:",
        placeholder="Type for ex. Imagine, Explore, 'Sip and enjoy'",
    )

    # Time
    time = labeled_text_input(
        label="Enter the time:", placeholder="Type for ex. day, dusk, afternoon"
    )

    # Custom Lighting
    custom_lighting = labeled_text_input(
        label="Enter custom lighting (if any):",
        placeholder="Type for ex. morning light, soft moonlight, warm sunlight",
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
                image_prompt = realistic_textsign_images_prompt.realistic_textsign_images_prompt.format(
                    subject=subject,
                    background_or_place=background_or_place,
                    your_text=your_text,
                    time=time,
                    custom_lighting=custom_lighting,
                    shot_type=shot_type,
                )

                file_name = generate_prompt_from_openai(
                    file_name.user_prompt_file_name.format(text=your_text)
                )
                image_output = generate_image_from_replicate(
                    image_prompt, width, height, selected_quality
                )
                st.image(image_output, caption=file_name, use_column_width=True)
                image_bytes = save_image(image_output)
                image_file_content = image_bytes.getvalue()
                image_file_key = f"{file_name}.png"
                save_content_aws(image_file_content, image_file_key, "aiimagebucket")
                prompt_file_content = image_prompt.encode('utf-8')
                prompt_file_key = f"{file_name}.txt"
                save_content_aws(prompt_file_content, prompt_file_key, "aiimagebucket")
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
                image_prompt = realistic_textsign_images_prompt.realistic_textsign_images_prompt.format(
                    subject=subject,
                    background_or_place=background_or_place,
                    your_text=your_text,
                    time=time,
                    custom_lighting=custom_lighting,
                    shot_type=shot_type,
                )

                file_name = generate_prompt_from_openai(
                    file_name.user_prompt_file_name.format(text=your_text)
                )
                image_output = generate_image_from_openai(
                    model, image_prompt, size, quality, style
                )
                st.image(image_output, caption=file_name, use_column_width=True)
                image_bytes = save_image(image_output)
                image_file_content = image_bytes.getvalue()
                image_file_key = f"{file_name}.png"
                save_content_aws(image_file_content, image_file_key, "aiimagebucket")
                prompt_file_content = image_prompt.encode('utf-8')
                prompt_file_key = f"{file_name}.txt"
                save_content_aws(prompt_file_content, prompt_file_key, "aiimagebucket")
                image_bytes = save_image(image_output)
                st.download_button(
                    label="Download Image",
                    data=image_bytes.getvalue(),
                    file_name=f"{file_name}.png",
                    key="download_button",
                    help="Click to download the generated image",
                )
                display_generated_image_feedback()

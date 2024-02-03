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
from prompts import water_color_painting_prompt, file_name

st.header(":blue[🌈 Water Color Painting]")
add_logo()
help_toggle = st.toggle("Display Help")
if help_toggle:
    st.markdown("""🎨 **Description:**
   \n 🎨 Use the Watercolor Painting tool to make beautiful images that look like real watercolor paintings - 
    it's like having a human touch! Just follow the steps and type in details like the subject 
    (for example, a bouquet of wildflowers or a bowl of ripe fruit), the surface it's on 
    (like a rustic wooden table or glossy marble countertop), background colors 
    (maybe soft pastel hues or deep indigo tones), background elements (like a meadow or a hint of a kitchen), 
    lighting (maybe gentle natural sunlight or warm ambient light from a window), mood (serene and peaceful or 
    vibrant and inviting), colors (like soft pinks, blues, and greens), and any special requests 
    (for example, capturing the play of light on the fruit's surface). 
    The magic tool gives you hassle-free painting in just seconds! 🖌️
    """)

    st.markdown(""" 🎨 **Instructions:**

    1. **Input**: Enter the subject for your Watercolor Painting. For example, type in a description like "bouquet of wildflowers," "bowl of ripe fruit," or "antique pocket watch."
    
    2. **Input**: Specify the surface for the painting. You can type in details such as "rustic wooden table," "glossy marble countertop," or "weathered leather book."
    
    3. **Input**: Define the background for the painting. Choose details like "soft pastel hues," "deep indigo tones," or "sepia tones."
    
    4. **Input**: Enter background elements, such as "subtle impression of a meadow" or "hint of a kitchen interior."
    
    5. **Input**: Describe the lighting for the painting. Specify details like "gentle natural sunlight," "warm ambient light from a window," or "soft candlelight."
    
    6. **Input**: Set the mood for the painting. Type in details like "serene and peaceful," "vibrant and inviting," or "nostalgic and contemplative."
    
    7. **Input**: Choose the colors for the painting. Specify details like "soft pinks, blues, and greens" or "rich reds, yellows, and oranges."
    
    8. **Input**: Add any special requests for the painting. For example, you can request to "capture the play of light on the fruit's surface."
    
    9. **Model**: Choose a model - Dale or Replicate.
    
    10. **Size**: Select the image size - Standard, Tall, or Wide.
    
    11. **Style**: Pick the Style - Dramatic or Natural.
    
    12. **Generate**: Click the "Generate Image" button.
    
    Let your imagination run wild! 🚀✨""")
    st.write(" ")
    st.video("https://youtu.be/kafi0dlUQmo")
else:
    st.write(
        """***Watercolor Painting tool helps you create watercolor painting images similar to human touch based on your input. 
    Follow the instructions and carefully enter the inputs. Choose the model, size, and quality. The magic tool provides you with hassle-free painting in seconds—click download to save. 
    If the result isn't perfect, try again. Your feedback is valued.***
    """
    )
    # Subject for Water Color Painting
    Subject = labeled_text_input(
        label="Enter the subject for Water Color Painting:",
        placeholder="Type subject description, e.g., bouquet of wildflowers, bowl of ripe fruit, antique pocket watch",
        padding="0px 0px 0rem",
    )

    # Surface for the painting
    Surface = labeled_text_input(
        label="Enter the surface for the painting:",
        placeholder="Type surface details, e.g., rustic wooden table, glossy marble countertop, weathered leather book",
        padding="0px 0px 0rem",
    )

    # Background for the painting
    Background = labeled_text_input(
        label="Enter the background for the painting:",
        placeholder="Type background details, e.g., soft pastel hues, deep indigo tones, sepia tones",
        padding="0px 0px 0rem",
    )

    # Background elements
    Background_Element = labeled_text_input(
        label="Enter background elements:",
        placeholder="Type background elements, e.g., subtle impression of a meadow, hint of a kitchen interior",
        padding="0px 0px 0rem",
    )

    # Lighting for the painting
    Lighting = labeled_text_input(
        label="Enter the lighting for the painting:",
        placeholder="Type lighting details, e.g., gentle natural sunlight, warm ambient light from a window, soft candlelight",
        padding="0px 0px 0rem",
    )

    # Mood for the painting
    Mood = labeled_text_input(
        label="Enter the mood for the painting:",
        placeholder="Type mood details, e.g., serene and peaceful, vibrant and inviting, nostalgic and contemplative",
        padding="0px 0px 0rem",
    )

    # Colors for the painting
    Colors = labeled_text_input(
        label="Enter the colors for the painting:",
        placeholder="Type color details, e.g., soft pinks, blues, and greens, rich reds, yellows, and oranges",
        padding="0px 0px 0rem",
    )

    # Special requests for the painting
    Special_Requests = labeled_text_input(
        label="Enter any special requests for the painting:",
        placeholder="Type special requests, e.g., capture the play of light on the fruit's surface",
        padding="0px 0px 0rem",
    )

    selected_model = st.radio(
        ":blue[**Select the Model**]", [":blue[Dalle]", ":blue[Replicate]"]
    )
    if selected_model == ":blue[Replicate]":
        width, height, selected_quality = image_sizes()
        if st.button(":blue[Generate Image]"):
            with st.spinner("Please wait, the image is being created..."):
                image_prompt = (
                    water_color_painting_prompt.water_color_painting_prompt.format(
                        Subject=Subject,
                        Surface=Surface,
                        Background=Background,
                        Background_Element=Background_Element,
                        Lighting=Lighting,
                        Mood=Mood,
                        Colors=Colors,
                        Special_Requests=Special_Requests,
                    )
                )

                file_name_prompt = generate_prompt_from_openai(
                    file_name.user_prompt_file_name.format(text=Subject)
                )
                image_output = generate_image_from_replicate(
                    image_prompt, width, height, selected_quality
                )
                st.image(image_output, caption=file_name_prompt, use_column_width=True)
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
                    file_name=f"{file_name_prompt}.png",
                    key="download_button",
                    help="Click to download the generated image",
                )
                display_generated_image_feedback()
    else:
        model, size, quality, style = open_ai_image_sizes()
        if st.button(":blue[Generate Image]"):
            with st.spinner("Please wait, the image is being created..."):
                image_prompt = (
                    water_color_painting_prompt.water_color_painting_prompt.format(
                        Subject=Subject,
                        Surface=Surface,
                        Background=Background,
                        Background_Element=Background_Element,
                        Lighting=Lighting,
                        Mood=Mood,
                        Colors=Colors,
                        Special_Requests=Special_Requests,
                    )
                )

                file_name_prompt = generate_prompt_from_openai(
                    file_name.user_prompt_file_name.format(text=Subject)
                )
                image_output = generate_image_from_openai(
                    model, image_prompt, size, quality, style
                )
                st.image(image_output, caption=file_name_prompt, use_column_width=True)
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
                    file_name=f"{file_name_prompt}.png",
                    key="download_button",
                    help="Click to download the generated image",
                )
                display_generated_image_feedback()

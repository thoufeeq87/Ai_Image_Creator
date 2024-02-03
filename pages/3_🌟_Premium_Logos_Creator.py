import streamlit as st
from api_helper import (
    generate_prompt_from_openai,
    generate_image_from_replicate,
    open_ai_image_sizes,
    generate_image_from_openai,
    save_image,
    labeled_text_input,
    display_generated_image_feedback,
    add_logo,
)
from prompts import customizable_premium_logos_prompt, file_name

st.header(":blue[🌟 Premium Logos Creator]")
add_logo()
help_toggle = st.toggle("Display Help")
if help_toggle:
    st.markdown("""🎨 **Description:**
    \n🌟 Employ the Premium Logo Creator tool to craft extraordinary logos for your brand! 
    Simply specify your company type, provide your preferred color scheme, input your brand name, 
    and include any desired symbols for the logo. If uncertain, a helpful tutorial video is available 
    to guide you through the tool's usage. Explore it for a more comprehensive understanding! 🎨
    """)

    st.markdown(""" 🎨 **Instructions:**

    1. **Input**: Provide the type of your company, like "Technology."
    
    2. **Input**: Specify the color you prefer for the logo.
    
    3. **Input**: Enter the text you want as the brand name in the logo.
    
    4. **Input**: If you have any symbols in mind, enter them.
    
    5. **Model**: Choose between Dale or Replicate.
    
    6. **Size**: Select the image size - Standard, Tall, or Wide.
    
    7. **Style**: Pick the Style - Dramatic or Natural.
    
    8. **Generate**: Click the "Generate Image" button.
    
    Unleash your creativity! 🚀✨""")
    st.write(" ")
    st.video("https://youtu.be/WbrKP-j246k")
else:

    st.write(
        """***Premium Logo crafts a realistic logo from the entered simple input. 
    Follow the instructions and input your desired text in the text box. Choose the model, size, and quality. 
    The magic tool creates a logo for your company or blog—click and click download image to save. 
    If the result isn't perfect, try again. Your feedback is valued.***
    """
    )
    # Company Type
    company_type = labeled_text_input(
        label="Enter the type of the company:",
        placeholder="Type for ex.tech, health, clothing",
    )

    # Color of the Text in the Logo
    color = labeled_text_input(
        label="Enter the color of the text in the logo:",
        placeholder="Type for ex. grey, green, red",
    )

    # Brand Name Text
    brand_name = labeled_text_input(
        label="Enter the brand name text:",
        placeholder="Type for ex. GRAY MATTER, ASPIRO, BALANCE",
    )

    # Symbol if Required
    symbol = labeled_text_input(
        label="Enter the symbol if required:",
        placeholder="Type for ex. digital brain, T-shirt",
    )
    selected_model = st.radio(
        ":blue[**Select the Model**]", [":blue[Dalle]", ":blue[Replicate]"]
    )
    if selected_model == ":blue[Replicate]":
        if st.button(":blue[Generate Image]"):
            with st.spinner("Please wait, the image is being created..."):
                image_prompt = customizable_premium_logos_prompt.customizable_premium_logos_prompt.format(
                    company_type=company_type,
                    color=color,
                    brand_name=brand_name,
                    symbol=symbol,
                )

                file_name = generate_prompt_from_openai(
                    file_name.user_prompt_file_name.format(text=brand_name)
                )
                image_output = generate_image_from_replicate(
                    image_prompt, width=1024, height=1024, selected_quality=70
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
                image_prompt = customizable_premium_logos_prompt.customizable_premium_logos_prompt.format(
                    company_type=company_type,
                    color=color,
                    brand_name=brand_name,
                    symbol=symbol,
                )

                file_name = generate_prompt_from_openai(
                    file_name.user_prompt_file_name.format(text=brand_name)
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

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
from prompts import professional_image_creator_prompt, file_name

st.header(":blue[👔 Professional Image Generator]")
add_logo()

help_toggle = st.toggle("Display Help")
if help_toggle:
    st.markdown("""🎨 **Description:**
        \n🖼️ Use the Professional Prompt to make realistic profile pictures easily as an avatar! 
          Just follow the steps and type in what you need in the text box - things like your organization name, 
          where you'll use the image (like on LinkedIn or Facebook), the mood and style you want for your profile picture, 
          and any extra details you'd like to include. The magic tool will create an awesome profile picture for you - 
          simply click download to save it! 🚀✨
        """)

    st.markdown(""" 🎨 **Instructions:**
    
    1. **Input**: Enter the Organization name in the text box. For example, type any Organization Name like "TechInnovate."
    
    2. **Input**: Specify the purpose of creating the profile picture. For instance, type where you plan to post the picture, such as "LinkedIn Profile."
    
    3. **Input**: Enter the tone and style you want for the profile picture. For example, type in "Professional tone" or "Tech Savvy Tone."
    
    4. **Input**: Add any additional details required in the profile picture. For instance, specify if you want to include tech gadgets or symbols.
    
    5. **Model**: Choose a model - Dale or Replicate.
    
    6. **Size**: Select the image size - Standard, Tall, or Wide.
    
    7. **Style**: Pick the Style - Dramatic or Natural.
    
    8. **Generate**: Click the "Generate Image" button.
    
    Let your imagination run wild! 🚀✨""")
    st.write(" ")
    st.video("https://youtu.be/7vKERNhooG8")

else:

    st.write(
        """***Professional Prompt creates realistic profile pictures from the entered input. 
    Follow the instructions and enter the desired input in the text box. Choose the model, size, and quality. 
    The magic tool crafts an amazing profile picture—click download to save. 
    If the result isn't perfect, try again. Your feedback is valued.***
    """
    )
    User_Information = labeled_text_input(
        label="Enter the Organisation name:",
        placeholder="Type any Organisation Name For Ex. TechInnovate",
    )
    Context = labeled_text_input(
        label="Enter the purpose of creating profile picture:",
        placeholder="Type where you will post the picture For Ex. LinkedIn Profile",
    )

    Tone_Style = labeled_text_input(
        label="Enter the tone and style of profile picture:",
        placeholder="Type For Ex. Professional tone, Tech Savvy Tone",
    )

    Detail = labeled_text_input(
        label="Enter any additional details required in profile picture:",
        placeholder="Type for Ex. Specify tech gadgets or symbols",
    )
    selected_model = st.radio(
        ":blue[**Select the Model**]", [":blue[Dalle]", ":blue[Replicate]"]
    )
    if selected_model == ":blue[Replicate]":
        width, height, selected_quality = image_sizes()
        if st.button(":blue[Generate Image]"):
            with st.spinner("Please wait, the image is being created..."):
                image_prompt = generate_prompt_from_openai(
                    professional_image_creator_prompt.professional_image_creator_prompt.format(
                        User_Information=User_Information,
                        Context=Context,
                        Tone_Style=Tone_Style,
                        Detail=Detail,
                    )
                )
                file_name = generate_prompt_from_openai(
                    file_name.user_prompt_file_name.format(text=User_Information)
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
                image_prompt = generate_prompt_from_openai(
                    professional_image_creator_prompt.professional_image_creator_prompt.format(
                        User_Information=User_Information,
                        Context=Context,
                        Tone_Style=Tone_Style,
                        Detail=Detail,
                    )
                )
                file_name = generate_prompt_from_openai(
                    file_name.user_prompt_file_name.format(text=User_Information)
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

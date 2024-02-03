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
from prompts import human_portrait_generation_prompt, file_name

st.header(":blue[👤 Human Portrait]")
add_logo()
help_toggle = st.toggle("Display Help")
if help_toggle:
    st.markdown("""🎨 **Description:**
   \n 👤 The Human Portrait tool works just like the Animal Portrait one, creating portraits of people based on your input. 
    Imagine giving it details such as the person's features, like curly hair or glasses, describing their outfit – 
    maybe a stylish jacket or a laid-back T-shirt. Choose an art style, whether classic or modern, and set the mood 
    by selecting a pose, like a friendly smile or a unique prop. You can even decide where the person is, whether it's 
    in a bustling city park or against a beautiful beach sunset. If you want, throw in some extra details, like a cool hat
    or a favorite accessory. Once you've done all that, you'll end up with fantastic, lifelike human portraits ready to 
    hare with your friends and followers! 🎨📸
    """)

    st.markdown(""" 🎨 **Instructions:**

    1. **Input**: Specify the time period for your character, such as Renaissance, 1920s, or Future.
    
    2. **Input**: Indicate the gender of the person - male or female.
    
    3. **Input**: Describe the persona you want to create, like a wise philosopher, a flapper dancer, or a cyberpunk hacker.
    
    4. **Input**: Describe the clothing for your character, such as traditional velvet robes, fringe and sequin dress, or a cyberpunk hacker attire.
    
    5. **Input**: Define the pose for your character, for instance, sitting contemplatively with a quill or striking a dynamic dancing pose.
    
    6. **Input**: Specify the background for the human portrait, like a dimly lit study with ancient scrolls or a jazz-filled speakeasy.
    
    7. **Input**: Add any additional elements for the portrait, such as none, an old book and a candle, or a vintage microphone and jazz band.
    
    8. **Model**: Choose a model - Dale or Replicate.
    
    9. **Size**: Select the image size - Standard, Tall, or Wide.
    
    10. **Style**: Pick the Style - Dramatic or Natural.
    
    11. **Generate**: Finally, click the "Generate Image" button.
    
    Let your imagination run wild! 🚀✨""")
    st.write(" ")
    st.video("https://youtu.be/vFPwfLpNufQ")
else:
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

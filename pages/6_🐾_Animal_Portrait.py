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
from prompts import animal_portrait_prompt, file_name

st.header(":blue[🐾 Animal Portrait]")
add_logo()
help_toggle = st.toggle("Display Help")
if help_toggle:
    st.markdown("""🎨 **Description:**
   \n 🐾 The Animal Portrait tool functions similarly to the Human Portrait one, generating captivating images 
     of animals based on your specifications. Picture entering details like the animal breed (perhaps a majestic 
     Siberian tiger), outlining distinctive features (such as a sleek silver mane), selecting an art style (maybe abstract), 
     choosing a pose (how about a playful leap), determining the background (like a lush jungle setting), and incorporating 
     additional elements like vibrant tropical flowers. Following these steps, you'll receive stunning, true-to-life animal
      portraits ready to showcase on your social media! 🌟📸
    """)

    st.markdown(""" 🎨 **Instructions:**

    1. **Input**: Enter the breed of animal you want to create, for example, Siamese Cat, Bulldog, Parrot.
    
    2. **Input**: Enter the description of clothing for the animal, like a royal velvet collar, sporty jersey, or colorful feathered hat.
    
    3. **Input**: Enter the art style you want to represent for the animal, such as baroque, pop art, or abstract expressionism.
    
    4. **Input**: Enter the pose for the animal, whether it's curled up on a cushion, standing proudly with a ball, or in an abstract expressionism pose.
    
    5. **Input**: Enter the background for the animal portrait, whether it's in an ornate castle interior, a bright and vibrant cityscape, or a whimsical setting.
    
    6. **Input**: Add any additional elements or properties for the animal portrait, like a golden crown on its head or a comic-style speech bubble saying 'Fetch!'
    
    7. **Model**: Choose a model - Dale or Replicate.
    
    8. **Size**: Select the image size - Standard, Tall, or Wide.
    
    9. **Style**: Pick the style - Dramatic or Natural.
    
    10. **Generate**: Finally, click the "Generate Image" button.
    
    Let your imagination run wild! 🚀✨""")
    st.write(" ")
    st.video("https://youtu.be/C2b-BYntBR0")
else:
    st.write(
        """***Animal Portrait crafts animal portrait images from the simple input. Follow the instructions and 
    input your desired text in the text box. Choose the model, size, and quality. 
    The magic tool creates a realistic image—click download to save. 
    If the result isn't perfect, try again. Your feedback is valued.***
    """
    )
    # Animal Breed
    Animal_Breed = labeled_text_input(
        label="Enter the breed of animal you want to create:",
        placeholder="Type for ex. Siamese Cat, Bulldog, Parrot",
    )

    # Clothing Description
    Clothing_Description = labeled_text_input(
        label="Enter the description of clothing for an animal:",
        placeholder="Type clothing description for ex. royal velvet collar, sporty jersey, colorful feathered hat",
    )

    # Art Style
    Art_Style = labeled_text_input(
        label="Enter the art style you want to represent for the animal:",
        placeholder="Type art style for ex. baroque, pop art, abstract expressionism",
    )

    # Pose
    Pose = labeled_text_input(
        label="Enter the pose of an animal:",
        placeholder="Type pose for ex. curled up on a cushion, standing proudly with a ball, abstract expressionism",
    )

    # Background
    Background = labeled_text_input(
        label="Enter the background of an animal portrait:",
        placeholder="Type background for ex. ornate castle interior, bright and vibrant cityscape & whimsical",
    )

    # Additional Elements
    Additional_Elements = labeled_text_input(
        label="Enter any additional element property for an animal portrait:",
        placeholder="Type additional element for ex. golden crown on its head, comic-style speech bubble saying 'Fetch!'",
    )

    selected_model = st.radio(
        ":blue[**Select the Model**]", [":blue[Dalle]", ":blue[Replicate]"]
    )
    if selected_model == ":blue[Replicate]":
        width, height, selected_quality = image_sizes()
        if st.button(":blue[Generate Image]"):
            with st.spinner("Please wait, the image is being created..."):
                image_prompt = animal_portrait_prompt.animal_portrait_prompt.format(
                    Animal_Breed=Animal_Breed,
                    Clothing_Description=Clothing_Description,
                    Art_Style=Art_Style,
                    Pose=Pose,
                    Background=Background,
                    Additional_Elements=Additional_Elements,
                )

                file_name = generate_prompt_from_openai(
                    file_name.user_prompt_file_name.format(text=Animal_Breed)
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
                image_prompt = animal_portrait_prompt.animal_portrait_prompt.format(
                    Animal_Breed=Animal_Breed,
                    Clothing_Description=Clothing_Description,
                    Art_Style=Art_Style,
                    Pose=Pose,
                    Background=Background,
                    Additional_Elements=Additional_Elements,
                )

                file_name = generate_prompt_from_openai(
                    file_name.user_prompt_file_name.format(text=Animal_Breed)
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

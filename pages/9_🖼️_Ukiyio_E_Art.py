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
from prompts import ukiyoe_print_prompt, file_name

st.header(":blue[🖼️ Ukiyio-E Art]")
add_logo()
help_toggle = st.toggle("Display Help")
if help_toggle:
    st.markdown("""🎨 **Description:**
   \n 🎨 Use the Ukiyo-e Art tool to make pictures inspired by Ukiyo-e culture - it's easy! 
    Just follow the steps and type in details like the number of subjects, what they're doing, 
    the setting (like a misty bamboo forest), their actions (maybe practicing traditional martial arts), 
    their clothing (like traditional samurai attire), and extra things like falling cherry blossoms and a stone lantern. 
    Then, pick the model, size, and quality. The magic tool will create a beautiful Ukiyo-e Art - 
    just click download to save it! 🖼️✨
    """)

    st.markdown(""" 🎨 **Instructions:**
    
    1. **Input**: Specify the number of subjects for Ukiyo-e Art, like one, two, or three.
    
    2. **Input**: Describe the subjects, such as samurais, a traveling merchant, or court musicians.
    
    3. **Input**: Provide setting details for Ukiyo-e Art, like a misty bamboo forest or a bustling Edo market.
    
    4. **Input**: Detail the actions of the subjects, for example, engaged in traditional martial arts training or haggling with customers over exotic goods.
    
    5. **Input**: Describe the clothing of the subjects, such as being armored in traditional samurai attire or wearing colorful robes.
    
    6. **Input**: Add any additional elements for Ukiyo-e Art, like none, falling cherry blossoms and a stone lantern, or vendor carts and a traditional shop.
    
    7. **Model**: Choose a model - Dale or Replicate.
    
    8. **Size**: Select the image size - Standard, Tall, or Wide.
    
    9. **Style**: Pick the Style - Dramatic or Natural.
    
    10. **Generate**: Click the "Generate Image" button.
    
    Let your imagination run wild! 🚀✨""")
    st.write(" ")
    st.video("https://youtu.be/V63uCslC33E")
else:
    st.write(
        """***Ukiyo-e Art enables you to create images related to Ukiyo-e culture based on your input. 
    Follow the instructions and carefully enter the inputs. Choose the model, size, and quality. The magic tool creates a Ukiyo-e Art—click download to save. 
    If the result isn't perfect, try again. Your feedback is valued.***"""
    )
    # Number of Subjects
    Number_of_Subjects = labeled_text_input(
        label="Enter the number of subjects for Ukiyio-E Art:",
        placeholder="Type for ex. one, two, three",
    )

    # Subject Description
    Subject_Description = labeled_text_input(
        label="Enter the description of the subject:",
        placeholder="Type subject description for ex. samurais, travelling merchant, court musicians",
    )

    # Setting Details
    Setting_Details = labeled_text_input(
        label="Enter the setting details for Ukiyio-E Art:",
        placeholder="Type setting details for ex. a misty bamboo forest, a bustling Edo market, an elegant palace courtyard",
    )

    # Specific Actions
    Specific_Actions = labeled_text_input(
        label="Enter the actions of the subject:",
        placeholder="Type specific actions for ex. engaged in traditional martial arts training, haggling with customers over exotic goods",
    )

    # Clothing Details
    Clothing_Details = labeled_text_input(
        label="Enter the clothing description of the subject:",
        placeholder="Type clothing details for ex. armored in traditional samurai attire, colorful robes adorned with trade symbols",
    )

    # Additional Elements
    Additional_Elements = labeled_text_input(
        label="Enter any additional element property for Ukiyio-E Art:",
        placeholder="Type additional element for ex. none, falling cherry blossoms and a stone lantern, vendor carts and traditional shop facades",
    )


    selected_model = st.radio(
        ":blue[**Select the Model**]", [":blue[Dalle]", ":blue[Replicate]"]
    )
    if selected_model == ":blue[Replicate]":
        width, height, selected_quality = image_sizes()
        if st.button(":blue[Generate Image 🎨]"):
            with st.spinner("Please wait, the image is being created..."):
                image_prompt = ukiyoe_print_prompt.ukiyo_e_print_prompt.format(
                    Number_of_Subjects=Number_of_Subjects,
                    Subject_Description=Subject_Description,
                    Setting_Details=Setting_Details,
                    Specific_Actions=Specific_Actions,
                    Clothing_Details=Clothing_Details,
                    Additional_Elements=Additional_Elements,
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
                image_prompt = ukiyoe_print_prompt.ukiyo_e_print_prompt.format(
                    Number_of_Subjects=Number_of_Subjects,
                    Subject_Description=Subject_Description,
                    Setting_Details=Setting_Details,
                    Specific_Actions=Specific_Actions,
                    Clothing_Details=Clothing_Details,
                    Additional_Elements=Additional_Elements,
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

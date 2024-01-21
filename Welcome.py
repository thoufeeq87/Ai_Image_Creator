import streamlit as st

from api_helper import send_email, add_logo

st.set_page_config(page_title="AI Image Gene", page_icon="🎨")

st.header(":blue[👋 Welcome to AI Image Gene! 🎨🤖]")
add_logo()
st.write(
    """**Hello and welcome to my AI Image Gene App! Thank you for checking out my app**. 
    I'm excited to tell you about it. This app allows you to get realistic AI-generated images based on your input. 
    \nYou have various options, ranging from basic prompts to creating images with a watercolor painting effect. 
    Simply check the sidebar and choose the option you prefer. 
    \n**The app is free and currently in the beta stage. 
    I would greatly appreciate your honest feedback, whether it's positive or negative. 
    Feel free to share any suggestions you may have.** 
    \nYour feedback is crucial for the app's improvement. 
    Please use the form below to provide your input. 
    \n**Thank you for using the app, and I hope you enjoy it!** 
"""
)
st.title("Feedback Form")

# User inputs
subject = st.text_input("Subject", "")
sender_email = st.text_input("Your Email", "")
message = st.text_area("Message", "")

# Send email button
if st.button("Send Feedback"):
    if sender_email and subject and message:
        send_email(sender_email, subject, message)
        st.success("Feedback sent successfully!")
    else:
        st.warning("Please fill in all the fields.")

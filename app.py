%%writefile app.py
import streamlit as st
import urllib.request
from PIL import Image
import time

Navigation = {"page_title":"Streamlitweb.io","page_icon":":smiley:","layout":"centered"}
st.beta_set_page_config(**Navigation)

def videoUserDefined(src: str, width="100%", height=315):
    """An extension of the video widget
    Arguments:
        src {str} -- url of the video Eg:- https://www.youtube.com/embed/B2iAodr0fOo
    Keyword Arguments:
        width {str} -- video width(By default: {"100%"})
        height {int} -- video height (By default: {315})
    """
    st.write(
        f'<iframe width="{width}" height="{height}" src="{src}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
        unsafe_allow_html=True,
    )
 
def main():
    st.title("Web Application in streamlit.")
    st.subheader("Application is created using google colab & ngrok")
    menu = ["Home","About"]
    choice = st.sidebar.selectbox('Select the option',menu)
    if choice == 'Home':
        st.subheader("Streamlit application created using Colab & ngrok")
    if choice == 'About':
        st.subheader("WebApplication-1.0")

    #Image opening
    #img = Image.open("download.jfif") #open the image stored in specified location
    img = Image.open(urllib.request.urlopen("https://mms.businesswire.com/media/20200616005364/en/798639/22/Streamlit_Logo_%281%29.jpg")) # Opens the image from the url
    st.image(img, width=300, caption="Simple Image")

    # Video playing
    #vid_file = open("sample-mp4-file.mp4","rb").read() #play the video stored in specified location
    #st.video(vid_file)
    videoUserDefined("https://www.youtube.com/embed/B2iAodr0fOo")

    #widgets
    if st.checkbox("Show/hide"):
        st.text("Showing or Hiding Widget")

    # Radio
    status = st.radio("What is your status",("Married","Single"))
    if status == 'Married':
      st.success("You are Married")
    else:
      st.info("You are single")

 
if __name__ == '__main__':
    main()

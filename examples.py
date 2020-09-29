import pandas as pd
import numpy as np
import yfinance as yf
import streamlit as st
import datetime as dt
from pandas_datareader import data as pdr
from PIL import Image

'''
# This is an H1 HEADER Title
## This is an H2 HEADER Title
### This is an H3 HEADER Title 

3 dashes --- produce a horizontal line:
--- 

**This line is BOLD\n**

_This line is in italics_

~~This line is crossed out~~
'''

#image=Image.open("yahoo_finance_python.jpeg")
#st.sidebar.image(image, use_column_width=True)

#sb_image=Image.open("yahoo_finance_python.jpeg")
#st.sidebar.image(sb_image, use_column_width=True)

#image=Image.open("market4.jpeg")
#st.image(image, use_column_width=False)



#st.image(image, caption='Sunrise by the mountains',use_column_width=True)
#st.sidebar.header('Enter')


# page_bg_img = '''
# <style>
# body {
# background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
# background-size: cover;
# }
# </style>
# '''
#st.markdown(page_bg_img, unsafe_allow_html=True)


######## sample code to add background image:
import base64

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg('bg4.jpg')
########

#these do same horizontal line:
st.write("""---""")
st.markdown("---")


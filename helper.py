from wordcloud import WordCloud
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import matplotlib.pyplot as plt
import streamlit as st

stopwords = StopWordRemoverFactory().get_stop_words()

# Function for generating word clouds
def generate_wordcloud(data):
  wc = WordCloud(width=400, height=330,
                 max_words=100, background_color='white', #colormap="Pastel1",
                 scale=2, stopwords=stopwords,
                 collocations=False).\
                 generate(data.to_string())  #collocation - bigram
  return wc

def add_logo(logo_url: str, height: int = 120):
    """Add a logo (from logo_url) on the top of the navigation page of a multipage app.
    Taken from https://discuss.streamlit.io/t/put-logo-and-title-above-on-top-of-page-navigation-in-sidebar-of-multipage-app/28213/6

    The url can either be a url to the image, or a local path to the image.

    Args:
        logo_url (str): URL/local path of the logo
    """

    logo = f"url({logo_url})"

    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: {logo};
                background-repeat: no-repeat;
                padding-top: {height - 40}px;
                background-position: 20px 20px;
                max-width:100%;
                background-size: 60px 60px;
                
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# st.markdown('<img style="text-align:center;max-width:100%;padding-bottom:32px" src="https://upload.wikimedia.org/wikipedia/commons/archive/c/ce/20210909091155%21Twitter_Logo.png">', unsafe_allow_html=True)
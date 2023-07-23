import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Overview", 
                   page_icon="📈",
                   layout="wide")

st.markdown("# Sentiment Overview")

# SIDEBAR
# st.sidebar.header("Sentiment")

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
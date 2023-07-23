import streamlit as st
import numpy as np
import datetime
import pandas as pd
from helper import add_logo

st.set_page_config(page_title="Overview", 
                   page_icon="📈",
                   layout="wide")

st.markdown("# Sentiment Overview")

# SIDEBAR
# st.sidebar.header("Sentiment")
add_logo("https://stis.ac.id/media/source/up.png",40)

today = datetime.datetime.now()
past_3m = datetime.date(today.year, today.month-3, 1)

date = list(
    st.sidebar.date_input(
    "Masukkan rentang waktu",
    (past_3m, 
     today),
    datetime.date(today.year-10, 1, 1), #maxval
    datetime.date(today.year+10, 12, 31), #minval
    )
)

# handling the date
if len(date)==1:
    date.append(date[0] + datetime.timedelta(days=1))

date[1] = date[1] + datetime.timedelta(days=1)
data = pd.read_csv('data/labeled.csv').drop(['Unnamed: 0'], axis=1)
data['like'] = data['like'].replace({'undefined':0}).astype(int)
data['status'] = data['status'].astype(str)
data['time'] = data['time'].apply(lambda x: x[:10])
data['interaction'] = data.apply(lambda x: x['like']+x['reply']+x['retweet'], axis=1)

"## Sampel Dataset"
st.dataframe(data[(data['time'] >= str(date[0])) & (data['time'] <= str(date[1]))])
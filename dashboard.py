import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from numerize import numerize
from helper import generate_wordcloud

import datetime
import plotly.express as px




st.set_page_config(page_title="Sentimen Pekan Raya Jakarta 2023",
                   page_icon="📈",
                   layout="wide")

# hide menu style
style = """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

<style>
"""
# st.markdown(style, unsafe_allow_html=True)

# DEFINISIKAN DATA DAN METRIKS
data = pd.read_csv('data/labeled.csv').drop(['Unnamed: 0'], axis=1)
data['like'] = data['like'].replace({'undefined':0}).astype(int)
data['time'] = data['time'].apply(lambda x: x[:10])
data['interaction'] = data.apply(lambda x: x['like']+x['reply']+x['retweet'], axis=1)

# FOR SENTIMENT
df_sentiment = pd.DataFrame(data['prediction'].value_counts()).rename({'prediction':'total',
                                                                       'count':'total'}, axis=1)
# df_sentiment.columns = [['total', df_sentiment.columns[-1]]]
df_sentiment['sentiment'] = ['Positive','Negative']

# FOR TWEET NUMBER
df_tweet = data.groupby(["time"]).agg({'like':['count','sum'],
                        'reply' : ['sum'],
                        'retweet' : ['sum']
                        }).reset_index()
df_tweet.columns = [col[0] if col[1] == '' else col[0] + '_' + col[1] for col in df_tweet.columns]

# SIDEBAR
# st.sidebar.header("Main")
# val = st.sidebar.selectbox(
#         "Pilih Sentimen",
#         ['Positif', 'Negatif']
#     )

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

with st.sidebar:
    pass


# TITLE
"# Analisis Sentimen Agenda Pekan Raya Jakarta Tahun 2023"
"Pekan Raya Jakarta (PRJ) merupakan agenda tahunan yang diselenggarakan oleh Pemerintah DKI Jakarta dengan kegiatan berupa festival, pameran, hingga konser musik. Melalui analisis sentimen terhadap cuitan pengguna Twitter, kita dapat mengetahui apa saja trend yang marak saat agenda ini terlaksana."
"---"

a11, a12 = st.columns(2)
a21, a22 = st.columns(2)

# BARIS PERTAMA
with a11:
    st.metric(label="Jumlah Tweet",
        value=f"{numerize.numerize(data.shape[0])}"
        )
    
    fig = px.line(df_tweet, x='time', y='like_count',
             hover_data=['like_sum', 'reply_sum', 'retweet_sum'], 
             labels={'like_sum':'like',
                     'reply_sum':'reply',
                     'retweet_sum':'retweet',
                     'like_count':'tweet'},
            height=400
            )
    fig.update_yaxes(visible=False, fixedrange=True)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with a12:
    st.metric(label="Jumlah Interaksi",
    value=f"{numerize.numerize(data['interaction'].sum().item())}"
    )
    fig = px.line(df_tweet, x='time', y='like_sum',
             hover_data=['like_sum', 'reply_sum', 'retweet_sum'], 
             labels={'like_sum':'like',
                     'reply_sum':'reply',
                     'retweet_sum':'retweet'},
            height=400
            )
    fig.update_yaxes(visible=False, fixedrange=True)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with a21:
    "Wordcloud"
    wc= generate_wordcloud(data['clean'])
    plt.figure(figsize=(10,8))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    st.pyplot(plt)

with a22:
    "Sentimen Pengguna"
    fig = px.pie(df_sentiment, 
            names='sentiment',
            values='total',  
            # title='Sentiment Pengguna',
            hole=.3,
            height=300
            ) 
    fig.update_traces(textposition='inside', textinfo='percent+label', textfont_size=18,)
    fig.update_layout(showlegend=False,
                      margin=dict(l=20, r=20, t=20, b=20),
)
    st.plotly_chart(
        fig,
        use_container_width=True
    )

"## Sampel Dataset"
st.dataframe(data[(data['time'] >= str(date[0])) & (data['time'] <= str(date[1]))])















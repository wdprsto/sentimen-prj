import streamlit as st
import numpy as np
import datetime
import pandas as pd
from helper import add_logo
import plotly.express as px

st.set_page_config(page_title="Overview", 
                   page_icon="📈",
                   layout="wide")

st.markdown("# Sentiment Overview")

# DATASET
# DEFINISIKAN DATA DAN METRIKS
data = pd.read_csv('data/labeled.csv').drop(['Unnamed: 0'], axis=1)
data['like'] = data['like'].replace({'undefined':0}).astype(int)
data['time'] = data['time'].apply(lambda x: x[:10])
data['interaction'] = data.apply(lambda x: x['like']+x['reply']+x['retweet'], axis=1)

# for sentiment
df_sentiment = pd.DataFrame(data['prediction'].value_counts()).rename({'prediction':'total',
                                                                       'count':'total'}, axis=1)
df_sentiment['sentiment'] = ['Positive','Negative']

# FOR TWEET NUMBER
df_tweet = data.groupby(["time","prediction"]).agg({
                        'like':['count','sum'],
                        'reply' : ['sum'],
                        'retweet' : ['sum']
                        }).reset_index()
df_tweet.columns = [col[0] if col[1] == '' else col[0] + '_' + col[1] for col in df_tweet.columns]


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

# sentimen
a11, a12 = st.columns(2)

with a11:
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
                      margin=dict(l=20, r=20, t=20, b=20))
    fig.update_yaxes(visible=False, fixedrange=True)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with a12:
    plotly_colors = ['red', '#636EFA'] # atur warna linechartnya agar sesuai denan warna di pie
    
    fig = px.line(df_tweet, x='time', y='like_sum', color='prediction',
             hover_data=['like_sum', 'reply_sum', 'retweet_sum'], 
             labels={'like_sum':'like',
                     'reply_sum':'reply',
                     'retweet_sum':'retweet',
                     'prediction':'sentiment'},
            height=400,
            color_discrete_sequence=plotly_colors
            )
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(showlegend=False)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

"## Sampel Tweet"
st.dataframe(data[(data['time'] >= str(date[0])) & (data['time'] <= str(date[1]))]\
                [['username','text','time','prediction','retweet','like','reply','tweet_link']],
            use_container_width=True,
            column_config={
                'prediction':'sentiment',
                'tweet_link':st.column_config.LinkColumn("tweet_link")
            }
             )
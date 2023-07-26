import streamlit as st
import numpy as np
import datetime
import pandas as pd
from helper import add_logo
import plotly.express as px

st.set_page_config(page_title="Hashtag Overview", 
                   page_icon="📈",
                   layout="wide")

st.markdown("# Hashtag Overview")

# DATASET
# DEFINISIKAN DATA DAN METRIKS
data = pd.read_csv('data/hashtag.csv').drop(['Unnamed: 0'], axis=1)
data['like'] = data['like'].replace({'undefined':0}).astype(int)
data['time'] = data['time'].apply(lambda x: x[:10])
data['interaction'] = data.apply(lambda x: x['like']+x['reply']+x['retweet'], axis=1)
data['hashtag'] = data['hashtag'].apply(lambda x: x.lower().strip().replace("ᅠᅠ","").replace("ᅠ",""))
# for top hashtag
# df_sentiment = pd.DataFrame(data['hashtag'].value_counts()).rename({'prediction':'total',
#                                                                        'count':'total'}, axis=1)

# FOR TWEET NUMBER
df_tweet = data.groupby(["hashtag"]).agg({
                        'like':['count','sum'],
                        'reply' : ['sum'],
                        'retweet' : ['sum'],
                        'interaction' : ['sum'],
                        'username':['nunique']
                        }).reset_index()
df_tweet.columns = [col[0] if col[1] == '' else col[0] + '_' + col[1] for col in df_tweet.columns]
df_tweet.sort_values(by=['interaction_sum'], ascending=False, inplace=True)


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
data2 = data.groupby(["hashtag","time"]).agg({
                        'like':['count','sum'],
                        'reply' : ['sum'],
                        'retweet' : ['sum'],
                        'interaction' : ['sum'],
                        'username':['nunique']
                        }).reset_index()
data2.columns = [col[0] if col[1] == '' else col[0] + '_' + col[1] for col in data2.columns]
st.dataframe(data2)

# sentimen
a11, a12 = st.columns(2)

with a11:  
    
    a111, a112 = st.columns(2)
    with a111:
        st.metric(label="Jumlah Hashtag",
        value=f"{(df_tweet.shape[0])}"
        )
        st.metric(label="Jumlah Tweet",
        value=f"{(df_tweet['like_count'].sum())}"
        )

    with a112:
        st.metric(label="Jumlah User",
        value=f"{(df_tweet['username_nunique'].sum())}"
        )
        st.metric(label="Total Engagement",
        value=f"{(df_tweet['interaction_sum'].sum())}"
        )

with a12:
    pass
    # plotly_colors = ['red', '#636EFA'] # atur warna linechartnya agar sesuai denan warna di pie
    
    # fig = px.line(df_tweet, x='time', y='like_sum', color='prediction',
    #          hover_data=['like_sum', 'reply_sum', 'retweet_sum'], 
    #          labels={'like_sum':'like',
    #                  'reply_sum':'reply',
    #                  'retweet_sum':'retweet',
    #                  'prediction':'sentiment'},
    #         height=400,
    #         color_discrete_sequence=plotly_colors
    #         )
    # fig.update_yaxes(visible=False, fixedrange=True)
    # fig.update_layout(showlegend=False)

    # st.plotly_chart(
    #     fig,
    #     use_container_width=True
    # )

"## Hashtag Details"
# st.dataframe(data[(data['time'] >= str(date[0])) & (data['time'] <= str(date[1]))]\
#                 [['username','text','time','prediction','retweet','like','reply','tweet_link']],
#             use_container_width=True,
#             column_config={
#                 'prediction':'sentiment',
#                 'tweet_link':st.column_config.LinkColumn("tweet_link")
#             }
#              )
st.dataframe(df_tweet[['hashtag','like_count','username_nunique','retweet_sum','like_sum','reply_sum','interaction_sum']],
             use_container_width=True,
             hide_index=True,
             column_config={
                'hashtag':'Hashtag',
                'like_count':"Tweets",
                'like_sum':'Likes',
                'reply_sum':'Replies',
                'retweet_sum':'Retweets',
                'interaction_sum':'Engagement',
                'username_nunique':'User'

            })
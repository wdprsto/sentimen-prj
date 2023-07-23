from wordcloud import WordCloud
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import matplotlib.pyplot as plt

stopwords = StopWordRemoverFactory().get_stop_words()

# Function for generating word clouds
def generate_wordcloud(data):
  wc = WordCloud(width=400, height=330,
                 max_words=100, background_color='white', #colormap="Pastel1",
                 scale=2, stopwords=stopwords,
                 collocations=False).\
                 generate(data.to_string())  #collocation - bigram
  return wc

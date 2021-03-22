# Python program to generate WordCloud 

  

# importing all necessery modules 

from wordcloud import WordCloud, STOPWORDS 

import matplotlib.pyplot as plt 

import pandas as pd 

from pathlib import Path

  

# Reads Excel file  

df = pd.read_excel(r"query-presto-272.xlsx", header=0, index_col=None) 

df.head()

  

comment_words = '' 

STOPWORDS = ''

stopwords = set(STOPWORDS) 

c = 0

# iterate through the Excel file 

for val in df['inc_nm_tx']: 

  # typecaste each val to string

  val = str.strip(str(val))

 

  # split the value

  tokens = val.split() 

    

  # Converts each token into lowercase 

  for i in range(len(tokens)): 

      tokens[i] = tokens[i].lower() 

    

  comment_words += " ".join(tokens)+" "

  

wordcloud = WordCloud(width = 800, height = 800, 

                background_color ='white', 

                stopwords = stopwords, 

                min_font_size = 10).generate(comment_words) 

  

# plot the WordCloud image                        

plt.figure(figsize = (8, 8), facecolor = None) 

plt.imshow(wordcloud) 

plt.axis("off") 

plt.tight_layout(pad = 0) 

  

plt.show() 

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 13:31:34 2018

@author: Sowmya
"""

import io
import re 
import tweepy 
import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


  
# keys and tokens from the Twitter Dev Console 
consumer_key = "x664MoaIumEtbB2pAaOoLtNUz"
consumer_secret = "wh3wDjx4lAa82EgCtTORHezjudiJwmR37Pkz58ASxPO1K06ZPN"
access_token = "1041499096492789762-4bHoVsUPAbJ9DRUlzty7xuKwvZxbA8"
access_token_secret = "tvZnzg6rEdQ0WhtK4dAvovOQGEaUEHMEq26Dcb5ozYcp4"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
## Pass access token and access secret to Tweepy's user authentication handler
auth.set_access_token(access_token, access_token_secret)

G1=nx.Graph()
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid=SentimentIntensityAnalyzer()

Company_1_positivetweet_count=0
Company_1_neutraltweet_count=0
Company_1_Negativetweet_count=0
Company_2_positivetweet_count=0
Company_2_neutraltweet_count=0
Company_2_Negativetweet_count=0


## Creating a twitter API wrapper using tweepy
print('###########################################################')
cleanedTweets = []
USA_Locations=['texas','tx','new york','ny','california','ca','north carolina','nc','philadelphia', 'pa','usa','washington','dc','san francisco','hoston','seattle','united states','illinois','boston','chicago','nj','miami','dallas','minneapolis','florida','usa','new jersey']
locationDict={}
result = []
count=1
api = tweepy.API(auth, wait_on_rate_limit=True)
Company_1=raw_input("Enter the 1st Company: ")
Company_2=raw_input("Enter the 2nd company: ")

search =Company_1+' OR '+Company_2
print(search)
print('Tweets are')

fetched_tweets = tweepy.Cursor(api.search, q= search +'-filter:retweets',
                               geo_enabled='True',tweet_mode="extended",lang='en').items(4000)
#fetched_tweets = api.search('samsung', count = 10000, lang='en')+ api.search('iphone', count = 10000, lang='en')

Locations=[]
for line in fetched_tweets: 
    #print(line.user.location)
    my_tweet = line.full_text
    location_count=0
    loc=[]
   
    my_tweet = re.sub('http\S+\s*', '', my_tweet)  # remove URLs
    my_tweet = re.sub('RT', '', my_tweet)  # remove RT
    my_tweet = re.sub('#\S+', '', my_tweet)  # remove hashtags
    my_tweet = re.sub('@\S+', '', my_tweet)  # remove mentions
    my_tweet = re.sub('[%s]' % re.escape("""!"#$%&'‘’“”–()—*?+,-./:;<=>?@[\]^_`{|}~"""), '', my_tweet)  # remove punctuations
    my_tweet = re.sub('\s+', ' ', my_tweet)  # remove extra whitespace
    
    ## regular expression compile method is used to combine the unicode patterns into regular expression objects for reuse
    emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"
    u"(\ud83d[\u0000-\uffff])|"# symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE) 
    my_tweet = emoji_pattern.sub(r'',my_tweet)
    
    #sentimentDict={}
    
    ## the strip method removes whitespace from beginning and end of the tweet text and lower method converts text to lowercase
    my_tweet = my_tweet.strip()
    my_tweet = my_tweet.lower()
    location=(line.user.location).lower()
    loc=location.split(',')
    for i in loc:
        print(i)
    print('-----------------------------!!!!!!!!!!!!')
    for country in USA_Locations:
        for word in loc:
            #print(word,country)
            #print(word[1:])
            if word[2:]==country or word==country or word[1:]==country:
                location='USA'
            
    
    for country in Locations:
        #print(location)
        if country==location:
            location_count=1
            
    if location_count==0:
        Locations.append(location)
        locationDict[location]=1
    else:
        locationDict[location]=locationDict[location]+1
    cleanedTweets.append(my_tweet)
    print(my_tweet,count)
    print('____________________________________')
    analysis = sid.polarity_scores(my_tweet)
    words=my_tweet.split()
    for word in words:
        if (word==Company_1 or word==Company_2 ):
            count=count+1
            company=word
            if analysis['pos'] >analysis['neg']:
                if company==Company_1:
                    Company_1_positivetweet_count=Company_1_positivetweet_count+1
                elif company==Company_2:
                    Company_2_positivetweet_count=Company_2_positivetweet_count+1
                sentiment = 'positive'
                result.append({
                        'Time': line.created_at.strftime("%d/%b/%Y:%H:%M:%S %Z"),
                        'text': my_tweet,
                        'location':line.user.location,
                        'sentiment':'positive',
                        'Company':company
                        })
            elif analysis['pos'] ==analysis['neg']:
                if company==Company_1:
                    Company_1_neutraltweet_count=Company_1_neutraltweet_count+1
                elif company==Company_2:
                   Company_2_neutraltweet_count=Company_2_neutraltweet_count+1
                  
                sentiment = 'neutral'
                result.append({
                        'Time': line.created_at.strftime("%d/%b/%Y:%H:%M:%S %Z"),
                        'text': my_tweet,
                        'location':line.user.location,
                        'sentiment':'neutral',
                        'Company':company
                        })
            elif analysis['pos'] <analysis['neg']:
                if company==Company_1:
                    Company_1_Negativetweet_count=Company_1_Negativetweet_count+1
                elif company==Company_2:
                    Company_2_Negativetweet_count=Company_2_Negativetweet_count+1
                sentiment = 'negative'
                result.append({
                        'Time': line.created_at.strftime("%d/%b/%Y:%H:%M:%S %Z"),
                        'text': my_tweet,
                        'location':line.user.location,
                        'sentiment':'negative',
                        'Company':company
                        })
    
    
    
    
## opens a new text file in write mode and write the cleaned list of dictionaries into the text file
#nx.draw_networkx(G1)
#pos=nx.random_layout(G1)
#plt.figure(3,figsize=(12,12))
#nx.draw(G1,pos,with_labels=True)
#plt.show()
for location in Locations:
    print(location,locationDict[location])
with io.open("Vadersentiment.json",'w',encoding="utf-8") as outfile:
   my_tweets = json.dumps(result, ensure_ascii=False,indent=1)
   if isinstance(my_tweets, str):
        my_tweets = my_tweets.decode("utf-8")

   outfile.write(my_tweets)
   


sentimentSize=[locationDict['USA'],count-locationDict['USA']]
labels='USA','Other'
plt.pie(sentimentSize,labels=labels, autopct='%1.1f%%',startangle=140)
plt.axis('equal')
plt.show()
#
#y_pos = np.arange(len(labels))
#plt.bar(y_pos, sentimentSize, align='center', alpha=0.5)
#plt.xticks(y_pos, labels)
#
#plt.ylabel('Tweets')
#plt.title('Companies Reviews')
print('count is',count)
print("USA Count is",locationDict['USA'])

positive_tweets=[Company_1_positivetweet_count,Company_2_positivetweet_count]
negative_tweets=[Company_1_Negativetweet_count,Company_2_Negativetweet_count]
neutral_tweets=[Company_1_neutraltweet_count,Company_2_neutraltweet_count]


N = 2
index = np.arange(N)  # the x locations for the groups
width = 0.27       # the width of the bars

fig = plt.figure()
df = fig.add_subplot(111)

bar1 = df.bar(index, positive_tweets, width, color='g')

bar2 = df.bar(index+width, negative_tweets, width, color='r')

bar3 = df.bar(index+width*2, neutral_tweets, width, color='b')

df.set_ylabel('TweetsCount')
df.set_xticks(index+width)
df.set_xticklabels( (Company_1, Company_2) )
df.legend( (bar1[0], bar2[0], bar3[0]), ('Positive', 'Negatuve', 'Neutral') ) # for the legend on top right

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        df.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%d'%int(h),
                ha='center', va='bottom')

autolabel(bar1)
autolabel(bar2)
autolabel(bar3)

plt.show()

 #****************************************************
    #To draw Network
    #*********************************************************
    #print(line)
#    user_mention=line.entities['user_mentions']
#    size=len(user_mention)
#    original_tweeter=line.user.name
#    if size>0:
#        for i in range(size):
#            mention_name=user_mention[i]['name']
#            print(mention_name)
#            G1.add_node(original_tweeter)
#            G1.add_edge(original_tweeter,mention_name)
#
#    
#            print('the original tweeter is: ',original_tweeter)

#    for i in range(size):
#        mention_name=user_mention[0]['name']
#        print(mention_name)
#        G1.add_edges_from([(original_tweeter,'samyuktha')])

#********************************************************************************************
#For sentimentAnalysis using TextBlob
##*********************************************************************
#from textblob import TextBlob
#positivetweet_count = 0
#neutraltweet_count = 0
#negativetweet_count = 0
#tweet_sentimentlist=[]  

#for ctweet in clean_list:
#    analysis = TextBlob(ctweet)
#    if analysis.sentiment.polarity > 0:
#        positivetweet_count+=1
#        sentiment = 'positive'
#    elif analysis.sentiment.polarity == 0:
#        neutraltweet_count+=1
#        sentiment = 'neutral'
#    elif analysis.sentiment.polarity < 0:
#        negativetweet_count+=1
#        sentiment = 'negative'
#    
#    tweet_sentimentlist.append({
#            'sentiment': sentiment,
#            'text': ctweet
#            }) 
#
#    
#with io.open("applesentiment.json",'w',encoding="utf-8") as outfile:
#   my_json_str = json.dumps(tweet_sentimentlist, ensure_ascii=False,indent=1)
#   if isinstance(my_json_str, str):
#        my_json_str = my_json_str.decode("utf-8")
#
#   outfile.write(my_json_str)
#    
#print(positivetweet_count)
#print(neutraltweet_count)  
#print(negativetweet_count)    

#********************************************************************************************

    
    





import streamlit as st
import pandas as pd
from transformers import pipeline
import tweepy
import os

# Set up Twitter API credentials
auth = tweepy.OAuthHandler(os.getenv("fJ1uQgqPfJUFRj1Oi5wzFNGUz"), os.getenv("xmQPuvzm1X6xgqKplDGCImd27AZC32oeDw4D6gpY50C57lE8iB"))
auth.set_access_token(os.getenv("1820100688262905857-NZAl8Ylc7a3RhHSxwYuMsuFEyU7du5"), os.getenv("3bvWkaqyp7aCG8toYVTXuWcKuf4h0xA0RcrRpLiQSZGLR"))
api = tweepy.API(auth)

# Initialize sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# Function to fetch tweets
def fetch_tweets(query, count=100):
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode="extended").items(count)
    return [tweet.full_text for tweet in tweets]

# Function to analyze sentiment
def analyze_sentiment(tweets):
    results = sentiment_analyzer(tweets)
    sentiments = [result['label'] for result in results]
    return pd.DataFrame({'Tweet': tweets, 'Sentiment': sentiments})

# Streamlit dashboard
def main():
    st.title("Real-Time Twitter Sentiment Analysis")
    st.subheader("Analyze sentiments on Twitter in real-time!")

    query = st.text_input("Enter the hashtag or keyword to search:", "#AI")
    tweet_count = st.slider("Number of tweets to analyze", min_value=10, max_value=100, step=10)

    if st.button("Fetch and Analyze"):
        with st.spinner("Fetching tweets..."):
            tweets = fetch_tweets(query, count=tweet_count)
            if tweets:
                with st.spinner("Analyzing sentiment..."):
                    df = analyze_sentiment(tweets)
                    st.success("Analysis complete!")

                    st.write("### Sentiment Distribution")
                    st.bar_chart(df['Sentiment'].value_counts())

                    st.write("### Sample Tweets")
                    st.write(df.head(10))
            else:
                st.warning("No tweets found.")

if __name__ == "__main__":
    main()

import csv
import sys
import os

def load_raw_data(filename):
    """
    Loads the CSV file into a list of dictionaries exactly as it is (messy).
    """
    if not os.path.exists(filename):
        print("Error: The file '" + filename + "' was not found.")
        sys.exit(1)

    raw_tweets = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = str(row.get("Text", "") or "").strip()
            likes = str(row.get("Likes", "") or "").strip()
            retweets = str(row.get("Retweets", "") or "").strip()
            username = str(row.get("Username", "") or "").strip()

            if text == "" and likes == "" and retweets == "" and username == "":
                continue

            raw_tweets.append(row)

    return raw_tweets

def clean_data(tweets):
    """
    QUEST 1: Handle missing fields.
    Check for missing text, and replace empty likes/retweets with 0.
    Return a clean list of tweets.
    """
    cleaned_tweets = []
    rows_removed = 0
    fields_fixed = 0

    for tweet in tweets:
        text_value = str(tweet.get("Text", "") or "").strip()
        likes_value = str(tweet.get("Likes", "") or "").strip()
        retweets_value = str(tweet.get("Retweets", "") or "").strip()

        if text_value == "":
            rows_removed = rows_removed + 1
            continue

        if likes_value == "":
            likes_value = "0"
            fields_fixed = fields_fixed + 1
        else:
            try:
                int(likes_value)
            except ValueError:
                likes_value = "0"
                fields_fixed = fields_fixed + 1

        if retweets_value == "":
            retweets_value = "0"
            fields_fixed = fields_fixed + 1
        else:
            try:
                int(retweets_value)
            except ValueError:
                retweets_value = "0"
                fields_fixed = fields_fixed + 1

        new_tweet = {}
        new_tweet["Tweet_ID"] = tweet.get("Tweet_ID", "")
        new_tweet["Username"] = tweet.get("Username", "")
        new_tweet["Text"] = text_value
        new_tweet["Retweets"] = retweets_value
        new_tweet["Likes"] = likes_value
        new_tweet["Timestamp"] = tweet.get("Timestamp", "")
        cleaned_tweets.append(new_tweet)

    print("Data Cleaning Report")
    print("--------------------")
    print("Rows removed:", rows_removed)
    print("Fields fixed:", fields_fixed)
    print("Tweets remaining:", len(cleaned_tweets))
    print()

    return cleaned_tweets

def find_viral_tweet(tweets):
    """
    QUEST 2: Loop through the list to find the tweet with the highest 'Likes'.
    Do not use the max() function.
    """
    pass

def custom_sort_by_likes(tweets):
    """
    QUEST 3: Implement Bubble Sort or Selection Sort to sort the list 
    by 'Likes' in descending order. NO .sort() allowed!
    """
    pass

def search_tweets(tweets, keyword):
    """
    QUEST 4: Search for a keyword and extract matching tweets into a new list.
    """
    pass

if __name__ == "__main__":
    dataset = load_raw_data("twitter_dataset.csv")

    if len(dataset) == 0:
        print("Error: The CSV file is empty. No tweets to analyze.")
        sys.exit(1)

    print("Loaded " + str(len(dataset)) + " raw tweets.\n")

    clean_dataset = clean_data(dataset)

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
            # skip totally empty rows
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

        # no text = remove the row
        if text_value == "":
            rows_removed = rows_removed + 1
            continue

        # likes
        if likes_value == "":
            likes_value = "0"
            fields_fixed = fields_fixed + 1
        else:
            try:
                int(likes_value)
            except ValueError:
                likes_value = "0"
                fields_fixed = fields_fixed + 1

        # retweets
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
    if len(tweets) == 0:
        print("Error: No tweets available to find a viral tweet.")
        return None

    # start with first tweet
    viral_tweet = tweets[0]
    highest_likes = int(viral_tweet["Likes"])

    i = 1
    while i < len(tweets):
        current_likes = int(tweets[i]["Likes"])
        if current_likes > highest_likes:
            highest_likes = current_likes
            viral_tweet = tweets[i]
        i = i + 1

    print("Viral Tweet")
    print("-----------")
    print("Username:", viral_tweet["Username"])
    print("Likes:", viral_tweet["Likes"])
    print("Text:", viral_tweet["Text"])
    print()

    return viral_tweet

def custom_sort_by_likes(tweets):
    """
    QUEST 3: Implement Bubble Sort or Selection Sort to sort the list 
    by 'Likes' in descending order. NO .sort() allowed!
    """
    # copy list first
    sorted_tweets = []
    for tweet in tweets:
        sorted_tweets.append(tweet)

    n = len(sorted_tweets)

    # bubble sort (highest likes first)
    i = 0
    while i < n - 1:
        j = 0
        while j < n - i - 1:
            left = int(sorted_tweets[j]["Likes"])
            right = int(sorted_tweets[j + 1]["Likes"])

            if left < right:
                temp = sorted_tweets[j]
                sorted_tweets[j] = sorted_tweets[j + 1]
                sorted_tweets[j + 1] = temp

            j = j + 1
        i = i + 1

    print("Top 10 Most Liked Tweets")
    print("------------------------")

    # print only top 10
    limit = 10
    if n < 10:
        limit = n

    k = 0
    while k < limit:
        t = sorted_tweets[k]
        print("Rank:", k + 1)
        print("Username:", t["Username"])
        print("Likes:", t["Likes"])
        print("Text:", t["Text"])
        print()
        k = k + 1

    return sorted_tweets

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

    # quest 1
    clean_dataset = clean_data(dataset)

    if len(clean_dataset) == 0:
        print("Error: No valid tweets left after cleaning.")
        sys.exit(1)

    # quest 2
    viral = find_viral_tweet(clean_dataset)

    # quest 3
    sorted_dataset = custom_sort_by_likes(clean_dataset)


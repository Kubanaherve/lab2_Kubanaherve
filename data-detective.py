import csv
import sys
import os

def load_raw_data(filename):
    """
    Loads the CSV file into a list of dictionaries exactly as it is (messy).
    I left it as it was since it does the work perfectly.
    """
    # I check if my file is really there first
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
        
    raw_tweets = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            raw_tweets.append(row)
    return raw_tweets

def clean_data(tweets):
    """
    QUEST 1: Handle missing fields.
    Check for missing text, and replace empty likes/retweets with 0.
    Return a clean list of tweets.
    """
    # I make a new list so I do not change the old one
    cleaned_tweets = []
    rows_removed = 0
    fields_fixed = 0

    # I go through every tweet and clean it one by one
    for tweet in tweets:
        text_value = tweet.get("Text", "")
        likes_value = tweet.get("Likes", "")
        retweets_value = tweet.get("Retweets", "")

        if text_value is None:
            text_value = ""
        if likes_value is None:
            likes_value = ""
        if retweets_value is None:
            retweets_value = ""

        text_value = str(text_value).strip()
        likes_value = str(likes_value).strip()
        retweets_value = str(retweets_value).strip()

        # If my tweet has no text I remove it
        if text_value == "":
            rows_removed = rows_removed + 1
        else:
            # I fix empty or bad Likes values here
            likes_is_valid = True

            if likes_value == "":
                likes_is_valid = False
            else:
                try:
                    likes_number = int(likes_value)
                    likes_value = str(likes_number)
                except ValueError:
                    likes_is_valid = False

            if likes_is_valid == False:
                likes_value = "0"
                fields_fixed = fields_fixed + 1

            # I do the same checks for Retweets
            retweets_is_valid = True

            if retweets_value == "":
                retweets_is_valid = False
            else:
                try:
                    retweets_number = int(retweets_value)
                    retweets_value = str(retweets_number)
                except ValueError:
                    retweets_is_valid = False

            if retweets_is_valid == False:
                retweets_value = "0"
                fields_fixed = fields_fixed + 1

            # I build my cleaned tweet and add it to my list
            new_tweet = {}
            new_tweet["Tweet_ID"] = tweet.get("Tweet_ID", "")
            new_tweet["Username"] = tweet.get("Username", "")
            new_tweet["Text"] = text_value
            new_tweet["Retweets"] = retweets_value
            new_tweet["Likes"] = likes_value
            new_tweet["Timestamp"] = tweet.get("Timestamp", "")

            cleaned_tweets.append(new_tweet)

    # I print my cleaning report
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

    # I start with the first tweet as my best one
    viral_tweet = tweets[0]
    highest_likes = int(viral_tweet["Likes"])

    # I compare each tweet myself one by one
    i = 1
    while i < len(tweets):
        current_tweet = tweets[i]
        current_likes = int(current_tweet["Likes"])

        if current_likes > highest_likes:
            highest_likes = current_likes
            viral_tweet = current_tweet

        i = i + 1

    # I show the viral tweet I found
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
    # I copy the tweets into my own list first
    sorted_tweets = []
    for tweet in tweets:
        sorted_tweets.append(tweet)

    n = len(sorted_tweets)

    # Bubble Sort: I compare neighbors and swap with a temp variable
    i = 0
    while i < n - 1:
        j = 0
        while j < n - i - 1:
            likes_left = int(sorted_tweets[j]["Likes"])
            likes_right = int(sorted_tweets[j + 1]["Likes"])

            # If the next tweet has more likes, I swap them
            if likes_left < likes_right:
                temp = sorted_tweets[j]
                sorted_tweets[j] = sorted_tweets[j + 1]
                sorted_tweets[j + 1] = temp

            j = j + 1
        i = i + 1

    # After sorting I only print the first 10 tweets
    print("Top 10 Most Liked Tweets")
    print("------------------------")

    if n < 10:
        top_count = n
    else:
        top_count = 10

    rank = 0
    while rank < top_count:
        tweet = sorted_tweets[rank]
        print("Rank:", rank + 1)
        print("Username:", tweet["Username"])
        print("Likes:", tweet["Likes"])
        print("Text:", tweet["Text"])
        print()
        rank = rank + 1

    return sorted_tweets

def search_tweets(tweets, keyword):
    """
    QUEST 4: Search for a keyword and extract matching tweets into a new list.
    """
    # I keep my matches in a new list
    matching_tweets = []

    # I ask the user for a search word
    keyword = input("Enter a keyword to search for: ")
    search_word = str(keyword).strip().lower()

    if search_word == "":
        print("Error: No keyword entered. Please type a word to search.")
        print()
        return matching_tweets

    # I check every tweet text one by one
    for tweet in tweets:
        tweet_text = tweet.get("Text", "")

        if tweet_text is None:
            tweet_text = ""

        tweet_text = str(tweet_text).lower()

        # check if the word is in the text
        if search_word in tweet_text:
            matching_tweets.append(tweet)

    # I print how many matches I found and then show them
    print("Keyword Search Results")
    print("----------------------")
    print("Matches found:", len(matching_tweets))
    print()

    match_number = 0
    while match_number < len(matching_tweets):
        tweet = matching_tweets[match_number]
        print("Match:", match_number + 1)
        print("Username:", tweet["Username"])
        print("Likes:", tweet["Likes"])
        print("Text:", tweet["Text"])
        print()
        match_number = match_number + 1

    return matching_tweets

if __name__ == "__main__":
    # I load my messy data first
    dataset = load_raw_data("twitter_dataset.csv")

    if len(dataset) == 0:
        print("Error: The CSV file is empty. No tweets to analyze.")
        sys.exit(1)

    print("Loaded " + str(len(dataset)) + " raw tweets.\n")

    # Quest 1: I clean my data
    clean_dataset = clean_data(dataset)

    if len(clean_dataset) == 0:
        print("Error: No valid tweets left after cleaning.")
        sys.exit(1)

    # Quest 2: I find the tweet with the most likes
    viral = find_viral_tweet(clean_dataset)

    # Quest 3: I sort by likes and show my top 10
    sorted_dataset = custom_sort_by_likes(clean_dataset)

    # Quest 4: I ask for a keyword and search my tweets
    search_results = search_tweets(clean_dataset, "")

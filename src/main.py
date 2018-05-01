
# INI BUAT FETCH TWEETS DAN TERIMA-KIRIM PARAMETER PHP-PYTHON
## Import tools and API
import twitter
import json
import sys
## Import Pattern 
import BM
import KMP
import RE

# Configurate keys
def read_config_file(filename):
    with open(filename, "r") as f:
        s = f.read()
    d = json.loads(s)
    APP_KEY = d["APP_KEY"]
    APP_SECRET = d["APP_SECRET"]
    TOKEN_KEY = d["TOKEN_KEY"]
    TOKEN_SECRET = d["TOKEN_SECRET"]
    return APP_KEY, APP_SECRET, TOKEN_KEY, TOKEN_SECRET

# Check is a tweet contains certain keyword and add parameter IS_SPAM to check if current tw
def SpamDetector(tweet, keywords, chosenAlgo):
    if (chosenAlgo == 1):
        tweet['IS_SPAM'] = KMP.KMPMatching(tweet["full_text"], keywords) != -1
    elif (chosenAlgo == 2):
        tweet['IS_SPAM'] = BM.BMMatching(tweet["full_text"], keywords) != -1
    else:
        tweet['IS_SPAM'] = RE.regex(tweet["full_text"], keywords) != None
    return tweet

def ExpandTweet(tweet):
    # Expand retweeted tweet
    if ('retweeted_status' in tweet):
        tweet['full_text'] = tweet['retweeted_status']['full_text']
        tweet['RT'] = True
    else :
        tweet['RT'] = False 
    return tweet


# Main Program
if __name__ == '__main__':
    ## RECEIVE PARAMETER FROM PHP
    keywords = sys.argv[1]
    chosenAlgo = int(sys.argv[2])
    
    if (chosenAlgo <=2):
        keywords = keywords.split(',')
        i = 0
        for keyword in keywords:
            keywords[i] = keyword.strip()
            i += 1
    # CONFIG TWITTER API
    APP_KEY, APP_SECRET, TOKEN_KEY, TOKEN_SECRET = read_config_file("test/config.json")
    api = twitter.Api(consumer_key=APP_KEY, consumer_secret=APP_SECRET,
                    access_token_key=TOKEN_KEY,access_token_secret=TOKEN_SECRET, tweet_mode='extended')
    # FETCH TWEETS INTO JSON
    tweets = api.GetSearch(term="gue", result_type="recent", count=100, return_json=True)
    # BUAT TEST BACA JSON
    with open("test/tuit.json", "w") as outfile:
        json.dump(tweets, outfile, indent=4)
    
    #pass to PHP
    data = []
    for tweet in tweets["statuses"]:
        #Delete unnecessary attributes of a tweet
        del tweet["entities"]
        del tweet["in_reply_to_status_id"]
        del tweet["in_reply_to_status_id_str"]
        del tweet["metadata"]
        del tweet["in_reply_to_user_id"]
        del tweet["in_reply_to_user_id_str"]
        del tweet["in_reply_to_screen_name"]

        data.append(tweet) # Add tweet data to json file           
        tweet = ExpandTweet(tweet)
        tweet = SpamDetector(tweet, keywords, chosenAlgo)
    
    # PASS TO JSON DATA TO PHP
    print(json.dumps(data))
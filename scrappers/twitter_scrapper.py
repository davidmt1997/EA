import twitter

# Twitter API keys
api = twitter.Api(consumer_key="FkqzuXTPFTelpza9HJ0bmd1CL",
                  consumer_secret="ZZfpwHoIIGG5N3rDizpjpRkHmWyQVEPIQw27ACTSr2kwKcqyYq",
                  access_token_key="1320016637576253440-WvzyoZj3yZ1qBditHGrE1rSHGMXcwb",
                  access_token_secret="zVGKv1EaeaaX4r0VTbP4mMiIuYLuhe1ws9pdirpdn2Zxk")

'''
Returns the number of followers, average retweet count and average favorite count (of the last 200 tweets) of a given page
''' 
def get_twitter_info(account):
    rt_count = 0
    fav_count = 0
    count = 0
    user = api.GetUser(screen_name=account, return_json=True)

    # Get the user timeline and the last 200 tweets
    tm = api.GetUserTimeline(screen_name=account, count=200)
    tweets = [i.AsDict() for i in tm]
    # Parse tweets status to get the follower, number of rts and favs
    for t in tweets: 

        # Check for tweets only by the main account, no replies or retweets to other accounts
        try:
            if t['in_reply_to_screen_name']:
                continue
        except KeyError:
            pass
        finally:

            if t['text'][:2] != "RT":
                try:
                    rt_count += int(t['retweet_count'])
                    fav_count += int(t['favorite_count'])
                    count += 1

                except KeyError:
                    pass
        
    return int(user["followers_count"]), (rt_count / count), (fav_count / count)
    
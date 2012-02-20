@Title: jweepy
@author: jay
@Version: 0.1

WARNING: It's kind of messy. Too many options loaded and yeah name's also weird!

First add your consumer_key, consumer_secret, access_token_key, acees_token_secret.
Find this at https://dev.twitter.com

Configure Proxies if any.

Modules/Libraries Required: twitter(Google-API)

0. Get Primary details.
  
  0.1 Get User
    
    get_user(string=None)
    
    if provided a username, it will return a twitter.User object corresponding the provided username
    
  0.2  Get Followers
    
    getfollowers()
    
    Returns a list of all of your followers as twitter.User objects
    
  0.3 Get Following/Friends
  
    getfollowing()
    
    Returns a list of all of your friends as twitter.User objects

1.To see timeline:

  1.1 See the timeline.
    
    show_friends_timeline(since_ids=None, hashtag_list = None, hashtag_db_name = None, tweet_db_name = None)

    since_ids - twitter.Status.id (the timeline will consist of all the tweets after the tweet with id as since_ids)
    hashtag_list - A list of hashtags if you want to search for particular hashtags
    hashtag_db_name - Provide a string name, If you want to save the hashtags and the counts. It will be stored in a gdbm file.
    tweet_db_name - Provide a string name, If you want to save the tweets hashtags and the tweet id. It will be stored in a gdbm file.

    Returns the tweet id of the latest tweet.

  1.2 See some user's timeline.
  
    show_user_timeline(user, since_ids = None, hashtag_list = None, hashtag_db_name = None, tweet_db_name = None)
    
    user - twitter.User object
    since_ids - twitter.Status.id (the timeline will consist of all the tweets after the tweet with id as since_ids)
    hashtag_list - A list of hashtags if you want to search for particular hashtags
    hashtag_db_name - Provide a string name, If you want to save the hashtags and the counts. It will be stored in a gdbm file.
    tweet_db_name - Provide a string name, If you want to save the tweets hashtags and the tweet id. It will be stored in a gdbm file.
    
    Returns the tweet id of the latest tweet.
  
  1.3 See Public timeline.
    
    show_public_timeline(since_ids = None,  hashtag_list = None, hashtag_db_name = None, tweet_db_name = None)
    
    user - twitter.User object
    since_ids - twitter.Status.id (the timeline will consist of all the tweets after the tweet with id as since_ids)
    hashtag_list - A list of hashtags if you want to search for particular hashtags
    hashtag_db_name - Provide a string name, If you want to save the hashtags and the counts. It will be stored in a gdbm file.
    tweet_db_name - Provide a string name, If you want to save the tweets hashtags and the tweet id. It will be stored in a gdbm file.
    
    Returns the tweet id of the latest tweet.
    
2. See Continuous Timeline.

  2.1 See continuous timeline.
  
    set_continuous_timeline(since_ids=None, hashtag_list = None, hashtag_db_name = None, tweet_db_name = None)
    
    since_ids - twitter.Status.id (the timeline will consist of all the tweets after the tweet with id as since_ids)
    hashtag_list - A list of hashtags if you want to search for particular hashtags
    hashtag_db_name - Provide a string name, If you want to save the hashtags and the counts. It will be stored in a gdbm file.
    tweet_db_name - Provide a string name, If you want to save the tweets hashtags and the tweet id. It will be stored in a gdbm file.
    
    It will run indefinitely untill KeyboardInterrupt is provided. (^c)
    
    Returns the tweet id of the latest tweet.
  
  2.2 See user's continuous timeline.
  
    set_continuous_user_timeline(user, since_ids = None, hashtag_list = None, hashtag_db_name = None, tweet_db_name = None)
    
    user - twitter.User object
    since_ids - twitter.Status.id (the timeline will consist of all the tweets after the tweet with id as since_ids)
    hashtag_list - A list of hashtags if you want to search for particular hashtags
    hashtag_db_name - Provide a string name, If you want to save the hashtags and the counts. It will be stored in a gdbm file.
    tweet_db_name - Provide a string name, If you want to save the tweets hashtags and the tweet id. It will be stored in a gdbm file.
    
    It will run indefinitely untill KeyboardInterrupt is provided. (^c)
    
    Returns the tweet id of the latest tweet.
    
  2.3 See public continuous timeline.
  
    set_continuous_public_timeline(since_ids = None, hashtag_list = None, hashtag_db_name = None, tweet_db_name = None)
    
    since_ids - twitter.Status.id (the timeline will consist of all the tweets after the tweet with id as since_ids)
    hashtag_list - A list of hashtags if you want to search for particular hashtags
    hashtag_db_name - Provide a string name, If you want to save the hashtags and the counts. It will be stored in a gdbm file.
    tweet_db_name - Provide a string name, If you want to save the tweets hashtags and the tweet id. It will be stored in a gdbm file.
    
    It will run indefinitely untill KeyboardInterrupt is provided. (^c)
    
    Returns the tweet id of the latest tweet.

3. Search hashtags(Search multiple hashtags in timelines)
  
  search_hashtags(hashtag_list, flag = 1, hashtag_db_flag = 1, ids = None, user = None, hashtag_db_name = None, tweet_db_name = None)
  
  hashtag_list - A list of hashtags(must be string)
  flag -  flag = 1 : Search hashtags in timeline.
          flag = 2 : Search hashtags in user's timeline.
          flag = 3 : Search hashtags in public timeline
  hashtag_db_flag - flag = 0  : Doesn't store hashtags
                    flag != 0 : Stroe hashtags
  ids - twitter.Status.id (the hashtags will be searched in tweets after the tweet with id as since_ids)
  user - if flag == 2: twitter.User object
  hashtag_db_name - 
    if flag == 1: 
      if hashtag_db_flag != 0 : Store hashtags and counts in a gdbm file with given string. If None, hashtag_db_flag = 'hashtag_timeline'
    if flag == 2:
      if hashtag_db_flag != 0 : Store hashtags and counts in a gdbm file with given string. If None, hashtag_db_flag = username
    if flag == 3:
      if hashtag_db_flag != 0 : Store hashtags and counts in a gdbm file with given string. If None, hashtag_db_flag = 'hashtag_public'
  tweet_db_name - If provided, it will store all the tweets containing the provided hashtags in a gdbm file with tweet ids.
                  else, it will not store the tweets.
                  
  It will run indefinitely untill Keyboard Interrupt (^c) is provided.
  
  Returns the id of the latest tweet.
                  
4. Get Conversation.

  get_conv(user_list, hashtag_db_name, tweet_db_name = None)
  
  user_list - A list containing twitter.User objects
  hashtag_db_name - A string name for gdbm file which will save all the hashtags and counts.
  tweet_db_name - If a string provided, all the tweets with hashtags will be stored in the gdbm file with tweet ids.
  
  It will run indefinitely untill Keyboard Interrupt (^c) is provided.
  
  Returns nothing

# -*- coding: utf-8 -*-

import twitter
import urllib2
import time
import re
import gdbm

opener = urllib2.build_opener()
urllib2.install_opener(opener)

api = twitter.Api(consumer_key="", consumer_secret="",access_token_key="", access_token_secret="",proxy ={})

def get_proxy_urllib(Proxy=None):
    if not Proxy:
        proxy = urllib2.ProxyHandler({}) # your proxy here
    else:   
        proxy = urllib2.ProxyHandler(Proxy)
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    return urllib2

def get_user(string):
    '''if provided a username, it will return a twitter.User object corresponding the provided username'''
    user = api.GetUser(string)
    return user    
    
def getfollowers():
    '''Returns a list containing all followers as twitter.User'''
    followers = api.GetFollowers()
    return followers

def getfollowing():
    '''Returns a list containing all followings/friends as twitter.User'''
    following = api.GetFriends()
    return following
    
def get_user_pic(user):
    '''Returns the URL of display picture of the twitter.User'''
    image_url = user.profile_image_url
    page = opener.open(image_url)
    f = open(user.screen_name+'.jpg','wb')
    f.write(page.read())
    f.close()
    return

def get_user_status(user):
    '''Returns the status as twitter.Status of twitter.User'''
    return user.status
    
def get_status_detail(status):
    '''Returns a tuple (status.id, status.text,status.location,status.user,status.urls,status.user_mentions,status.hashtags) of twitter.Status'''
    return(status.id, status.text,status.location,status.user,status.urls,status.user_mentions,status.hashtags)
    
def show_friends_timeline(since_ids=None, hashtag_list = None, hashtag_db_name=None, tweet_db_name = None):
    '''since_ids - twitter.Status.id (the timeline will consist of all the tweets after the tweet with id as since_ids)
    hashtag_list - A list of hashtags if you want to search for particular hashtags
    hashtag_db_name - Provide a string name, If you want to save the hashtags and the counts. It will be stored in a gdbm file.
    tweet_db_name - Provide a string name, If you want to save the tweets hashtags and the tweet id. It will be stored in a gdbm file.

    Returns the tweet id of the latest tweet.
    '''
    timeline = api.GetFriendsTimeline(since_id = since_ids)
    if not timeline:
        return since_ids
    hashtag_timeline_db = None
    tweet_db = None
    if hashtag_db_name:
        hashtag_timeline_db = gdbm.open(hashtag_db_name,'c')
    if tweet_db_name:
        tweet_db = gdbm.open(tweet_db_name,'c')
    
    since_ids = show_timeline(timeline, hashtag_db = hashtag_timeline_db, tweet_db = tweet_db ,hashtag_list = hashtag_list)
    if hashtag_db_name:
        hashtag_timeline_db.close()
    if tweet_db_name:
        tweet_db.close()
    return since_ids

def set_continuous_timeline(since_ids=None, hashtag_list = None, hashtag_db_name = None, tweet_db_name = None):
    '''
    since_ids - twitter.Status.id (the timeline will consist of all the tweets after the tweet with id as since_ids)
    hashtag_list - A list of hashtags if you want to search for particular hashtags
    hashtag_db_name - Provide a string name, If you want to save the hashtags and the counts. It will be stored in a gdbm file.
    tweet_db_name - Provide a string name, If you want to save the tweets hashtags and the tweet id. It will be stored in a gdbm file.
    
    It will run indefinitely untill KeyboardInterrupt is provided. (^c)
    
    Returns the tweet id of the latest tweet.
    '''    
    try:
        if not since_ids:
            since_ids = None
        while 1:
            since_ids = show_friends_timeline(since_ids, hashtag_list = hashtag_list, hashtag_db_name = hashtag_db_name, tweet_db_name = tweet_db_name )
            time.sleep(15)
    except KeyboardInterrupt:
        return since_ids

def show_user_timeline(user, since_ids = None, hashtag_list = None, hashtag_db_name = None, tweet_db_name = None):
    '''
    user - twitter.User object
    since_ids - twitter.Status.id (the timeline will consist of all the tweets after the tweet with id as since_ids)
    hashtag_list - A list of hashtags if you want to search for particular hashtags
    hashtag_db_name - Provide a string name, If you want to save the hashtags and the counts. It will be stored in a gdbm file.
    tweet_db_name - Provide a string name, If you want to save the tweets hashtags and the tweet id. It will be stored in a gdbm file.
    
    Returns the tweet id of the latest tweet.
    '''
    if not user:
        return since_ids
    if not user.protected:
        try:
            timeline = api.GetUserTimeline(user.id, since_id = since_ids)
        except ValueError:
            print 'ValueError'
    else:
        return since_ids
    if not timeline:
        return since_ids
    hashtag_user_db = None
    if hashtag_db_name:
 #       print hashtag_db_name
        hashtag_user_db = gdbm.open(hashtag_db_name+'_hashtag','c')
    if tweet_db_name:
        tweet_user_db = gdbm.open(tweet_db_name+'_tweets','c')
        
    since_ids = show_timeline(timeline, hashtag_db = hashtag_user_db, tweet_db = tweet_user_db, hashtag_list = hashtag_list)
    if hashtag_db_name:
        hashtag_user_db.close()
    if tweet_db_name:
        tweet_user_db.close()
    return since_ids
    
def set_continuous_user_timeline(user, since_ids = None, hashtag_list = None, hashtag_db_name = None, tweet_db_name = None ):
    '''
    user - twitter.User object
    since_ids - twitter.Status.id (the timeline will consist of all the tweets after the tweet with id as since_ids)
    hashtag_list - A list of hashtags if you want to search for particular hashtags
    hashtag_db_name - Provide a string name, If you want to save the hashtags and the counts. It will be stored in a gdbm file.
    tweet_db_name - Provide a string name, If you want to save the tweets hashtags and the tweet id. It will be stored in a gdbm file.
    
    It will run indefinitely untill KeyboardInterrupt is provided. (^c)
    
    Returns the tweet id of the latest tweet.
    '''    
    if not user:
        return since_ids
    
    try:
        while 1:
 #           print hashtag_db_name
            since_ids = show_user_timeline(user, since_ids, hashtag_list = hashtag_list, hashtag_db_name = hashtag_db_name, tweet_db_name = None)
            time.sleep(30)
    except KeyboardInterrupt:
        return since_ids
        
def show_public_timeline(since_ids = None,  hashtag_list = None, hashtag_db_name = None, tweet_db_name = None):
    '''
    user - twitter.User object
    since_ids - twitter.Status.id (the timeline will consist of all the tweets after the tweet with id as since_ids)
    hashtag_list - A list of hashtags if you want to search for particular hashtags
    hashtag_db_name - Provide a string name, If you want to save the hashtags and the counts. It will be stored in a gdbm file.
    tweet_db_name - Provide a string name, If you want to save the tweets hashtags and the tweet id. It will be stored in a gdbm file.
    
    Returns the tweet id of the latest tweet.
    '''
    timeline = api.GetPublicTimeline(since_id = since_ids)
    if not timeline:
        return since_ids
    hashtag_public_db = None
    tweet_db = None
    if hashtag_db_name:
        hashtag_public_db = gdbm.open(hashtag_db_name,'c')
    if tweet_db_name:
        tweet_db = gdbm.open(tweet_db_name,'c')
    since_ids = show_timeline(timeline, hashtag_list = hashtag_list, hashtag_db = hashtag_public_db, tweet_db = tweet_db)
    if hashtag_db_name:
        hashtag_public_db.close()
    if tweet_db_name:
        tweet_db.close()
    return since_ids

def set_continuous_public_timeline(since_ids = None, hashtag_list = None, hashtag_db_name = None, tweet_db_name = None):
    '''
    since_ids - twitter.Status.id (the timeline will consist of all the tweets after the tweet with id as since_ids)
    hashtag_list - A list of hashtags if you want to search for particular hashtags
    hashtag_db_name - Provide a string name, If you want to save the hashtags and the counts. It will be stored in a gdbm file.
    tweet_db_name - Provide a string name, If you want to save the tweets hashtags and the tweet id. It will be stored in a gdbm file.
    
    It will run indefinitely untill KeyboardInterrupt is provided. (^c)
    
    Returns the tweet id of the latest tweet.
    '''
    try:
        count = 0
        if not since_ids:
            since_ids = None
        while 1:
            since_ids = show_public_timeline(since_ids, hashtag_list = hashtag_list, hashtag_db_name = hashtag_db_name, tweet_db_name = tweet_db_name)
            count = count+1
            time.sleep(1)
            if count > 60:
                break
    except KeyboardInterrupt:
        return since_ids 
        
def show_timeline(timeline, hashtag_db=None, tweet_db = None, hashtag_list=None):
    for i in range(len(timeline)-1,-1,-1):
        ids = timeline[i].id
        screen_name = '@'+timeline[i].user.screen_name
        user_name = timeline[i].user.name
        text = timeline[i].text
        tweet = screen_name+' ('+user_name+') '+': '+text
        print tweet
        res = get_hashtag(text)
        if hashtag_list:
            for j in range(len(hashtag_list)):
                if not hashtag_list[j].startswith('#'):
                    hashtag_list[j]='#'+hashtag_list[j]
                if hashtag_list[j] in res:
             #      print "opening",hashtag_list[j]+"_hashtag"
                    py_db = gdbm.open(hashtag_list[j]+'_hashtag','c')
                    py_db[str(timeline[i].id)] = repr(tweet)
                    py_db.close()
        if res:
  #          print hashtag_db
            if hashtag_db is not None:
   #             print 'save_hashtag'
                hashtag_db = save_hashtag(res, hashtag_db)
            if tweet_db is not None:
                tweet_db = save_tweet(ids, tweet, tweet_db)
    return timeline[0].id

def get_hashtag(tweet):
    hashtag = re.compile(u"#\w+")
    res = re.findall(hashtag, tweet)
    for i in range(len(res)):
        res[i] = res[i].lower()
    print res
    return res
    
def save_hashtag(res, db):
    for i in range(len(res)):
        try:
            count = int(db[res[i]])
            count = count + 1
            db[res[i]] = str(count)
        except KeyError:
            db[res[i]] = '1'
    return db

def save_tweet(ids, tweet, db):
    print tweet
    try:
        db[str(ids)] = tweet
    except TypeError:
        print 'typeerror'
    return db
    

def search_hashtags(hashtag_list, flag = 1, hashtag_db_flag = 1, ids = None, user = None, hashtag_db_name = None, tweet_db_name = None):
    '''
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
    '''
    if hashtag_list:
        for i in range(len(hashtag_list)):
            hashtag_list[i] = hashtag_list[i].lower()
            if not hashtag_list[i].startswith('#'):
                hashtag_list[i] = '#'+hashtag_list[i]
    if flag == 1:
        if hashtag_db_flag:
            if not hashtag_db_name:
                hashtag_db_name = 'hashtags_timeline'
        ids = set_continuous_timeline(ids, hashtag_list, hashtag_db_name = hashtag_db_name, tweet_db_name = tweet_db_name)
    if flag == 2:
        print 'user hashtags'
        if not user:
            print 'No user provided'
            return ids
        if hashtag_db_flag:
            if hashtag_db_name is not None:
                hashtag_db_name = hashtag_db_name
            else:
                hashtag_db_name = user.screen_name
        else:
            hashtag_db_name = None
#        print hashtag_db_name
        ids = set_continuous_user_timeline(user, ids, hashtag_list, hashtag_db_name = hashtag_db_name, tweet_db_name = tweet_db_name)
        
    if flag == 3:
        if hashtag_db_flag:
            if not hashtag_db_name:
                hashtag_db_name = 'hashtags_public'
        ids = set_continuous_public_timeline(ids, hashtag_list = hashtag_list, hashtag_db_name = hashtag_db_name, tweet_db_name = tweet_db_name)
    return ids

def get_conv(user_list, hashtag_db_name, tweet_db_name = None) :
    '''
user_list - A list containing twitter.User objects
hashtag_db_name - A string name for gdbm file which will save all the hashtags and counts.
tweet_db_name - If a string provided, all the tweets with hashtags will be stored in the gdbm file with tweet ids.
  
It will run indefinitely untill Keyboard Interrupt (^c) is provided.
  
Returns nothing
    '''
    if not user_list:
        return
    try:
        ids = len(user_list)*[None]
        while 1:
            for i in range(len(user_list)):
                time.sleep(2)
                ids[i] = show_user_timeline(user=user_list[i], since_ids = ids[i], hashtag_db_name = hashtag_db_name, tweet_db_name = tweet_db_name, hashtag_list = None)
                #ids[i] = search_hashtags(ids = ids[i], flag=2,hashtag_db_flag=1,user=user_list[i],hashtag_db_name = hashtag_db_name)
    except KeyboardInterrupt:
        return
    
def get_user_profile(user):
    user_id = user.id
    name = user.name
    screen_name = user.screen_name
    des = user.description
    protected = user.protected
    image_url = user.profile_image_url
    user_url = user.url
    status = user.status
    status_count = user.statuses_count
    followers_count = user.followers_count
    friends_count = user.friends_count
    
    return(user, user_id, name, screen_name, des, protected, image_url, user_url, status, status_count, followers_count, friends_count)
    
def get_tweet_profile(status):
    t = status.created_at
    f = status.favorited
    in_reply_to = (status.in_reply_to_screen_name, status.in_reply_to_user_id, status.in_reply_to_status_id)
    source = status.source
    status_id = status.id
    tweet = status.text
    user = status.user
    user_mentions = status.user_mentions
    
    return(status_id, tweet, user, in_reply_to, user_mentions, f, t)

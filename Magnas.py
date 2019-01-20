import time
import tweepy
from tweepy import OAuthHandler
import json 
import sys

#Fill in with your twiiter Dev Account data
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

#Search query
username= ''
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
user = api.get_user(screen_name = username)


print("")
print('Name: ' + user.name)
print('Friends: ' + str(user.friends_count))
print('Tweets: ' + str(user.statuses_count))
print('')


userTweets = 1000 #number of users tweets to pull from
sampleSize = 1000 #number of replies to pull

batchSize = 200 #number of tweets to pull in each page


CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


#Get user tweets to check replies against, store in dictionary
tweets = tweepy.Cursor(api.user_timeline, screen_name = username,  include_rts = False).items()

data = {}
data["author"] = username
data["tweets"] = {}
tweetCounter = 0
print("Getting user tweets...")
for status in tweets:
	if tweetCounter < userTweets:
		data["tweets"][status.id] = {}
		data["tweets"][status.id]["text"] = status.text.encode("utf-8")
		data["tweets"][status.id]["replies"] = []
		tweetCounter += 1

		sys.stdout.write("\r" + str(tweetCounter) + "/" + str(userTweets) + "    " + str(tweetCounter/(userTweets/100)) + "%")
		sys.stdout.flush()
	else:
		break
print("")
print("")
print("Getting replies...")



#Get tweets @user, and check if they are replies to a tweet that the user made. If so, store in the dicitonary under that tweet.
c = tweepy.Cursor(api.search, q="@" + username, count=batchSize)
totalCounter = 0
replyCounter = 0
rateLimitCounter = 0

while replyCounter < sampleSize:
	try:
		for reply in c.items():
			if replyCounter < sampleSize:
				if reply.in_reply_to_status_id is not None:
					if rateLimitCounter != 0:
						rateLimitCounter = 0
						sys.stdout.write("\r" + ERASE_LINE)
						sys.stdout.write(CURSOR_UP_ONE)
					if int(reply.in_reply_to_status_id) in data["tweets"]:
						data["tweets"][int(reply.in_reply_to_status_id)]["replies"].append(reply.text.encode("utf-8"))
						totalCounter += 1
						replyCounter += 1
						sys.stdout.write("\r" + "Tweet: " + str(totalCounter) + "    " + str(replyCounter) + "/" + str(sampleSize) + "    " + str(replyCounter/(sampleSize/100)) +"%")
						sys.stdout.flush()
					else:
						totalCounter += 1
						sys.stdout.write("\r" + "Tweet: " + str(totalCounter) + "    " + str(replyCounter) + "/" + str(sampleSize) + "    " + str(replyCounter/(sampleSize/100)) +"%")
						sys.stdout.flush()
				lastTime = time.time()
			else:
				break

	except tweepy.TweepError:
		if rateLimitCounter == 0:
			sys.stdout.write("\n")
		sys.stdout.write("\r -- Rate Limit Exceeded, Waiting for Clearance...  (" + str(rateLimitCounter) +"/15)")
		rateLimitCounter += 1
		time.sleep(60)
		continue

	except StopIteration:
		print("Not enough @tweets to match sampleSize")
		break

print("")
print("")
print("Data exported to data.txt")




with open('data.txt', 'w') as outfile:
	json.dump(data, outfile)


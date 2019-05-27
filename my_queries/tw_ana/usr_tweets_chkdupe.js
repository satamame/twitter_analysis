var user_id = 278941157
print('For user# ' + user_id)
print("Count : " + db.usr_tweets.find({'user.id': user_id}).count())
print("IDs   : " + db.usr_tweets.distinct("id", {'user.id': user_id}).length)
var tweet_id = (db.usr_tweets.findOne({'user.id': user_id}, {id: 1}))['id']
print("t-id#1: " + tweet_id)
print("Dupe  : " + db.usr_tweets.find({id: tweet_id}, {text: 1}).count())
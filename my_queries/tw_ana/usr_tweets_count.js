print("Count: " + db.usr_tweets.find({}).count())
print("IDs  : " + db.usr_tweets.distinct('id').length)
print("Words: " + db.usr_tweets.find({words: {$exists: true}}).count())
print("IDs  : " + db.usr_tweets.distinct('id', {words: {$exists: true}}).length)
print("Samples : " + db.users.find({used_as_sample: true}).count())
print("w/tweets: " + db.users.find({tweet_count: {$gt: 0}}).count())
print(">= 1000 : " + db.users.find({tweet_count: {$gt: 999}}).count())
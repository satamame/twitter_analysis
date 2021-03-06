print("Count:      " + db.usr_tweets.find({}).count())
// print("Users:      " + db.usr_tweets.aggregate([{$group: {_id: '$user.id', count: { $sum: 1 }}}], {allowDiskUse:true, corsor:{}}).count())
print("test user:  " + db.usr_tweets.aggregate([{$match: {test_data: true}}, {$group: {_id: '$user.id', count: { $sum: 1 }}}], {allowDiskUse:true, corsor:{}}).count())
print("test_data:  " + db.usr_tweets.find({test_data: true}).count())
// print("with words: " + db.usr_tweets.find({test_data: true, words: {$exists: true}}).count())
print("with topic: " + db.usr_tweets.find({test_data: true, words: {$exists: true}, topic_id: {$exists: true}, topic_prob: {$exists: true}}).count())
print("prob >= .5: " + db.usr_tweets.find({test_data: true, words: {$exists: true}, topic_id: {$exists: true}, topic_prob: {$gte: 0.5}}).count())
print("Count: " + db.tw_samples.find({}).count())
print("IDs  : " + db.tw_samples.distinct('id').length)
print("Words: " + db.tw_samples.find({words: {$exists: true}}).count())
print("IDs  : " + db.tw_samples.distinct('id', {words: {$exists: true}}).length)
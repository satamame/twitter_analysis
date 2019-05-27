print("Count: " + db.users.find({}).count())
print("IDs  : " + db.users.distinct("user.id").length)
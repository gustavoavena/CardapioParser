from persistence.firebase import setup_firebase


db = setup_firebase()

tokens = db.child('tokens').get().val()


for t, d in tokens.items():
    d["almoco"] = "11:00"
    d["jantar"] = "17:00"


db.child('tokens').set(tokens)
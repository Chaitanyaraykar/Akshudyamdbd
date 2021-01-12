from flask import Flask , jsonify


class RLocation:
    def __init__(self, key, name, lat, lng):
        self.key = key
        self.name = name
        self.lat = lat
        self.lng = lng
        self.contact = ""


class OLocation():
    def __init__(self, key, name, lat, lng, contact):
        self.key = key
        self.name = name
        self.lat = lat
        self.lng = lng
        self.contact = contact


class PLocation():
    def __init__(self, key, name, lat, lng, contact, foodq):
        self.key = key
        self.name = name
        self.lat = lat
        self.lng = lng
        self.contact = contact
        self.foodq = foodq

class Blog():
    def __init__(self, user, blog):
        self.user = user
        self.blog = blog


# class PVinfo:
#     def Foodtrans(self):
#         pvinstance={
#             "_id" : uuid.uuid4().hex,
#             "producername" :"gunda",
#             "producercontact" : "9874563215",
#             "volunteername" : "Durgesh",
#             "volunteergender" : "Male",
#             "foodamount": 5
#         }

#         db.pvinstance.insert_one(pvinstance)


#         return jsonify(pvinstance) , 200
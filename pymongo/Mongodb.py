import pymongo

myclient = pymongo.MongoClient('mongodb://192.168.56.1:60000')#ip du mongos
mydb = myclient['test']#id the la db
mycol = mydb["books"]#id de la collection



for i in range (50):
    mydict = { "title" : "Harry Potter "+str(i), "language" : "French"}
    print(mycol.insert_one(mydict))

insert = mycol.insert_one({ "title" : "Harry Potter 0", "language" : "French"})
find = mycol.find_one({"title":"Harry Potter 0"})
delete = mycol.delete_one({"title":"Harry Potter 0"})

print(find)#print la cmd voulue

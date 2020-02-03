from pymongo import MongoClient
from collections import defaultdict
db_url="mongodb://crescent:123456cre@ds353457.mlab.com:53457/comp9900"
client=MongoClient(db_url,connectTimeoutMS=30000)
db=client["comp9900"]
userd=db.users
propd=db.property
userls=["name","password","username","phone","pay_card","history","likes","owner","properties","description"]

def check_log(username,pass_word): #for login
    result=search_one(username,item_s="username")
    if result==None:
        return 0
    else:
        if (pass_word == result["password"]):
            dict_temp = result.copy()
            del dict_temp['_id']
            #print(dict_temp)
            return dict_temp
        else:
            return 0

def search_one(content_s,item_s=None): #items:address,content_s:7 hunston rd.
    #print(type(item_s))
    if item_s==None:
        item_s="username"
    if item_s in userls:
        records=userd.find_one({item_s:content_s})
    else:
        records=propd.find_one({item_s:content_s})
    return records

def updateRecord(record, updates):
    userd.update_one({'username':record["username"]},{
                              '$set': updates
                              }, upsert=False)

def change(chg):
#chg={"a":"1","b":'test',"c":''}
    keys = list(chg.keys())
    for key in keys: #del which==None
        if chg[key]=='':
            del(chg[key])
    #print('after del..is:',chg)
    record=search_one(chg["username"],"username")
    updateRecord(record, chg)

#check_log("test@gmial.com","1234")
def search_likes(inside):
    nprop=inside.split(",")#split->list
    all_list=[]
    for i in nprop:
        #print (search_one(i,"address"))
        tp=search_one(i,"address") #get the whole info of this address
        if tp is not None:
            lis=[]
            #print(tp["address"])
            lis.append(tp["address"])
            lis.append(tp["title"])
            #bath split out
            cbath=0
            s=set(tp["service"].split(","))
            if "g_bath" in s:
                cbath+=1
                if "d_bath" in s:
                    cbath+=1
            lis.append(cbath)
            lis.append(tp["size"])
            lis.append(tp["capacity"])
            #parking split out
            cparking=0
            if "parking" in s:
                cparking+=1
            lis.append(cparking)
            lis.append(tp["price"])
            lis.append(tp["pictures"])
            all_list.append(lis)
        else:
            print("nonetype address",i)
    return all_list


def search_property(chose):
    print(chose)
    t_set = set(chose)

    # prop_d={}
    prop_d = defaultdict(list)
    for i in propd.find():
        # print (i['service'])
        # print ('check here:',i['suburb']) #Castle Hill
        # prop_d['suburb']=i['suburb']
        prop_d[i['address']].append(i['suburb'])
        prop_d[i['address']].append(i['service'])  # key:value address: services.
    print ('~~~~~~~~',prop_d)

    match=[]#return ["",""]
    for j in prop_d.keys():  # j:each key
        tep = prop_d[j][1].split(",")
        tep.append(prop_d[j][0])  # get suburb
        a_set = set(tep)
        if True==t_set.issubset(a_set):#return address
            match.append(j)

    if len(match)==0:
        return 0
    else:
        print("match is: ",match)
        return match #["add1","add2"]

def pushRecord(test):
    print(test)
    userd.insert_one(test)
# def delete_one(userg,address,c):
#     #userg=username ,address=house address
#     #from database,only delete from user database ,likes
#     if c=='ulike':
#         return 0
#
#     #from database,delete from user and property,owner delete their property
#     if c=='uprop':
#         return 0
#     #from database,only delete from user database ,history
#     if c=='uhis':
#         return 0

def trans_services(l):
    print(l)
    s=l.split(',')
    if 'Check_Indate' in s:
        s.remove('Check_Indate')
    if 'Check_Outdate' in s:
        s.remove('Check_Outdate')
    if 'G_Bath' in s:
        s.remove('G_Bath')
    if 'D_Bath' in s:
        s.remove('D_Bath')
        s.append('Bath(Disabled)')
    if 'Air' in s:
        s.remove('Air')
        s.append('Air conditioned')
    if 'Swimming' in s:
        s.remove('Swimming')
        s.append('Swimming Pool ')
    if 'Laundary' in s:
        s.remove('Laundary')
        s.append('Laundary Service')
    if 'Elevator' in s:
        s.remove('Elevator')
        s.append('Barrier-free elevator')
    if 'Dog' in s:
        s.remove('Dog')
        s.append('Guide dog')
    return s


def updateRecordforuserd(record, updates):
    userd.update_one({'_id': record['_id']}, {
        '$set': updates
    }, upsert=False)


def deleteRecord(userg, address, c):
    # userg= ,address=house address
    # from database,only delete from user database ,likes
    if c == 'ulike':
        info = search_one(userg, "username")  # search username
        all_likes = set(info["likes"].split(","))  # list saving each service
        all_likes.remove(address)
        # print("all likes are: ",all_likes)
        # del the choosen likes
        new = ','.join(all_likes)
        updates = {"likes": new}
        updateRecordforuserd(info, updates)


    # from database,delete from user and property,owner delete their property
    if c == 'uprop':
        info = search_one(userg, "username")  # owner delete their property
        all_prop = set(info["properties"].split(","))
        all_prop.remove(address)
        new = ','.join(all_prop)
        updates = {"properties": new}
        updateRecordforuserd(info, updates)

        info_house = search_one(address, "address")  # delete property
        propd.delete_one(info_house)

    # from database,only delete from user database ,history
    if c == 'prop':
        info_house = search_one(address, "address")  # delete property
        propd.delete_one(info_house)

def dic_to_list(d):
    print(d)
    keys = list(d.keys())
    s=[]
    for x in keys:
        if "/*/" in d[x]:
            l=d[x].split("/*/")
            for y in l:
                a=[]
                a.append(x)
                a.append(y)
                s.append(a)
        else:
            a=[]
            a.append(x)
            a.append(d[x])
            s.append(a)
    print(s)
    return s
def search_history(hist):
    a=hist.split(",") #list saving each service
    #print(a)
    all_h=[]
    for i in a:
        each_h=i.split("(")
        one_p=search_one(each_h[0],"address")#get suburb
        #print(one_p["suburb"])
        if one_p is not None:
            each_h.append(one_p["suburb"])
            each_h.append(one_p["price"])
            each_h.append(one_p["pictures"].split(" ")[0])
            all_h.append(each_h)
        else:
            print("nonetype address",i)
    return (all_h)

def pushProperty(test):
    userinfo=search_one(test["owner"],"username") #test["owner"]
    #print("userproperties is ,",userinfo["properties"])
    t=userinfo["properties"]
    t+=","
    t+=test["address"]
    print("t is: ",t)
    updates={"properties":t}
    updateRecordforuserd(userinfo, updates)
    propd.insert_one(test)
def updateRecordforpropd(record, updates):
    propd.update_one({'_id': record['_id']},{
                              '$set': updates
                              }, upsert=False)

def add_comment(user,address,msg):
    info=search_one(user,"username")#use name to check history
    name=info["name"]
    #print(info["history"])
    a=info["history"].split(",")
    all_h=[]
    for i in a:
        temp=i.split("(")
        all_h.append(temp[0])
    all_his=set(all_h)
    if address not in all_his: #address not in history
        return 0
    else:
        add_to=search_one(address,"address")
        #print("temp is:",temp)
        ch=add_to["comments"]
        print (ch)
        chg={}
        if name in ch:#already has comments before
            t=ch[name]
            t+='/*/'
            t+=msg
            ch[name]=t
        else:
            ch[name]=msg
        chg["comments"]=ch
        #print("chg now is: ",chg)
        updateRecordforpropd(add_to, chg)
        return 1

def add_like(user, address):
    info=search_one(user,"username")#search this users likes
    t=info["likes"]
    if t!="null":
        a=set(info["likes"].split(","))
        if address not in a: #add into likes
            t+=','
            t+=address
            chg={}
            chg["likes"]=t
            #print("chg now is: ",chg)
            updateRecordforuserd(info, chg)
            return 1
        else: #address already in likes
            return 0
    else:
        chg={}
        chg["likes"]=address
        updateRecordforuserd(info, chg)


def update_checktime(address, checkin, checkout):
    single_property = propd.find_one(address)
    if single_property["checkin"] == "":
        single_property["checkin"] = checkin
        single_property["checkout"] = checkout
        propd.update_one(address, {'$set': single_property})
    else:
        single_property["checkin"] += ", "
        single_property["checkin"] += checkin
        single_property["checkout"] += ", "
        single_property["checkout"] += checkout
        propd.update_one(address, {'$set': single_property})

    return 1

def update_history(username, address, indate, outdate):
    single_user = userd.find_one(username)
    date_string = process_date(indate, outdate)
    final_string = address + '(' + date_string
    if single_user["history"] == "null":
        single_user["history"] = final_string
        userd.update_one(username, {'$set': single_user})
    else:
        single_user["history"] += ","
        single_user["history"] += final_string
        userd.update_one(username, {'$set': single_user})

    return 1

def process_date(indate, outdate):
    a = indate.split('-')
    b = outdate.split('-')
    result = ""
    for i in range(len(a)):
        result += a[i]
    result += '-'
    for j in range(len(b)):
        result += b[j]

    return result
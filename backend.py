from flask import Flask,jsonify, request, render_template, url_for, redirect,make_response
import os
import sys
import json
import pro_data
import copy
import datetime
#project by :
#z5137978 xilan yuan
#z5124388 yujie liu
#z5109206 hang su

app = Flask(__name__)
@app.route('/tripnsw',methods=["POST","GET"])
#http://127.0.0.1:5000/tripnsw
#ok
def search_property_belogin():
    print( '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    b = request.args.get('suburb')
    c = request.args.get('check_indate')
    d = request.args.get('check_outdate')

    a = request.args.get('getdata')
    if a==None:
        print ('first time whayt shows: ',a)
        return render_template('index.html')
    else:
        print ('a is ::::::::::::::::::::::::',a)
        #print('suburb is :: ',b)

        temp=a.split(",") #list saving each service
        temp_set=set(temp)
        temp_set.add(b)
        temp_set.add('check_indate')
        temp_set.add('check_outdate')
        temp_set.remove('') #dictionary to save name been checked
        print ('set is: ',temp_set)

        re=pro_data.search_property(temp_set)
        if re==0:
            return jsonify({"status": "error", "message": "no property has been found"}), 200, {"Content-Type": "application/json"}
            #no found property
        else:
            print ("found the property address is ",re)
            return jsonify({"status": "success", "data": re}), 200, {"Content-Type": "application/json"}


#http://127.0.0.1:5000/tripnsw/login
#completed
@app.route('/tripnsw/login',methods=['GET','POST'])
def log_in():
    print("22222")
    user = request.args.get('email')
    password = request.args.get('password')

    re = pro_data.check_log(user, password)

    if user == None and password == None:
        return render_template('login.html')
    elif re == 0:
         return jsonify({"status": "error", "message": "the username or password you input is incorrect"}), 200, {"Content-Type": "application/json"}
    else:
        return jsonify({"status": "success", "data": re}), 200, {"Content-Type": "application/json"}

@app.route('/tripnsw/register',methods=['GET','POST'])
#http://127.0.0.1:5000/tripnsw/register
#cha photo
def regi():
    print("33333")
    a={}
    f_all_none = 1
    #password identify
    pw=request.form.get('password')
    pw1=request.form.get('r_password')
    if pw1!=pw:
        return jsonify({"status": "error", "message": "the password and repassword should same"}), 200, {
            "Content-Type": "application/json"}
        #return "the password and repassword should same ",200
    b=request.form.get('uname')
    a["username"]=b
    # print(a)
    a["password"] = pw
    # print(a)
    b = request.form.get('name')
    a["name"] = b
    # print(a)
    b = request.form.get('phone')
    a["phone"] = b
    print(a)
    #upload head portraits
    #photo_h=request.files.get('up_head')
    photo_h=request.files.get('up_head')
    print("77777777")
    if photo_h is not None:
        print("888888888")

        phot_name=photo_h.filename
        print(phot_name)
        basedir = os.path.abspath(os.path.dirname(__file__))
        print(basedir)
        file_dir=basedir+"/static/imghead/"+phot_name
        print(file_dir)
        photo_h.save(file_dir)
        a["head"]=phot_name
    for x in a.values():
        if x!=None :
            f_all_none=0
            break
    if f_all_none==1:
        return render_template('register.html')
    else:
        #insert_function from pro_data
        a["history"] = "null"
        a["likes"] = "null"
        a["owner"] = 0
        a["pay_card"] ="null"
        a["properties"]="null"
        a["description"]=""

        # pro_data.pushRecord(a)
        re = pro_data.search_one(a["username"],"username")
        if re==None:
            temp_save=copy.deepcopy(a)
            #add record
            pro_data.pushRecord(a)
            return jsonify({"status": "success", "data": temp_save}), 200, {"Content-Type": "application/json"}
        else:
            return jsonify({"status": "error", "message": "the username(email-address) already exist"}), 200, {"Content-Type": "application/json"}



@app.route('/tripnsw/mainpage',methods=['GET','POST'])
#http://127.0.0.1:5000/tripnsw/mainpage
#ok
def search_propertyafterlog():
    print("mainnnnnnnn!!!")
    user=request.args.get('username')
    b = request.args.get('suburb')
    c = request.args.get('check_indate')
    d = request.args.get('check_outdate')

    a = request.args.get('getdata')

    if a==None:
        return render_template('mainpage.html',userh=user)
    else:
        print(a)
        print(user)
        print(b)
        temp=a.split(",") #list saving each service
        temp_set=set(temp)
        temp_set.add(b)
        temp_set.add('check_indate')
        temp_set.add('check_outdate')
        temp_set.remove('') #dictionary to save name been checked
        re=pro_data.search_property(temp_set)
        print(re)
        if re==0:
            return jsonify({"status": "error", "message": "no property has been found"}), 200, {"Content-Type": "application/json"}
            #no found property
        else:
            return jsonify({"status": "success", "data": re}), 200, {"Content-Type": "application/json"}

@app.route('/tripnsw/profile',methods=['GET','POST'])
#http://127.0.0.1:5000/tripnsw/profile
def pro():
    print("profile page!!!!")
    user = request.args.get('username')
    de_add = request.args.get('adr')
    print(user)
    print("delete address:",de_add)
    re = pro_data.search_one(user)#users information
    del re['_id']
    print(re)
    # print(re['name'])
    if de_add!=None and "/deleteprop" in de_add:
        print("delete property")
        de_add = de_add.split('/')[0]
        pro_data.deleteRecord(user, de_add, 'uprop')  # from database,only delete from user
        # delete(user,de_add,'uprop') from database, delete from user and property
        return jsonify({"status": "success", "data": 0}), 200, {"Content-Type": "application/json"}

    have_house=re['properties']
    have_history=re['history']
    print("have history:",have_history)
    num_history=1
    num_house=1
    if have_house=='null':
        num_house=0
        hv_housel='null'
    else:
        hv_housel=pro_data.search_likes(have_house)
        print("hv_housel::::::",hv_housel)
        for i in hv_housel:
            i[7]=i[7].split(" ")
        print("nowwwwww::::::",hv_housel)

    if have_history=='null':
        print("11111111")
        num_history=0
        hv_hisl='null'
    else:
        print("2222222222")
        hv_hisl=pro_data.search_history(have_history)
        # hv_hisl["history"]
        #print("hv_hisl:",hv_hisl)
    return render_template('profile.html',nameh=re['name'],telh=re['phone'],mailh=re['username'],hello=re['name'],likeh=hv_housel,num_househ=num_house,num_hish=num_history,
                           hv_hish=hv_hisl,photoh=re['head'])

@app.route('/tripnsw/modify',methods=['GET','POST'])
#http://127.0.0.1:5000/tripnsw/modify
#completed
def modify_details():
    print("modify!!!!")
    a={}
    user = request.args.get('username')
    user_info=pro_data.search_one(user.split("&")[0])
    print(user_info)
    print(user)
    if '/check' in user:
        c=user.split('/')
        print(c[0])

        pw = request.args.get('mo_pass')
        pw1 = request.args.get('mo_rpass')
        if pw1!=pw:
            return jsonify({"status": "error", "message": "the password and repassword should same"}), 200, {
            "Content-Type": "application/json"}
        a["name"]=request.args.get('mo_name')
        a["username"]=c[0]
        a["password"]=pw
        a["phone"]=request.args.get('mo_phone')
        a["description"]=request.args.get('mo_message')
        print(a)
        #update
        pro_data.change(a)
        return jsonify({"status": "success", "data": c[0]}), 200, {"Content-Type": "application/json"}
    return render_template('modify.html',nameh=user_info["name"])

@app.route('/tripnsw/postad',methods=['GET','POST'])
#http://127.0.0.1:5000/tripnsw/postad
#cha photo
def upload_ads():
    print("upload!!!!!!")
    a={}
    f_all_none = 1
    print("upload advertisements")
    user = request.args.get('username')
    ow=request.args.get('owner')
    print(user)
    # to check if is owner
    if "/check" in user:
        user = user.split('/')[0]
        n=pro_data.search_one(user,"username")
        print(n)
        if n["owner"]==1:
            return jsonify({"status": "success", "data": "ok"}), 200, {"Content-Type": "application/json"}
            # return render_template('up-ad.html', userh=n["name"])
        else:
            return jsonify({"status": "error","message": "you are not the owner , so you can not subimt your property."}), 200, {
                                                  "Content-Type": "application/json"}
    #the user is owner
    if ow=='1':
        user = user.split('/')[0]
        nn = pro_data.search_one(user, "username")["name"]
        return render_template('up-ad.html', userh=nn)
    if ow=='0':
        user = user.split('/')[0]
        title = request.form.get('property_title')
        capacity = request.form.get('property_capacity')
        price = request.form.get('property_price')
        address = request.form.get('property_address')
        surburb = request.form.get('property_surburb')
        postcode = request.form.get('property_postcode')
        describe = request.form.get('form_comment')
        service = request.form.get('getdata')
        j_photo = request.files.getlist('picture')
        print("77777777")
        basedir = os.path.abspath(os.path.dirname(__file__))
        print(basedir)
        if j_photo is not None:
            print("88888888")
            s=""
            for x in j_photo:
                file_dir = basedir + "/static/imghouse/" + x.filename
                x.save(file_dir)
                #print(x.filename)
                s+=x.filename;
                s+=' '

            #print("s is: ",s)
        a["title"] = title
        a["address"] = address
        a["suburb"] = surburb
        a["postcode"] = postcode
        a["capacity"] = capacity
        a["price"] = price
        a["describe"] = describe
        a['service'] = service
        a["pictures"]=s
        if a['service'] != None and len(a['service']) != 0:
            a['service'] = a['service'][:-2]
        print(a)

        a["owner"] = user
        a["longitude"] = "null"
        a["latitude"] = "null"
        a["size"] = "null"
        re = pro_data.search_one(a["address"], "address")
        if re==None:
            print(a)
            temp_save=copy.deepcopy(a)
            pro_data.pushProperty(a)
            return jsonify({"status": "success", "data": temp_save}), 200, {"Content-Type": "application/json"}
        else:
            pro_data.deleteRecord(user, a["address"], "prop")
            pro_data.pushProperty(a)

            return jsonify({"status": "error", "message": "This existing property has been updated."}), 200, {"Content-Type": "application/json"}


@app.route('/tripnsw/likes',methods=['GET','POST'])
#http://127.0.0.1:5000/tripnsw/likes
#ok
def favorite_list():
    print("favorites list")
    user = request.args.get('username')
    de_add=request.args.get('adr')
    print(user)
    print("delete add:",de_add)

    if  de_add!=None and '/deletelike' in de_add:
        print("delete item")
        de_add=de_add.split('/')[0]
        pro_data.deleteRecord(user,de_add,'ulike') #from database,only delete from user
        #delete(user,de_add,'uprop') from database, delete from user and property
        return  jsonify({"status": "success", "data": 0}), 200, {"Content-Type": "application/json"}

    re = pro_data.search_one(user)
    adressl=re["likes"]
    print(adressl)
    hv_like=1
    if adressl!='null':
        re_data=pro_data.search_likes(adressl)
        print(re_data)

        #house_pic=[]
        for i in re_data:
            t = i[7].split(" ")
            i[7]=t
        print(re_data)
    else:
        hv_like=0
        re_data=[]
        print("hv_lik:",hv_like)
    
    #print(house_pic)
    #house_pic = re_data[7].split(" ")

    return render_template('favorites.html',nameh=user,housesh=re_data,hv_likeh=hv_like)

@app.route('/tripnsw/edetail',methods=['GET','POST'])
#http://127.0.0.1:5000/tripnsw/edetail
#ok
def each_details():
    print("each details!!!!!")
    user = request.args.get('username')
    address=request.args.get('adr')
    print(user)
    print(address)
    if address!=None:
        if '/comment' in address:
            print("submit~~~~~~~~~~~~~~")
            address=address.split('/')[0]
            msg=request.args.get("message")
            print(msg)
            #get name ,check history,add comments to database,return 0(not in history ,can not add commets),return 1(add successfully)
            a=pro_data.add_comment(user,address,msg)
            print(a)
            if a==0:
                print("cannor submit")
                return jsonify({"status": "error", "data": "you have not lived in the accommodation ,can not add new comment"}), 200, {
                "Content-Type": "application/json"}
            else:
                print("submit success")
                return jsonify({"status": "success", "data": "add comment successfully!"}), 200, {"Content-Type": "application/json"}
        if '/addlike' in address:
            print("addlike~~~~~")
            address = address.split('/')[0]
            a=pro_data.add_like(user,address)
            #add address into user-likes,return =0(address has existed),return 1(adress has added into user-likes)
            if a==0:
                return jsonify({"status": "error", "data": "you have added the house into favorite list before,please check in favorites"}), 200, {
                "Content-Type": "application/json"}
            else:
                return jsonify({"status": "success", "data": "add the house into favorites list successfully!"}), 200, {"Content-Type": "application/json"}
        print("!!!!!!!!!")
        address=address.title()
        print(address)
        house_info=pro_data.search_one(address,"address")
        print(house_info)
        owner=house_info["owner"]
        print(owner)
        owner_info=pro_data.search_one(owner,"username")
        print(owner_info)
        sell=house_info["service"].title()
        servicel=pro_data.trans_services(sell)
        commentl=pro_data.dic_to_list(house_info["comments"])
        if user=='0':
            namel="user"
            nolog=0
        else:
            user_info=pro_data.search_one(user,"username")
            namel=user_info["name"]
            nolog=1
        house_pic=house_info["pictures"].split(" ")

        print(servicel)
        print(house_pic)
        return render_template('details.html',h_title=house_info["title"],h_addr=house_info["address"],h_price=house_info["price"]
                               ,h_long=house_info["longitude"],h_lat=house_info["latitude"],h_size=house_info["size"],
                               h_cap=house_info["capacity"],serviceh=servicel,nameh=namel,desh=house_info["dscribe"],h_surburb=house_info["suburb"],
                               ownerh=owner_info["name"],emailh=owner_info["username"],desuh=owner_info["description"],commenth=commentl,nologh=nolog,pich=house_pic,
                               photoh=owner_info["head"])

@app.route('/tripnsw/searchresult',methods=['GET','POST'])
#http://127.0.0.1:5000/tripnsw/searchresult
#ok
def for_searchresult():
    re_data=[]
    #print("~~~~~~~~~~~~~~~~~~~~~~~~searchresult page!!!!!!!!!!!!!!!")
    add1 = request.args.get('addr') #get the string, then split by,
    user=request.args.get('username')
    print("user isisisisisis ",user)
    if user=="0":
        userl='user'
    else:
        userl=pro_data.search_one(user,"username")["name"]
    addr=add1.split(",")
    for i in addr:
        print("iiiii is:",i)
        temp=[]
        p_info=pro_data.search_one(i,"address")
        print("p_info is:::::::::::: ",p_info)
        newt=p_info["address"]
        siz=p_info["size"]
        bed=p_info["capacity"]
        servs=set(p_info["service"].split(',',))
        house_pic=p_info["pictures"].split(" ")[0]

        baths=0
        if "g_bath" in servs:
            baths=1
            if "d_bath" in servs:
                baths+=1
        if "parking" in servs:
            park=1
        else:
            park=0
        price=p_info["price"]
        temp.append(newt)
        temp.append(siz)
        temp.append(bed)
        temp.append(baths)
        temp.append(park)
        temp.append(price)  #temp should be write into for loop
        temp.append(house_pic)
        re_data.append(temp)
    #re_data=[[],[]]
    print(re_data)
    print("re_data is: ",re_data)
    #return render_template('searchresult.html',ntitle=newt,sizef=siz,nbed=bed,nbath=baths,ngar=park,pr=price,resulth=re_data)
    return render_template('searchresult.html',resulth=re_data,userh=userl)

@app.route('/tripnsw/pay',methods=['GET','POST'])
#http://127.0.0.1:5000/tripnsw/pay
def payment_details():
    print("each pay!!!!!")
    a = {}
    f_all_none = 1
    has_empty_value = 0
    user = request.args.get('username')
    addr = request.args.get('adr')
    address=addr.title()
    # print(address)
    n = pro_data.search_one(address, "address")
    print(user)
    print(address)
    print("database: ", n)
    p_capacity = int(n["capacity"])
    h_checkin = n["checkin"]
    h_checkout = n["checkout"]
    h_price = n["price"]
    wel_name = user.split("@")[0]
    date_in = request.args.get("pay_checkin")
    date_out = request.args.get("pay_checkout")
    customer_number = request.args.get('pay_people')
    pay_card = request.args.get('pc_number')
    card_date = request.args.get('pc_date')
    card_code = request.args.get('pc_code')
    customer_name = request.args.get('p_name')
    customer_username = request.args.get('p_mail')
    customer_phone = request.args.get('p_phone')
    a["pay_card"] = pay_card
    a["card_date"] = card_date
    a["card_code"] = card_code
    a["customer_name"] = customer_name
    a["customer_username"] = customer_username
    a["customer_phone"] = customer_phone
    a["pay_checkin"] = date_in
    a["pay_checkout"] = date_out
    a["pay_people"] = customer_number
    print("data get: ", a)
    for x in a.values():
        if x != None:
            f_all_none = 0
            break
    for y in a.values():
        if y == "":
            has_empty_value = 1
            break
    if f_all_none == 1:
        return render_template('payment.html', userh=wel_name, h_title=n["title"],h_addr=n["address"],h_price=n["price"], h_cap=n["capacity"])
    elif has_empty_value == 1:
        return jsonify({"status": "error",
                        "message": "Please fill all the information in the form."}), 200, {
                   "Content-Type": "application/json"}
    else:
        if customer_number.isdigit() == False:
            return jsonify({"status": "error",
                            "message": "Number of people should be integer."}), 200, {
                    "Content-Type": "application/json"}
        else:
            if p_capacity < int(customer_number):
                return jsonify({"status": "error", "message": "The number of people is greater than the the houses capacity, please choose another house"}), 200, {"Content-Type": "application/json"}
        person_in_year, person_in_month, person_in_day = get_ymd(date_in)
        person_out_year, person_out_month, person_out_day = get_ymd(date_out)
        if compare(person_in_year, person_in_month, person_in_day, person_out_year, person_out_month, person_out_day) == "second":
            return jsonify({"status": "error",
                            "message": "Checkout date should be later than Checkin date, please choose the correct check date"}), 200, {
                    "Content-Type": "application/json"}
        day_in = datetime.datetime(person_in_year, person_in_month, person_in_day)
        day_out = datetime.datetime(person_out_year, person_out_month, person_out_day)
        interval = (day_out - day_in).days
        cost = str(int(h_price) * int(interval)) + "$"
        reminder = "Payment successfully!The total cost is " + cost
        if h_checkin == "":
            temp_save = copy.deepcopy(a)
            # print(temp_save)
            pro_data.update_history({"username": user}, address, date_in, date_out)
            pro_data.update_checktime({"address": address}, date_in, date_out)
            return jsonify({"status": "success", "data": temp_save,"message": reminder}), 200, {"Content-Type": "application/json"}
        elif "," not in h_checkin:
            if judge(h_checkin, h_checkout, date_in, date_out) == True:
                temp_save = copy.deepcopy(a)
                pro_data.update_history({"username": user}, address, date_in, date_out)
                pro_data.update_checktime({"address": address}, date_in, date_out)
                return jsonify({"status": "success", "data": temp_save,"message": reminder}), 200, {"Content-Type": "application/json"}
            else:
                return jsonify({"status": "error",
                                "message": "The house cannot be rented during the time period you selected, please select another time slot."}), 200, {
                        "Content-Type": "application/json"}                
        else:
            old_in_list = h_checkin.split(", ")
            old_out_list = h_checkout.split(", ")
            length = len(old_in_list)
            can_be_rent = 1
            for i in range(length):
                if judge(old_in_list[i], old_out_list[i], date_in, date_out) == False:
                    can_be_rent = 0
                    break
                else:
                    continue
            if can_be_rent == 0:
                return jsonify({"status": "error",
                                "message": "The house cannot be rented during the time period you selected, please select another time slot."}), 200, {
                        "Content-Type": "application/json"}
            else:
                temp_save = copy.deepcopy(a)
                pro_data.update_history({"username": user}, address, date_in, date_out)
                pro_data.update_checktime({"address": address}, date_in, date_out)
                return jsonify({"status": "success", "data": temp_save,"message": reminder}), 200, {"Content-Type": "application/json"}   


def get_ymd(date_string):
    date_list = date_string.split("-")
    year = int(date_list[0])
    month = int(date_list[1])
    day = int(date_list[2])
    return year, month, day


def compare(year_a, month_a, day_a, year_b, month_b, day_b):
    if year_a > year_b:
        return "second"
    elif year_a < year_b:
        return "first"
    else:
        if month_a > month_b:
            return "second"
        elif month_a < month_b:
            return "first"
        else:
            if day_a > day_b:
                return "second"
            elif day_a < day_b:
                return "first"
            else:
                return "same"

def judge(old_in, old_out, new_in, new_out):
    old_in_year, old_in_month, old_in_day = get_ymd(old_in)
    old_out_year, old_out_month, old_out_day = get_ymd(old_out)
    new_in_year, new_in_month, new_in_day = get_ymd(new_in)
    new_out_year, new_out_month, new_out_day = get_ymd(new_out)
    if compare(new_out_year, new_out_month, new_out_day, old_in_year, old_in_month, old_in_day) != "second":
        return True
    elif compare(old_out_year, old_out_month, old_out_day, new_in_year, new_in_month, new_in_day) != "second":
        return True
    else:
        return False




if __name__ == '__main__':
    app.run(debug=True)

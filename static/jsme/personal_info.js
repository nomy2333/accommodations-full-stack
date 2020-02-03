function check_info(){

    var url = window.location.href;
    var new_url=window.location.search;
    var user=new_url.split('&')[0];
    var uv=user.split('=')[1];

//    alert(new_url)
//    alert(user)
//    alert(uv)
    if (uv=='0'){
        location.href="/tripnsw";
    }
    else{
//        alert("/tripnsw/profile"+new_url)
        location.href="/tripnsw/profile"+user;
    }


//    new_url=url.replace("#login","/check")
//    $.ajax({
//        url: new_url,
//        type:'GET',
//        crossDomain: true,
//        success:function(data){
//            if(data.status === 'success') {
//                //document.location.pathname = '/tripnsw/mainpage'
//                //location.href="${pageContext.request.contextPath }/classify/queryClassify?c="+sStr;
//                //location.href="/tripnsw/mainpage?username="+name
//                //alert(typeof(data.dat.name))
//                s=data.dat.name+','+data.dat.password+','+data.dat.username+','+data.dat.phone+','+data.dat.pay_card+','+data.dat.history+','+data.dat.likes+','+data.dat.owner
//                //alert(s)
//                location.href="/tripnsw/profile?userinfo="+s
//
//                //document.location.pathname = "/tripnsw/mainpage?username="+name
//            } else {
//                alert("fail")
//            }
//        }
//    });


}
function tomain(){
//    alert("!!!!!!")
    var url = window.location.href;//获取url中"?"符后的字串
    var new_url=window.location.search;
//    alert(new_url)
    l=new_url.split('&')[0]
    l1=l.split('=')[1]
//    alert(l1)
    if (l1==0){
    location.href="/tripnsw"
    }
    else{
    location.href="/tripnsw/mainpage"+l;
    }

}
function modi_detail(){
    var url = window.location.href;
    var new_url=window.location.search;
    l=new_url.split('&')[0]
    //alert(new_url)
    location.href="/tripnsw/modify"+l;

}
//function up_ads(){
//    var url = window.location.href;
//    var new_url=window.location.search.split("&")[0];
//    alert(new_url)
//    location.href="/tripnsw/postad"+new_url;
//}
function favo_check(){
    var url = window.location.href;
    var new_url=window.location.search;
    l=new_url.split('&')[0]
//    alert("favo_check")
//    alert(new_url)
//    alert("/tripnsw/likes"+new_url)
    location.href="/tripnsw/likes"+l;

}

function sub_modi(){
//    alert("1111111")
    var urlp = window.location.href;
    var new_url=window.location.search.split('&')[0];
    var urla='/tripnsw/modify'+new_url+'/check';
//    alert(urla)
    var j_name=document.getElementById('mo_name').value;
    var j_phone=document.getElementById('mo_phone').value;
    var j_pass=document.getElementById('mo_pass').value;
    var rj_pass=document.getElementById('mo_rpass').value;
    var j_mess=document.getElementById('mo_message').value;
    $.ajax({
        url: urla,
        type:'GET',
        data:{mo_name: j_name, mo_phone:j_phone, mo_pass:j_pass, mo_rpass: rj_pass, mo_message:j_mess},
        crossDomain: true,
        success:function(data){
            if(data.status === 'success') {
                alert("successful modification")
                location.href="/tripnsw/profile?username="+data.data
            } else {
                alert(data.message)
            }
        }
    });
}
function check_detail(){
    var h_address=document.getElementById('house_id');
    var urlp = window.location.href;
    var new_urlp=window.location.search.split("&")[0];
//    alert(new_urlp);
//    alert (h_address.innerText);
    url="/tripnsw/edetail"+new_urlp+"&adr="+h_address.innerText;
//    alert(url)
    location.href=url
}
function delete_house(x){
//    alert("delete 11111111")
//    alert(x)
    var urlp = window.location.href;
//    alert(urlp)
    var new_urlp=window.location.search.split("&")[0];//argu after ? includes ?
//    alert(new_urlp)
    var urla=window.location.href;//all url
//    alert(urla)
    if(urla.indexOf("?") != -1){
        url1 = urla.split("?")[0];//all before ?
//        alert(url1)
    }
   url=url1+new_urlp+"&adr="+x+'/deletelike';
//    alert(url)
    $.ajax({
        url: url,
        type:'GET',
        data:{},
        crossDomain: true,
        success:function(data){
            if(data.status === 'success') {
                alert("successful modification")
                location.href=urlp
            } else {
                alert(data.message)
            }
        }
    });

}
function jump_ad(){
//    alert("jump_ad")
//    var url = window.location.href;//获取url中"?"符后的字串
    var n=window.location.search;
    var nn=n.split("&")
//    a=nn[1].split

    if (nn[1] == null ){
        var url="/tripnsw/postad"+nn[0]+"/check";
//        alert(url)
        $.ajax({
            url: url,
            type:'GET',
            data:{},
            crossDomain: true,
            success:function(data){
                if(data.status === 'success') {
    //                alert("successful modification")
                    location.href="/tripnsw/postad"+nn[0]+"&owner=1";
                } else {
                    alert(data.message)
                }
            }
        });

    }
    else{
//        alert(nn[1])
        a=nn[1].split("=")[0]
        if (a=="owner"){
            location.href="/tripnsw/postad"+nn[0]+"&owner=1";
        }
        else{
            var url="/tripnsw/postad"+nn[0]+"/check";
//        alert(url)
            $.ajax({
                url: url,
                type:'GET',
                data:{},
                crossDomain: true,
                success:function(data){
                    if(data.status === 'success') {
        //                alert("successful modification")
                        location.href="/tripnsw/postad"+nn[0]+"&owner=1";
                    } else {
                        alert(data.message)
                    }
                }
            });

        }

    }
}


function upnew_ads(){
//    alert("111111111111111111111")
    var url = window.location.href;
    var new_url=window.location.search;
    var user=new_url.split("&")[0];
    var nn="/tripnsw/postad"+user+"&owner=0";

//    alert(nn)
    var ad_title=document.getElementById('property_title').value;
    var ad_capacity=document.getElementById('property_capacity').value;
    var ad_price=document.getElementById('property_price').value;
    var ad_address=document.getElementById('property_address').value;
    var ad_surburb=document.getElementById('property_surburb').value;
    var ad_postcode=document.getElementById('property_postcode').value;
    var ad_describe=document.getElementById("form_comment").value;

    var str=$("input[type='checkbox']:checked");
    var objarray=str.length;
    var chestr="";

    for (i=0;i<objarray;i++) {
        if(str[i].checked == true) {
            chestr+=str[i].value+", ";
        }
    }
//    alert(chestr)
    //var j_photo=document.getElementById('galleryp')[0].files;
    var fd=new FormData();
    var files= $("#gallery")[0].files;
    /**这里多次append file到同一个key里面*/
    for(var i=0;i<files.length;i++){
//        alert(i);
        fd.append("picture", files[i]);
    }
    fd.append('property_title',ad_title);
    fd.append('property_capacity',ad_capacity);
    fd.append('property_price',ad_price);
    fd.append('property_address',ad_address);
    fd.append('property_surburb',ad_surburb);
    fd.append('property_postcode',ad_postcode);
    fd.append('getdata',chestr);
    fd.append('form_comment',ad_describe);

    $.ajax({
        url: nn,
        type:'GET',
//        data:{
//        property_title: ad_title,
//        property_capacity: ad_capacity,
//        property_price: ad_price,
//        property_address: ad_address,
//        property_surburb: ad_surburb,
//        property_postcode: ad_postcode,
//        getdata: chestr,
//        form_comment: ad_describe
//        },
        data:fd,
        contentType:false,
        processData:false,
        type:'POST',
        success:function(data){
            if(data.status === 'success') {
                alert("Successfully posted!")
                location.href="/tripnsw/profile" + new_url
            } else {
                alert(data.message)
                location.href="/tripnsw/profile" + new_url
            }
        }
    });
}
function sub_comment(){
//    alert("submit comment!")
    var comment=document.getElementById('message').value;
    var argument_s=window.location.search;
//    alert(argument_s)
//    alert(comment)
    add_argu=argument_s+"/comment";
//    alert(add_argu)
//    alert("/tripnsw/edetail"+add_argu)

    $.ajax({
        url:"/tripnsw/edetail"+add_argu,
        type:'GET',
        data:{message:comment},
        crossDomain: true,
        success:function(data){
            if(data.status === 'success') {
                alert(data.data)
//                alert("11111111")
                location.href="/tripnsw/edetail" + argument_s;
            } else {
                alert(data.data)
//                alert("/tripnsw/edetail" + argument_s);
//                alert("22222222")
//
//                location.href="/tripnsw/edetail" + argument_s;

            }
        }

    });

}
function history_todetail(x){
//    alert("delete 11111111")
//    alert(x)
    var user = window.location.search.split('&')[0];
//    alert(user)
    var new_url="/tripnsw/edetail"+user+"&adr="+x;
//    alert(new_url);
    location.href=new_url;


}
function topay(){
    var user = window.location.search;
    var new_url="/tripnsw/pay"+user;
    location.href=new_url;
}
function add_like(){
//    alert("like~~~~~")
    var url=window.location.href;
    var ar=window.location.search.split('&')[0];
//    alert(url)

    url=url+"/addlike";
//    alert(url)
//    location.href=url;
//    var a=window.location.search.split('&');
    $.ajax({
        url:url,
        type:'GET',
        crossDomain: true,
        success:function(data){
            if(data.status === 'success') {
                alert(data.data)
//                aler("11111111")
//                location.href="/tripnsw/likes" + ar;
            } else {
                alert(data.data)
//                alert("22222222")
//                location.href="/tripnsw/likes" + ar;
//                alert("/tripnsw/edetail" + argument_s);
//                alert("22222222")
//
//                location.href="/tripnsw/edetail" + argument_s;

            }
        }

    });


}

function submit_pay(){
    //alert("111111111111111111111")
    var indate = document.getElementById('pay_checkin').value;
    var outdate = document.getElementById('pay_checkout').value;
    var customer_number = document.getElementById('pay_people').value;
    var pay_card = document.getElementById('pc_number').value;
    var card_date = document.getElementById('pc_date').value;
    var card_code = document.getElementById('pc_code').value;
    var buyer_name = document.getElementById('p_name').value;
    var buyer_mail = document.getElementById("p_mail").value;
    var buyer_phone = document.getElementById("p_phone").value;
    var url = window.location.href;
    var new_url=window.location.search;
//    var nurl=new_url.split('&')[0]
    var nn='/tripnsw/pay'+ new_url
    $.ajax({
        url: nn,
        type:'GET',
        data:{
        pay_checkin: indate,
        pay_checkout: outdate,
        pay_people: customer_number,
        pc_number: pay_card,
        pc_date: card_date,
        pc_code: card_code,
        p_name: buyer_name,
        p_mail: buyer_mail,
        p_phone: buyer_phone
        },
        crossDomain: true,
        success:function(data){
            if(data.status === 'success') {
                alert(data.message)
                location.href="/tripnsw/profile" + new_url
//                if (confirm(data.message)) {
//                    alert("Payment Successful")
//                    location.href="/tripnsw/profile" + new_url
//                } else {
//                    alert("Payment failed, please try it again.")
//                }
            } else {
                alert(data.message)
            }
        }
    });
}
function del_property(x){
    //    alert("delete 11111111")
//    alert(x)
    var urlp = window.location.href;
//    alert(urlp)
    var new_urlp=window.location.search;//argu after ? includes ?
//    alert(new_urlp)
    var urla=window.location.href;//all url
//    alert(urla)
    if(urla.indexOf("?") != -1){
        url1 = urla.split("?")[0];//all before ?
//        alert(url1)
    }
   url=url1+new_urlp+"&adr="+x+'/deleteprop';
//   alert(url)
    $.ajax({
        url: url,
        type:'GET',
        data:{},
        crossDomain: true,
        success:function(data){
            if(data.status === 'success') {
                alert("successful delete your property!")
//                alert(urlp)
                location.href=urlp
            } else {
                alert(data.message)
            }
        }
    });
}




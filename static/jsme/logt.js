function sess(){
    var name=document.getElementById('username').value;
    var password=document.getElementById('password').value;
    $.ajax({
        url: '/tripnsw/login',
        type:'GET',
        data:{email: name, password: password},
        crossDomain: true,
        success:function(data){
            if(data.status === 'success') {
                //document.location.pathname = '/tripnsw/mainpage'
                //location.href="${pageContext.request.contextPath }/classify/queryClassify?c="+sStr;
                location.href="/tripnsw/mainpage?username="+name

                //document.location.pathname = "/tripnsw/mainpage?username="+name
            } else {
                alert(data.message)
            }
        }
    });
}
function for_register(){
    var u_name=document.getElementById('uname').value;
    var j_name=document.getElementById('name').value;
    var j_pass=document.getElementById('password').value;
    var rj_password=document.getElementById('r_password').value;
    var j_phone=document.getElementById('phone').value;
    //var j_payment=document.getElementById('payment').value;
    var j_photo=document.getElementById('up_head').files[0];
    //var j_photo=$('#')
//    console.log(j_photo.files[0].size);
//    alert("herererere");
//    alert(j_photo.name);
    //alert(j_photo.files[0].size);
    var fd=new FormData();
    fd.append('uname',u_name);
    fd.append('name',j_name);
    fd.append('password',j_pass);
    fd.append('r_password',rj_password);
    fd.append('phone',j_phone);
    fd.append('up_head',j_photo);


    $.ajax({
        url: '/tripnsw/register',
        type:'GET',
        data:fd,
//        data:{uname: u_name, name:j_name, password:j_pass, r_password: rj_password, phone:j_phone,up_head:j_photo},
        contentType:false,
        processData:false,
        type:'POST',
        success:function(data){
            if(data.status === 'success') {
                location.href="/tripnsw/mainpage?username="+u_name
            } else {
                alert(data.message)
            }
        }
    });
}
function choose() {
        var check_1=document.getElementById('check_indate').value;
        var check_2=document.getElementById('check_outdate').value;
        var check_3=document.getElementById('suburb').value;
        //alert(check_3); //ok

        var str=$("input[type='checkbox']:checked");
        var objarray=str.length;
        var chestr="";  // save id/name
        //var nextStr = "";
        for (i=0;i<objarray;i++)
        {
        if(str[i].checked == true)
        {
            chestr+=str[i].value+",";
            //nextStr+=str[i].nextSibling.nodeValue; //  "Guide dog"
        }
        }
        //alert(chestr+"---"+nextStr);
        //alert(chestr); //ok

        $.ajax({
            url: '/tripnsw',
            type:'GET',
            data:{
                check_indate: check_1,
                check_outdate: check_2,
                suburb: check_3,
                getdata:chestr
            },
            crossDomain: true,
            success:function(data){
                if(data.status === 'success') {
                    adds=data.data; //get re(address) from .py
                    //alert(adds)
                    location.href="/tripnsw/searchresult?username=0&addr="+adds
                } else {
                    alert(data.message)
                }
            }
        });
}
function choose_afterlog() {
    var user=window.location.search;
//    alert(user)
    var check_1=document.getElementById('check_indate').value;
    var check_2=document.getElementById('check_outdate').value;
    var check_3=document.getElementById('suburb').value;
    //alert(check_3); //ok

    var str=$("input[type='checkbox']:checked");
    var objarray=str.length;
    var chestr="";  // save id/name
    //var nextStr = "";
    for (i=0;i<objarray;i++)
    {
    if(str[i].checked == true)
    {
        chestr+=str[i].value+",";
        //nextStr+=str[i].nextSibling.nodeValue; //  "Guide dog"
    }
    }
    //alert(chestr+"---"+nextStr);
    //alert(chestr); //ok

    $.ajax({
        url: '/tripnsw/mainpage'+user,
        type:'GET',
        data:{
            check_indate: check_1,
            check_outdate: check_2,
            suburb: check_3,
            getdata:chestr
        },
        crossDomain: true,
        success:function(data){
            if(data.status === 'success') {
                adds=data.data; //get re(address) from .py
                //alert(adds)
                location.href="/tripnsw/searchresult"+user+"&addr="+adds;
            } else {
                alert(data.message)
            }
        }
    });
}

function search_arealog(a) { //search pictue after login
    var check_1=document.getElementById('check_indate').value;
    var check_2=document.getElementById('check_outdate').value;
    var user=window.location.search;
//    var user=new_url.split('&')[0];

    //alert("!!!!!"+user);
    //document.getElementById('suburb')
    //alert(check_3); //ok

    var str=$("input[type='checkbox']:checked");
    var objarray=str.length;
    var chestr="";  // save id/name
    //var nextStr = "";
    for (i=0;i<objarray;i++)
    {
    if(str[i].checked == true)
    {
        chestr+=str[i].value+",";
        //nextStr+=str[i].nextSibling.nodeValue; //  "Guide dog"
    }
    }

    $.ajax({
        url: '/tripnsw',
        type:'GET',
        data:{
            check_indate: check_1,
            check_outdate: check_2,
            suburb: a,
            getdata:chestr
        },
        crossDomain: true,
        success:function(data){
            if(data.status === 'success') {
                adds=data.data; //get re(address) from .py
                //alert(adds)
                location.href="/tripnsw/searchresult"+user+"&addr="+adds
            } else {
                alert(data.message)
            }
        }
    });
}

function search_byarea(a) {
    var check_1=document.getElementById('check_indate').value;
    var check_2=document.getElementById('check_outdate').value;
    //document.getElementById('suburb')
    //alert(check_3); //ok

    var str=$("input[type='checkbox']:checked");
    var objarray=str.length;
    var chestr="";  // save id/name
    //var nextStr = "";
    for (i=0;i<objarray;i++)
    {
    if(str[i].checked == true)
    {
        chestr+=str[i].value+",";
        //nextStr+=str[i].nextSibling.nodeValue; //  "Guide dog"
    }
    }

    $.ajax({
        url: '/tripnsw',
        type:'GET',
        data:{
            check_indate: check_1,
            check_outdate: check_2,
            suburb: a,
            getdata:chestr
        },
        crossDomain: true,
        success:function(data){
            if(data.status === 'success') {
                adds=data.data; //get re(address) from .py
                //alert(adds)
                location.href="/tripnsw/searchresult?username=0&addr="+adds
            } else {
                alert(data.message)
            }
        }
    });
}
import base64

import demjson
from flask import Flask,jsonify,session,render_template,redirect
from flask.globals import request
from flask.json import jsonify
from dbnew import connection
from connection import conn

import os
from DBConnection import Db
app = Flask(__name__)
app.secret_key="hi"

syspath = r"C:\project\myprivacydecision\mpmd\MPMD\static\\"


# @app.route('/aa')
# def s():
#     return "hai";

@app.route('/',methods=['POST','get'])
def login1():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        db=Db()
        res = db.selectOne("select * from user_login where emailid = '" + username + "' and password = '" + password + "'")
        if res is not None:
            session['lg'] = "lin"
            if res['utype']=='admin':
                 return redirect('/adminhome')
        else:
            return ''' <script> alert("Invalid Username  or Password...!!!!");window.location='/' </script>   '''
    return render_template("login.html")

@app.route('/adminhome')
def adminhome():
    if session['lg'] == "lin":
        return render_template("admin/index.html")
    else:
        return render_template("login.html")




@app.route('/logout')
def logout():
    session['lg']=""
    session.clear()
    return redirect('/')

# ===================================================admin===========================================================

@app.route('/view_users')
def view_users():
    if session['lg'] == "lin":
        db=Db()
        q=db.select("select * from user_reg")
        return render_template("admin/view users.html",d=q)
    else:
        return render_template("login.html")


@app.route('/view_complaint')
def view_complaint():
    if session['lg'] == "lin":
        db = Db()
        res = db.select("select * from complaint,user_reg where complaint.user_id = user_reg.uid ")
        return render_template("admin/view_complaint.html",d=res)
    else:
        return render_template("login.html")


@app.route('/reply_complaint/<c_id>',methods=['get','post'])
def reply_complaint(c_id):
    if session['lg'] == "lin":
        if request.method=="POST":
             reply=request.form['textarea']
             db = Db()
             db.update("update complaint set reply='"+reply+"', reply_date = curdate() where complaint_id = '"+c_id+"'")
             return '''<script>alert("Reply Send Sucessfullly");window.location = "/view_complaint"</script>'''
        return render_template("admin/reply.html")
    else:
        return render_template("login.html")


@app.route('/view_feedback')
def view_feedback():
    if session['lg'] == "lin":
        db=Db()
        q=db.select("SELECT * FROM feedback,user_reg WHERE feedback.user_id=user_reg.uid")
        return render_template("admin/view_feedback.html",d=q)
    else:
        return render_template("login.html")

# =============================================================================================================================================

@app.route('/registration',methods=["POST"])
def registration():
    fname = request.form["fname"];
    gender = request.form["gender"];
    dob = request.form["dob"];
    emailid = request.form["emailid"];
    phone = request.form["ph"];
    photo = request.files["pic"]
    password = request.form["password"];
    # a = base64.b64decode(photo)
    # print(a)
    # path = "/home/god/Desktop/mpmd/MPMD/static/userreg/" + emailid + ".jpg"
    # path = syspath+"userreg/" + emailid + ".jpg"
    # absolute_path = os.path.abspath("../userreg/"+emailid+".jpg");
    # print(absolute_path)
    # fh=open("static/kkk/" +nam+ ".jpg", "wb")
    # fh = open(path, "wb")
    # fh.write(a)
    # fh.close()
    photo.save(r"C:\project\myprivacydecision\mpmd\MPMD\static\userreg\\"+ emailid+ ".jpg")
    abc = "static/userreg/" + emailid+ ".jpg"
    s="select max(uid) from user_reg"
    c=conn()
    id=c.mid(s)
    q=Db().selectOne("SELECT * FROM `user_login` WHERE `emailid`='"+emailid+"'")
    if q is None:
        p=Db().selectOne("SELECT * FROM `user_reg` WHERE `phone`='"+phone+"'")
        if p is None:
            qry1 = "insert into user_reg(fname,gender,dob,emailid,phone,photo)values('"+fname+"','"+gender+"','"+dob+"','"+ emailid+"','"+phone+"','"+ abc+"')"
            qry2 = "insert into user_login(emailid,password,utype)values ('"+emailid+"','"+password+"','user')"
            print(qry2);
            c=conn()
            ss = "insert into tbl_privacy(post,profile,request,userid) values('public','public','public','" + str(id) + "')"
            c.nonreturn(ss)
            c.nonreturn(qry1)
            c.nonreturn(qry2)
            return jsonify(status='ok')
        else:
            return jsonify(status="phn")
    else:
        return jsonify(status='no')

@app.route('/login', methods=['POST'])
def login():
    emailid= request.form["emailid"];
    password = request.form["password"];
    qry = "select * from user_login where emailid='"+emailid+"' and password='"+ password+"'"
    c=conn()
    res=c.selectone(qry)
    if res is not None:
        qry2 = "select uid from user_reg where emailid='"+emailid+"'"
        res = c.selectone(qry2)
        return jsonify(status='ok', id=res[0])
    else:
        return jsonify(status='no')

@app.route('/viewprofile', methods=['POST'])
def profile():
   uid = request.form["uid"];
   qry = "select * from user_reg where uid='"+ uid +"'"
   c=conn()
   res=c.selectone(qry)
   if res is not None:
       return jsonify(status='ok', fname=res[1], gender=res[2], dob=res[3], emailid=res[4], phone=res[5],photo=res[6])
   else:
       return jsonify(status='no')

@app.route('/editprofile', methods=['POST'])
def edit():
    uid = request.form["uid"];
    qry = "select * from user_reg where uid='" + uid + "'"
    c=conn()
    res=c.selectone(qry)
    if res is not None:
        return jsonify(status='ok', fname=res[1], gender=res[2], dob=res[3], emailid=res[4], phone=res[5], photo=res[6])
    else:
        return jsonify(status='no')

@app.route('/updateprofile', methods=['POST'])
def update():
    fname = request.form["fname"];
    emailid = request.form["emailid"];
    gender = request.form["gender"];
    dob = request.form["dob"];
    phone = request.form["ph"];
    # photo = request.form["photo"]
    uid = request.form["uid"];
    qry3 = "update user_reg SET fname='"+fname+"',gender='"+gender+"',dob='"+ dob+"',emailid='"+emailid+"',phone='"+phone+"' where uid='" +uid+"'"
    c=conn()
    c.nonreturn(qry3)
    return jsonify(status='ok')

@app.route('/postprivacy', methods=['POST'])
def pp():
    ispublic=request.form["ispublic"];
    isfriends=request.form["isfriends"];
    isbfriends=request.form["isbfriends"];
    isrelative=request.form["isrelative"];
    isme=request.form["isme"];
    pid=request.form["pid"];
    qry11="insert into tbl_postprivacy(postid,ispublic,isfriends,isbfriends,isrelative,isme)values('"+str(pid)+"','"+ispublic+"','"+isfriends+"','"+isbfriends+"','"+isrelative+"','"+isme+"')"
    c=conn()
    c.nonreturn(qry11)
    return jsonify(status='ok')

@app.route('/privacysettings',methods=['POST'])
def ps():
    category=request.form["category"];
    permit_or_deny=request.form["permit_or_deny"]
    limited_or_unlimited=request.form["limited_or_unlimited"];
    post_month=request.form["post_month"];
    no_of_limit=request.form["no_of_limit"];
    uid=request.form["uid"];
    qry01="insert into tbl_privacy(category,permit_or_deny,limited_or_unlimited,post_month,no_of_limit,uid)values('"+category+"','"+ permit_or_deny+"','"+limited_or_unlimited+"','"+post_month+"','"+no_of_limit+"','"+uid+"')"
    c=conn()
    c.nonreturn(qry01)
    return jsonify(status='ok')


@app.route('/viewfriends',methods=['POST'])
def friends():
    uid=request.form["uid"];
    qqry="select uid,fname,emailid,photo from user_reg where uid in(select frid from tbl_friend where uid='"+uid+"')OR uid in(select uid from tbl_friend where frid='"+uid+"')"
    print(qqry)
    c=conn()
    results=c.jsonsel(qqry)
    return jsonify(status="ok", users=results)

@app.route('/search',methods=['POST'])
def srch():
    uid=request.form["uid"];
    print(uid)
    name=request.form["srch"];
    qy="select uid,fname,emailid,photo from user_reg WHERE fname like '%"+name+"%' and uid!='"+uid+"' and uid not in (SELECT uid FROM tbl_request WHERE fid='"+uid+"') and uid not in (SELECT fid FROM tbl_request WHERE uid='"+uid+"') and uid not in ( SELECT uid FROM tbl_friend WHERE frid='"+uid+"') and uid not in (SELECT frid FROM tbl_friend WHERE uid ='"+uid+"' ) "
    c=conn()
    results=c.jsonsel(qy)
    return jsonify(status="ok", users=results)

@app.route('/changephoto', methods=['POST'])
def chphoto():
    uid = request.form["uid"];
    print(uid)
    photo = request.form["imgdp"];
    a = base64.b64decode(photo)
    path = syspath + "userreg\\" + str(uid) + ".jpg"
    fh = open(path, "wb")
    fh.write(a)
    fh.close()

    abc = "static/userreg/" + str(uid) + ".jpg "
    return jsonify(status="ok")

@app.route('/friendschat',methods=['POST'])
def chatfrnd():
    uid=request.form["uid"];
    qqry="select uid,fname,photo from user_reg where uid in (select frid from tbl_friend where uid='"+uid+"')OR uid in (select uid from tbl_friend where frid='"+uid+"')"
    c=conn()
    results=c.jsonsel(qqry)
    if len(results)>0:
        return jsonify(status="ok", users=results)
    else:
        return jsonify(status="no")

@app.route('/chatsend',methods=['POST'])
def chatsend():
    from_id=request.form["from_id"];
    to_id=request.form["to_id"];
    msg=request.form["msg"];
    qr1="insert into tbl_chat(from_id,to_id,msg,date,time)values ('"+from_id+"','"+to_id+"','"+msg+"',CURDATE(),CURTIME())"
    c=conn()
    c.nonreturn(qr1)
    return jsonify(status='ok')

@app.route('/chat',methods=['POST'])
def chat():
    id = request.form["lastmsgid"];
    from_id = request.form["from_id"];
    to_id = request.form["to_id"];
    qr2="select from_id,msg,date,id from tbl_chat where id>'"+id+"' AND ((to_id='"+to_id+"' and from_id='"+from_id+"') or (to_id='"+from_id+"' and from_id='"+to_id+"')) order by id asc"
    c=conn()
    results=c.jsonsel(qr2)
    if len(results)>0:
        return jsonify(status="ok", users=results)
    else:
        return jsonify(status="no")

@app.route('/and_sndrequest',methods=['POST'])
def sendreq():
    uid=request.form["id"];
    fid=request.form["frndid"];
    q20="insert into tbl_request(uid,fid,reqdate,status)values('"+uid+"','"+fid+"',CURDATE(),'pending')"
    c=conn()
    c.nonreturn(q20)
    return jsonify(status='ok')

@app.route('/and_unfrnd',methods=['post'])
def unfrnd():
    uid=request.form["id"];
    fid=request.form["frndid"];
    qry="delete from tbl_friend where (uid='"+uid+"' and fid='"+fid+"') or (uid='"+fid+"' and fid='"+uid+"')"
    c = conn()
    c.nonreturn(qry)
    return jsonify(status="ok")

@app.route('/viewreq',methods=['POST'])
def viewreq():

    uid=request.form["uid"];
    qreq="select user_reg.uid, user_reg.fname,user_reg.photo,user_reg.emailid,tbl_request.reqdate,tbl_request.reqid from user_reg inner join tbl_request on user_reg.uid = tbl_request.uid where tbl_request.status='pending' AND tbl_request.fid='"+uid+"'"
    c=conn()
    results=c.jsonsel(qreq)
    return jsonify(status="ok", users=results)

@app.route('/reqaccepted',methods=['POST'])
def accepted():
    reqid=request.form["reqid"];

    uid=request.form["uid"];

    frid=request.form["frid"];
    print(frid);
    status=request.form["status"];
    acqry="update tbl_request set status='"+status+"' where reqid='"+reqid+"'"
    c=conn()
    c.nonreturn(acqry)
    if status=="accepted":
        inac="insert into tbl_friend (uid,frid,date,status) values ('"+uid+"','"+frid+"',CURDATE(),'"+status+"')"
        c.nonreturn(inac)

    return jsonify(status='ok')

@app.route('/reqrejected',methods=['POST'])
def rejected():
    reqid = request.form["reqid"];
    reqry="update tbl_request set status='rejected' where reqid='"+reqid+"'"
    c=conn()
    c.nonreturn(reqry)
    return jsonify(status='ok')
@app.route('/postid',methods=['POST'])
def postid():
    postid=request.form["postid"];
    qry="delete from tbl_post where postid='" + postid + "'"
    c=conn()
    c.nonreturn(qry)
    return jsonify(status='ok')

@app.route("/and_profile",methods=['post'])
def and_profile():
    our_id=request.form['uid']
    frndid=request.form['user']
    s = "SELECT * FROM tbl_privacy where userid='" + frndid + "'"
    c = conn()
    res1 = c.selectone(s)
    if res1 is not None :
        if res1[3] =="public" and res1[2]=="public":
            qry="select * from user_reg where uid='"+frndid+"'"
            print(qry)
            c=conn()
            res=c.selectone(qry)
            s="select user_reg.uid,user_reg.fname,user_reg.photo,tbl_post.photopost,tbl_post.description,tbl_postlike.isliked as 'islike' ,CONVERT(tbl_post.date,char(10)) as 'date',tbl_post.postid from user_reg inner join tbl_post on user_reg.uid = tbl_post.uid  left join tbl_postlike on tbl_post.postid=tbl_postlike.postid where user_reg.uid='"+frndid+"' order by tbl_post.postid desc"
            c=conn()
            results = c.jsonsel(s)
            if res is not None:
                qry1 = "select * from tbl_request where (fid='"+frndid+"' and uid='"+our_id+"') or (fid='"+our_id+"' and uid='"+frndid+"')"
                res1 = c.selectone(qry1)
                print(res1)
                if res1 is not None:
                    stat=res1[3]
                    return jsonify(status="ok",mail=res[1],name=res[2],gender=res[3],image=res[4],stat=stat,users=results)
                else:
                    return jsonify(status="ok", mail=res[1], name=res[2], gender=res[3], image=res[4], stat="no",users=results)
            else:
                return jsonify(status="no")

        elif res1[3] == "fof" and res1[2] == "fof" :
            ss="select * from tbl_friend where (uid in (select uid from tbl_friend where frid='"+our_id+"') or (select frid from tbl_friend where uid='"+our_id+"') and (frid='"+frndid+"')) or(((frid in (select uid from tbl_friend where frid='"+our_id+"') or (select frid from tbl_friend where uid='"+our_id+"'))) and (uid='"+frndid+"'))"
            res2=c.selectall(ss)
            if res2 is not None:
                ry = "select * from user_reg where uid='" + frndid + "'"
                print(ry)
                c = conn()
                res = c.selectone(ry)
                s = "select user_reg.uid,user_reg.fname,user_reg.photo,tbl_post.photopost,tbl_post.description,tbl_postlike.isliked as 'islike' ,CONVERT(tbl_post.date,char(10)) as 'date',tbl_post.postid from user_reg inner join tbl_post on user_reg.uid = tbl_post.uid  left join tbl_postlike on tbl_post.postid=tbl_postlike.postid where user_reg.uid='" + frndid + "' order by tbl_post.postid desc"
                c = conn()
                results = c.jsonsel(s)
                if res is not None:
                    qry1 = "select * from tbl_request where (fid='" + frndid + "' and uid='" + our_id + "') or (fid='" + our_id + "' and uid='" + frndid + "')"
                    res1 = c.selectone(qry1)
                    print(res1)
                    if res1 is not None:
                        stat = res1[3]
                        return jsonify(status="ok", mail=res[1], name=res[2], gender=res[3], image=res[4], stat=stat,
                                       users=results)
                    else:
                        return jsonify(status="ok", mail=res[1], name=res[2], gender=res[3], image=res[4], stat="no",
                                       users=results)
                else:
                    return jsonify(status="no")

        elif res1[3] =="public" and res1[2]=="fof":
            ry = "select * from user_reg where uid='" + frndid + "'"
            print(ry)
            c = conn()
            res = c.selectone(ry)
            if res is not None:
                ss = "select * from tbl_friend where (uid in (select uid from tbl_friend where frid='" + our_id + "') or (select frid from tbl_friend where uid='" + our_id + "') and (frid='" + frndid + "')) or(((frid in (select uid from tbl_friend where frid='" + our_id + "') or (select frid from tbl_friend where uid='" + our_id + "'))) and (uid='" + frndid + "'))"
                results = c.jsonsel(ss)
                if len(results)>0:
                    qry1 = "select * from tbl_request where (fid='" + frndid + "' and uid='" + our_id + "') or (fid='" + our_id + "' and uid='" + frndid + "')"
                    res1 = c.selectone(qry1)
                    print(res1)
                    if res1 is not None:
                        stat = res1[3]
                        return jsonify(status="ok", mail=res[1], name=res[2], gender=res[3], image=res[4], stat=stat,
                                       users=results)
                    else:
                        return jsonify(status="ok", mail=res[1], name=res[2], gender=res[3], image=res[4], stat="no",
                                       users=results)
                else:
                    return jsonify(status="ok", mail=res[1], name=res[2], gender=res[3], image=res[4], stat="no",
                                   users=results)

        elif res1[3] =="fof" and res1[2]=="public":
            ry = "select * from user_reg where uid='" + frndid + "'"
            print(ry)
            c = conn()
            res = c.selectone(ry)
            if res is not None:
                ss = "select * from tbl_friend where (uid in (select uid from tbl_friend where frid='" + our_id + "') or (select frid from tbl_friend where uid='" + our_id + "') and (frid='" + frndid + "')) or(((frid in (select uid from tbl_friend where frid='" + our_id + "') or (select frid from tbl_friend where uid='" + our_id + "'))) and (uid='" + frndid + "'))"
                results = c.jsonsel(ss)
                if len(results)>0:
                    qry1 = "select * from tbl_request where (fid='" + frndid + "' and uid='" + our_id + "') or (fid='" + our_id + "' and uid='" + frndid + "')"
                    res1 = c.selectone(qry1)
                    print(res1)
                    if res1 is not None:
                        stat = res1[3]
                        return jsonify(status="ok", mail=res[1], name=res[2], gender=res[3], image=res[4], stat=stat,
                                       users=results)
                    else:
                        return jsonify(status="ok", mail=res[1], name=res[2], gender=res[3], image=res[4], stat="no",
                                       users=results)
                else:
                    return jsonify(status="ok", mail=res[1], name=res[2], gender=res[3], image=res[4], stat="no",
                                   users=results)
        else:
            return jsonify(status="no")

    else:
        return jsonify(status="no")

@app.route("/security",methods=['POST'])
def desec():
    uid=request.form["uid"]
    profile=request.form["profile"]
    requ=request.form["request"]
    post=request.form["post"]
    s="SELECT * FROM tbl_privacy where userid='"+uid+"' "
    c=conn()
    res=c.selectone(s)
    if res is not None:
        ss="update tbl_privacy set post='"+post+"',profile='"+profile+"',request='"+requ+"' where userid='"+uid+"'"
        c.nonreturn(ss)
    else:
        ss = "insert into tbl_privacy(post,profile,request,userid) values('" + post + "','" + profile + "','" + requ + "','" + uid + "')"
        c.nonreturn(ss)
    return jsonify(status="ok")

@app.route("/viewsecurity",methods=['POST'])
def showsecurity():
    uid=request.form["uid"]
    s="SELECT * FROM tbl_privacy where userid='"+uid+"'"
    c=conn()
    res=c.selectone(s)
    if res is not None:
        return jsonify(status="ok",profile=res[3],request=res[4],post=res[2])
    else:
        return jsonify(status="no")


@app.route('/sendcomplaints',methods=['post'])
def sendcomplaints():
    db=Db()
    lid=request.form['lid']
    com=request.form['comp']
    r={}
    res=db.insert("insert into `complaint`(`complaint_id`,`complaint`,`complaint_date`,`reply`,`reply_date`,`user_id`) values ( '','"+com+"',curdate(),'pending','0000-00-00','"+lid+"');")
    if int(res)>0:
        r['status']="ok"
    else:
        r['status']="none"
    return demjson.encode(r)


@app.route('/viewcompnt',methods=['post'])
def viewcompnt():
    db=Db()
    lid=request.form['lid']
    print(lid)
    r={}
    res=db.select("select * from  `complaint` where user_id='"+lid+"'")
    # print(res)
    if len(res)>0:
        r['status']="ok"
        r['data']=res
        # print(res)
    else:
        r['status']="none"
    return demjson.encode(r)




@app.route('/sendfeedback',methods=['post'])
def sendfeedback():
    db=Db()
    lid=request.form['lid']
    com=request.form['feedback']
    r={}
    res=db.insert("insert into `feedback`(`feedback_id`,`user_id`,`feedback`,`feedback_date`) values ( '','"+lid+"','"+com+"',curdate());")
    if int(res)>0:
        r['status']="ok"
    else:
        r['status']="none"
    return demjson.encode(r)


@app.route('/viewfeedback',methods=['post'])
def viewfeedback():
    db=Db()
    lid=request.form['lid']
    r={}
    res=db.select("SELECT * FROM feedback,user_reg WHERE feedback.user_id=user_reg.uid")
    if len(res)>0:
        r['status']="ok"
        r['data']=res
    else:
        r['status']="none"
    return demjson.encode(r)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

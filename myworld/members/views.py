from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Members
from django.urls import reverse
from django.db.models import Q
# Create your views here.
import psycopg2
import random




def search_all(table_name):
    conn=psycopg2.connect(database='movie_databse',user='gaussdb',password='2001CCMqwe@',
                      host='172.24.160.1',port='15432')
    # 创建cursor对象：
    cursor = conn.cursor() 
    # 使用cursor对象来执行SQL语句。
    cursor.execute("select * from "+table_name)
    res=[]
    
    tmp=cursor.fetchall()
    conn.commit()
    
    
    cursor.execute("select column_name from information_schema.columns  \
                    where table_schema='public' and table_name='"+table_name+"';")
    tmp_idx=cursor.fetchall()
    conn.commit()
    conn.close()

    for i in range(len(tmp)):
        res.append({})
        for j in range(len(tmp[i])):  
            res[i][tmp_idx[j][0]]=tmp[i][j]  
    
    return res


def add_to_table(x,y,z):
    t=search_all('cinema')
    if not(x.isdigit()):
        return False
    for var in t:
        if(int(var['cinema_id'])==int(x)):
            return False
    
    conn=psycopg2.connect(database='movie_databse',user='gaussdb',password='2001CCMqwe@',
                      host='172.24.160.1',port='15432')
    cursor = conn.cursor() 
    cursor.execute("INSERT INTO CINEMA VALUES ('"+ x +"', '"+ y +"', '"+z+"');")
    conn.commit()
    conn.close()


def delete_record(id):
    conn=psycopg2.connect(database='movie_databse',user='gaussdb',password='2001CCMqwe@',
                      host='172.24.160.1',port='15432')
    cursor = conn.cursor() 
    cursor.execute("DELETE FROM cinema where CINEMA_ID='"+ str(id) +"'")
    conn.commit()
    conn.close()

def update_record(x,y,z):
    t=search_all('cinema')
    #for var in t:
    #    if(int(var['cinema_id'])==int(x)):
    #        return False
    
    conn=psycopg2.connect(database='movie_databse',user='gaussdb',password='2001CCMqwe@',
                      host='172.24.160.1',port='15432')
    cursor = conn.cursor() 
    
    cursor.execute("update cinema set name='"+y+"',address='"+z+"' where CINEMA_ID='"+ str(x) +"'")
    
    conn.commit()
    conn.close()
    return True

def index(request):

    mymem=Members.objects.all().values()
    # 返回指定记录：
    # mydata = Members.objects.filter(firstname='Emil').values()
    # mydata = Members.objects.filter(Q(firstname='Emil') | Q(firstname='Tobias')).values()
    # 排序：
    # mydata = Members.objects.all().order_by('firstname').values()
    movies=search_all("movie")
    template=loader.get_template('index.html')
    context={'movie':movies,}
    
    return HttpResponse(template.render(context,request))


def login(request):

    template=loader.get_template('login.html')
    tmp=search_all('words')
    num=len(tmp)
    i=random.randint(0,num-1)
    print(i)
    res=tmp[i]
    context={'words':res,}
    return HttpResponse(template.render(context,request))

def check(request):
    user=search_all("user_")
    x=request.POST['Email']
    y=request.POST['Password']
    flag=0
    statu=0
    for var in user:
        if var['email']==x and var['pass_word']==y:
            flag=1
            statu=var['role_']
            break
    # 用户名密码正确且为用户
    if flag==1 and statu==0:
        return HttpResponseRedirect(reverse('index'))

    # 用户名密码正确且为管理员
    elif flag==1 and statu==1:
        return HttpResponseRedirect(reverse('adminpage'))
    else:
        return HttpResponseRedirect(reverse('login'))


def add(request):
    template=loader.get_template('add.html')
    return HttpResponse(template.render({},request))

def addrecord(request):
    x=request.POST['cid']
    y=request.POST['name']
    z=request.POST['address']

    flag=add_to_table(x,y,z)
    if (flag==False):
        return HttpResponseRedirect(reverse('faultpage'))
    return HttpResponseRedirect(reverse('adminpage'))

#第三步，执行对应的view
def delete(request,id):
    delete_record(id)
    return HttpResponseRedirect(reverse('adminpage'))

def update(request,id):
    cid=id
    cinema=search_all('cinema')
    updatecinema={}
    for var in cinema:
        if (int(var['cinema_id'])==int(cid)):
            updatecinema=var
    contex={'cinema':updatecinema,}
    template=loader.get_template('update.html')
    return HttpResponse(template.render(contex,request))

def updaterecord(request,id):
    x=request.POST['cid']
    y=request.POST['name']
    z=request.POST['address']
    
    flag=update_record(x,y,z)

    if (flag==False):
        return HttpResponseRedirect(reverse('faultpage'))

    return HttpResponseRedirect(reverse('adminpage'))

def infopage(request,id):
    # 获取该电影页面
    mov=[]
    tmp=search_all("movie")
    for var in tmp:
        if int(var['movie_id'])==id:
            mov=var
            break
    

    # 获取重映场次
    session=[]
    tmp=search_all("session_")
    for var in tmp:
        if(var['movie_id']==id):
            session.append(var)

    # 获取该电影重映的影院
    cinma=[]
    tmp=search_all('cinema')
    
    history=[]
    for var in session:
        ci_id=var['cinema_id']

        if ci_id not in history:
            cinma.append(tmp[int(ci_id)-1])
            history.append(ci_id)
    
    # 获取该影院的所有放映厅
    hall=[]
    tmp=search_all('hall')
    for dyy in cinma:
        cid=int(dyy['cinema_id'])
        for var in tmp:
            if (int(var['cinema_id'])==cid):
                hall.append(var)

    # 获取关于该电影的评论
    comments=[]
    tmp=search_all('comments_')
    for var in tmp:
        if var['movie_id']==id:
            comments.append(var)

    # 根据评论表中的用户id找到对应的用户名称
    user=[]
    uhistory=[]
    tmp=search_all('user_')
    for var1 in comments:
        uid=int(var1['user_id'])
        if uid not in uhistory:
            uhistory.append(uid)
        else:
            break
        for var2 in tmp:
            if int(var2['user_id'])==uid:
                user.append(var2)
    
    # 用户头像
    template=loader.get_template('infopage.html')
    
    context={'movie':mov,'session':session,'cinema':cinma,'hall':hall,'comment':comments,'user':user,}
    return HttpResponse(template.render(context,request))

# 查找页面
def searches(request):
    name=request.POST['search']
    print('name:',name)
    allmov=search_all('movie')
    match=[]
    # 英文名或中文名
    for m in allmov:
        if name in m['name'] or name in m['foreignname']:
            match.append(m)
    template=loader.get_template('searches.html')


    context={'matches':match,}
    
    return HttpResponse(template.render(context,request))

# adminpage
def adminpage(request):
    movie=search_all('movie')
    cinema=search_all('cinema')
    hall=search_all('hall')
    session=search_all('session_')
    user_=search_all('user_')
    words=search_all('words')
    template=loader.get_template('adminpage.html')
    context={'cinema':cinema,
             'hall':hall,
             'session':session,
             'user':user_,
             'words':words,
             'movie':movie,
            }
    
    return HttpResponse(template.render(context,request))

def faultpage(request):
    template=loader.get_template('faultpage.html')
    return HttpResponse(template.render({},request))
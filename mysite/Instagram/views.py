from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Count

from django.shortcuts import render , redirect
from .models import  User , Post , Comments , Subscriber ,PostDetails, Seens  , Likes , Message
import hashlib, os
from django.contrib import messages
from django.core.exceptions import ValidationError
import json 
from django.http import JsonResponse
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
import datetime
from datetime import timedelta
from django.core import serializers
import math 
from twisted.internet import task, reactor
import time
from background_task import background
t=time.time()
from django.http import HttpResponse, Http404


@background(schedule=10)
def notify_user(user_id):
    # lookup user by id and send them a message
    user = User.objects.filter(id=int(user_id)).update(Status=False)
    user = User.objects.filter(id=int(user_id)).update(OfflineTime=datetime.datetime.now())
    
    
def admin(request):
    
    try:        
        password = "1234567"
        if not  User.objects.filter(Email="admin@gmail.com").exists():
            user=User(
                First_Name="Admin",
                Last_Name="Admin",
                Email="admin@gmail.com"  , 
                Password=make_password(password.encode('utf-8')), 
                Role = "admin",
                Is_Email_Verified=1
                )
            user.save()    
    except Exception:    
        return redirect('/signin')

def StartUp(request):
    admin(request)

def check_password(hash, password):
    """Generates the hash for a password and compares it."""
    generated_hash = make_password(password)
    return hash == generated_hash

def make_password(password):
    assert password
    hash = hashlib.md5(password).hexdigest()
    return hash

def check_password(hash, password):
    """Generates the hash for a password and compares it."""
    generated_hash = make_password(password)
    return hash == generated_hash


def IsAuthentcated(request):
    
    try:
        StartUp(request)
        if  request.session.get('email', False) == False:
            return False
        else:
            return True        
    except Exception:
        return True


def signin(request):
    
    StartUp(request)
    if IsAuthentcated(request) == True:
       return redirect('/insta')
    else:
        
        if request.method == 'POST':
             
            loginusername = request.POST['email']
            loginpassword = request.POST['password']
            try:
                user = User.objects.get(Email = loginusername)
                if user is not None:
                    if(check_password(user.Password , loginpassword.encode('utf-8'))):
                        request.session['firstname'] = user.First_Name
                        request.session['lastname'] = user.Last_Name
                        
                        request.session['email'] = user.Email
                        request.session['role'] = user.Role
                        request.session['id'] = user.id
                        request.session['IsVerified'] = user.Is_Email_Verified
                        request.session['image'] = user.image
                        request.session['username'] = user.Username
                        user.Status=True
                        user.save()

                        # if user.Is_Email_Verified == 0:
                        #     return redirect('confirm_email') 
                        return redirect('/insta')
                    else:
                        messages.error(request, "email or password not correct")    
                        return redirect('signin')
                                            
                else:
                    messages.error(request, "email or password not correct")    
                    return redirect('signin')     
            except Exception:
                messages.error(request, "user not found")    
                return redirect('signin')
        else:
            return render(request, 'Instagram/signin.html')


def signout(request):
    User.objects.filter(Email = request.session.get('email', False)).update(Status=False)
    for key in list(request.session.keys()):
      del request.session[key]
      
    return redirect('signin')

def signup(request):

    if IsAuthentcated(request):
       return redirect('/insta')
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        gender = request.POST['gender']
        
        
        if  User.objects.filter(Email=email).exists():
            print(email)
            messages.error(request , "Account already exists")       
            return render(request ,'Instagram/signup.html')

        if password != confirmpassword:
             messages.error(request , "passwords do not match")       
             return render(request ,'Instagram/signup.html')
       
        password_salt = os.urandom(32).hex()
        hash = hashlib.sha512()
        hash.update(('%s%s' % (password_salt, password)).encode('utf-8'))
        password_hash = hash.hexdigest()
        try:

            user = User(
                First_Name = firstname,
                Last_Name = lastname,
                Email = email,
                Password = make_password(password.encode('utf-8')),
                Gender = gender,
            )
            user.save()
            user.full_clean()
            request.session['firstname'] = user.First_Name
            request.session['lastname'] = user.Last_Name
            
            request.session['email'] = user.Email
            request.session['username'] = user.Username
            
            request.session['role'] = user.Role
            request.session['id'] = user.id
            request.session['image'] = user.image.url
            request.session['IsVerified'] = False
            return redirect('/insta')    
        except ValidationError as e:
            for i in e.messages:
              messages.error(request , i)
            return render(request ,'Instagram/signup.html')                
        # return redirect('confirm_email')
    else:
        return render(request ,'Instagram/signup.html')

    return render(request ,'Instagram/signup.html')


def profile(request):
    user_id = ""    
    if IsAuthentcated(request) == False:
       return redirect('signin')
    if request.method == 'POST':
       response_data = {}     
       picture=request.POST['image']
       if picture:
            now = datetime.datetime.now()
            user = User.objects.get(Email = request.session.get('email', False))
            user.image =picture
            user.save() 
            request.session['image']=picture
            response = {
                         'msg':'Your form has been submitted successfully' # response message
            }
            return JsonResponse(response) # return response as JSON
    else:  
        user_id=request.GET['user_id'] 

    
    user = User.objects.get(id=int(user_id))
    posts = Post.objects.filter(User_id = int(user.id)).all(); 
    allPostDetails=[]
    for i in posts:
        item=PostDetails(
            post=i,
            comments =getPerfectCount(request, Comments.objects.filter(Post_id = int(i.id)).count()),
            likes=getPerfectCount(request, Likes.objects.filter(LikedPost_id = int(i.id)).count())
        )
        allPostDetails.append(item)
    parem = {'user' : user , 'posts':allPostDetails , 'total_posts':getPerfectCount(request,len(posts)) }
    return render(request ,'Instagram/profile.html' , parem)

def getPerfectCount(request , number):
    if number > 1000:
       return str(number/1000)+"k" 
    return number   

def main(request):

    if IsAuthentcated(request) == False:
       return redirect('signin')
    else:

        ids=[]
        mySeens=[]

        for i in Seens.objects.filter(SeenUser_id = int(request.session.get('id', False))).all():
            mySeens.append(i.SeenPost.id)

        for i in Subscriber.objects.filter(SubscriberUser_id = int(request.session.get('id', False))).only('SubscribedUser_id'):
            ids.append(i.SubscribedUser.id)
        ids.append(int(request.session.get('id', False)))
        #suggested frieds on left side
        suggestions = User.objects.exclude(id__in=ids).filter(~Q(id = int(request.session.get('id', False)))).all()    
        print()
        subcribers = Subscriber.objects.filter(SubscriberUser_id = int(request.session.get('id', False))).all()    

        subcribers_ids = subcribers.only('SubscribedUser_id')
        posts = Post.objects.filter(User_id__in=ids).all().order_by('-DateTime')
        parem  = {  'posts' : posts , 'suggestions':suggestions , 'subcribers': subcribers}   
    return render(request ,'Instagram/main.html' , parem)
def search(request):
    user = User.objects.filter(Q(Username__startswith=request.GET['value'])  | Q(Email__startswith=request.GET['value']) | Q(First_Name__startswith=request.GET['value']) | Q(Last_Name__startswith=request.GET['value'])).values()
    return JsonResponse({"list": list(user)})

def post_seen(request):
    id = request.GET['id']

    if  Seens.objects.filter(SeenUser_id = int(request.session.get('id', False))).filter(SeenPost_id = int(id)).exists() == False:
        seen = Seens(
            SeenUser = User.objects.get(id = int(request.session.get('id', False))),
            SeenPost = Post.objects.get(id = id),
            
        )
        seen.save()
    return JsonResponse({"list": 'list(user)'})

def update_my_status(request):
    id = request.session.get('id', False)
    t=time.time()
    notify_user(id)
    User.objects.filter(id = int(id)).update(Status = True)
    user = User.objects.get(id = int(id))

    return JsonResponse({"OfflineTime": user.OfflineTime , "Status":user.Status})


def getLikes(request , id):
    count = Likes.objects.filter(LikedPost_id = int(id)).count()
    return count

def get_last_message(request):
    
    messageslist = []
    messages = Message.objects.filter( Q(Reciever_id =int(request.session.get('id', False))) | Q(Sender_id =int(request.session.get('id', False))) ).values('Sender_id', 'Description', 'Status','Reciever_id','Type').order_by('DateTime') # ensure you add the order_by()Message.objects.group_by('Reciever_id')
    for i in messages:
        messageslist.append(i)
    return JsonResponse({"messageslist": messageslist  })

def chat(request):
    id = int(request.GET['id'])

    ids=[]

    for i in Subscriber.objects.filter(SubscriberUser_id = int(request.session.get('id', False))).only('SubscribedUser_id'):
        ids.append(i.SubscribedUser.id)

    users = User.objects.exclude(id = int(request.session.get('id', False))).all()
    parem= {"users":list(users) , 'id' : id   }    
    return render(request ,'Instagram/chat.html' , parem)

def update_message(request):
    messages = Message.objects.filter(Reciever_id = int(request.session.get('id', False))).filter( ~Q(Status ="seen")).count()
    return JsonResponse({"message_count": messages  })

def user_status(request):

    id = request.GET['id']
    user = User.objects.get(id = int(id))

    return JsonResponse({"status": user.Status , "offline_time":user.OfflineTime  })

def save_message(request):
    reciever = request.POST['id']
    message = request.POST['message']
    print(message)
    message = Message(
            Description = message,
            Sender = User.objects.get(id = int(request.session.get('id', False))),
            Reciever = User.objects.get(id = int(reciever)),
    )
    message.save()
    return JsonResponse({"status": True , "id":message.id})

def status_message(request):
    reciever = request.GET['id']
    messageslist = []
    message = Message.objects.filter(Reciever = int(reciever)).filter(Sender = int(request.session.get('id', False))).filter( Q(Status='delievered') | Q(Status='sent') | Q(Status='seen') )
    for i in message:
        item ={
            'id':i.id,
            'Description':i.Description,
            'Status':i.Status,
            'Sender':{'id':i.Sender.id},
            'Reciever':{'id':i.Reciever.id},
            'DateTime':i.DateTime,
            
        }
        
        messageslist.append(item)
    response={
        'messages':messageslist
    }    
    return JsonResponse(response)


def update_all_comments(request):

    comments = Comments.objects.all()
    seenList = []
    response={}
    for i in comments:
        if  str(request.session.get('id', False)) not in i.SeenUsers:
            i.SeenUsers.append(request.session.get('id', False)) 
            i.save()
            response = {
                                    'image':i.User.image ,
                                    'username':i.User.Username ,
                                    'description':i.Description,
                                    'datetime':i.DateTime ,
                                    'post_id':i.Post.id ,
                                    'id':i.id ,
                                    'total':Comments.objects.filter(Post_id = i.Post_id).count()
                                    
                                    
                                    
                        }
    
            return JsonResponse(response)
    return JsonResponse(response)

def seen_all_messages(request):
    reciever = request.GET['id']
    message = Message.objects.filter(Sender = int(reciever)).filter(Reciever  = int(request.session.get('id', False))).filter(Status='delievered').update(Status='seen')
    
    response={
        'messages':'seen'
    }    
    return JsonResponse(response)


def get_messages(request):
    reciever = request.GET['id']
    messageslist = []
    message = Message.objects.filter(Sender = int(reciever)).filter(Reciever = int(request.session.get('id', False))).filter(Status='sent')
    for i in message:
        item ={
            'id':i.id,
            'Description':i.Description,
            'Status':i.Status,
            'Sender':{'id':i.Sender.id},
            'Reciever':{'id':i.Reciever.id},    
            'DateTime':i.DateTime,
            'Type':i.Type,
            'Url':i.Url,
            
        }
        messageslist.append(item)
        i.Status="delievered"
        i.save()
    response={
        'messages':messageslist
    }    
    return JsonResponse(response)

def get_all_messages(request):
    reciever = request.GET['id']
    messageslist = []
    message = Message.objects.filter(Q(Reciever = int(reciever)) | Q( Sender = int(reciever)  ) ).filter( Q( Sender = int(request.session.get('id', False))  )      | Q( Reciever = int(request.session.get('id', False))))
    for i in message:
        item ={
            'id':i.id,
            'Description':i.Description,
            'Status':i.Status,
            'Sender':{'id':i.Sender.id},
            'Reciever':{'id':i.Reciever.id},    
            'DateTime':i.DateTime,
            'Type':i.Type,
            'Url':i.Url,
            
            
        }
        messageslist.append(item)
        
    response={
        'messages':messageslist
    }    
    return JsonResponse(response)


def get_Likes(request):
    id = request.GET['id']

    if  Likes.objects.filter(LikerUser_id = int(request.session.get('id', False))).filter(LikedPost_id = int(id)).exists():
        return JsonResponse({"like": True , "count":getLikes(request , id)})
    else:    
        return JsonResponse({"like": False , "count":getLikes(request , id) })

def like_seen(request):
    id = request.GET['id']

    if  Likes.objects.filter(LikerUser_id = int(request.session.get('id', False))).filter(LikedPost_id = int(id)).exists():
        Likes.objects.filter(LikerUser_id = int(request.session.get('id', False))).filter(LikedPost_id = int(id)).delete()    
        return JsonResponse({"like": False , "count":getLikes(request , id)})
    else:    
        like = Likes(
            LikerUser = User.objects.get(id = int(request.session.get('id', False))),
            LikedPost = Post.objects.get(id = int(id)),
            
        )
        like.save()

        return JsonResponse({"like": True , "count":getLikes(request , id) })


def upload_photos(request):

    if request.method == 'POST' and request.FILES['images']:
        images=request.FILES.getlist('images')   
        folder='media/photos/'
        post = Post()
        post.Type="image"
        photos = [] 
        for i in images:
            now = datetime.datetime.now()
            myfile = i
            fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
            filename = fs.save(now.strftime("%d%m%Y%H%M%S")+'.jpg', myfile)
            file_url = fs.url(filename)
            item = "/"+folder+filename
            photos.append(item)
        post.Photos = photos
        post.Title = request.POST['title']
        post.Description = request.POST['description']
        post.User = User.objects.get(id = int(request.session.get('id', False)) )
        post.save()     
    return render(request ,'Instagram/upload_photos.html')

def single_post(request):
    id = request.GET['id']
    post  = Post.objects.filter(id = int(id))
    parem = {'posts' : post}
    return render(request ,'Instagram/single_post.html' , parem )


def share_post(request):
    reciever = request.POST['user_id']
    message = request.POST['image']
    
    message = Message(
            Type = "image",
            Url = request.POST['post_id'],
            Description = message,
            Sender = User.objects.get(id = int(request.session.get('id', False))),
            Reciever = User.objects.get(id = int(reciever)),
    )
    message.save()
    return JsonResponse({"status": True , "id":message.id})

def upload(request):

    if request.method == 'POST':
       title = request.POST['title']
       description = request.POST['description']
       picture = ''
       vedio = request.POST['vedio']
       try:
        if request.POST['picture'] == '':
                messages.error(request, "Upload vedio cover picture")    
                return render(request ,'Instagram/upload.html')
       except Exception :
           picture = request.FILES['picture']
       if vedio == '':
            messages.error(request, "Upload vedio file")    
            return render(request ,'Instagram/upload.html')
       post = Post(
          Title = title,
          Description=description,
          Image = picture,
          Vedio = vedio,
          User = User.objects.get(id = int(request.session.get('id', False)) ) 
       )
       post.save()
       messages.success(request, "Post uplaoded successfully")    

    return render(request ,'Instagram/upload.html')


def upload_comments(request):
    if request.method == 'POST':
        
        if request.POST['description']==None:
            return JsonResponse(response)    
        comment = Comments(
            Description = request.POST['description'],
            Post = Post.objects.get(id = int(request.POST['post_id'])),
            User = User.objects.get(id = int(request.session.get('id', False))),
        ) 
        comment.save()
        response = {
                                'image':comment.User.image ,
                                'username':comment.User.Username ,
                                'description':comment.Description,
                                'datetime':comment.DateTime ,
                                'post_id':comment.Post.id ,
                                'id':comment.id ,
                                
                                
                                
                    }
        return JsonResponse(response)


def subscribe(request):
    if request.GET['id']:

        subscriber = Subscriber(
            SubscriberUser= User.objects.get(id = int(request.session.get('id', False))),
            SubscribedUser= User.objects.get(id = int(request.GET['id'])),
        )
        subscriber.save()

        response = {
                                'comments':'allComments' # response message
                    }
        return JsonResponse(response) 

def delete_comment(request):
    if request.GET['id']:
        comment = Comments.objects.get(id=int(request.GET['id'])); 
        Comments.objects.filter(id=int(request.GET['id'])).delete();    
        response = {
                                'post_id':comment.Post.id # response message
                    }
        return JsonResponse(response) 


def get_correct_time(request , value):

    if value <= 60 and value > 10:
       return '1s ago'
    elif value > 60 and value < 3600:
       return str(math.floor(value/60))+"m ago"     
    elif value > 60 and value < 3600:
       return str(math.floor(value/60))+"m ago"     
    elif value > 3600 and value < 86400:
       return str(math.floor((value/60)/60))+"h ago"     
    elif value > 86400 and value < 86400*7:
       return str(math.floor(((value/60)/60)/24))+"d ago"     
    elif value > 86400*7 and value < 86400*7*30:
       return str(math.floor((((value/60)/60)/24)/7))+"w ago"     
    elif value > 86400*7*30 and value < 86400*7*30*12:
       return str(math.floor(((((value/60)/60)/24)/7)/30))+"month ago"
    elif value > 86400*7*30*12:
       return str(math.floor((((((value/60)/60)/24)/7)/30)/12))+"years ago"
            
    return 'just now'


def comments_time(request):
    commentsTime=[]
    PostsTime=[]
        
    #section for calculating the comments time
    for i in Comments.objects.all():
        datetimeFormat = '%Y-%m-%d %H:%M:%S'
        date1 = str(datetime.datetime.today()).split('.')[0]
        date2 = str(i.DateTime).split('.')[0] 
        diff = datetime.datetime.strptime(date1, datetimeFormat)-datetime.datetime.strptime(date2, datetimeFormat)
        response = {
                       'comment_id': i.id ,
                       'duration': get_correct_time(request , diff.seconds),
                       'post_id': i.Post.id,                       
                   }
        commentsTime.append(response)

    #section for calculating the comments time
    for i in Post.objects.all():
        datetimeFormat = '%Y-%m-%d %H:%M:%S'
        date1 = str(datetime.datetime.today()).split('.')[0]
        date2 = str(i.DateTime).split('.')[0] 
        diff = datetime.datetime.strptime(date1, datetimeFormat)-datetime.datetime.strptime(date2, datetimeFormat)
        response = {
                       'post_id': i.id ,
                       'duration': get_correct_time(request , diff.seconds),
                   }
        PostsTime.append(response)




    finalresponse = {
                    'commentsTime': commentsTime,
                    'PostsTime': PostsTime,                   
                }            
                   
    return JsonResponse(finalresponse) 

        
def unsubscribe(request):
    if request.GET['id']:
        print(request.GET['id'])
        Subscriber.objects.filter(SubscribedUser_id = int(request.GET['id'])).filter(SubscriberUser_id = int(request.session.get('id', False))).delete()
        response = {
                                'comments':'allComments' # response message
                    }
        return JsonResponse(response) 


def get_all_comments(request):
     
     allComments=[]
     comments = Comments.objects.all()
     for i in comments:
         response = {
                                'image':i.User.image ,
                                'username':i.User.Username ,
                                'description':i.Description,
                                'datetime':i.DateTime ,
                                'post_id':i.Post.id ,
                                'id':i.id ,
                                
                                
                    }
         allComments.append(response);  

     response = {
                                'comments':allComments # response message
                    }
     return JsonResponse(response)               

def upload_image_file(request):
    if request.method == 'POST':
        vedio=request.FILES['images']   
        folder='media/images/' 
        now = datetime.datetime.now()
        if request.method == 'POST' and request.FILES['vedio']:
            myfile = request.FILES['images']
            fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
            filename = fs.save(now.strftime("%d%m%Y%H%M%S")+'.jpg', myfile)
            file_url = fs.url(filename) 
            response = {
                                'file':filename # response message
                    }
            return JsonResponse(response)
    raise Http404    


def upload_vedio_file(request):
    if request.method == 'POST':
        vedio=request.FILES['vedio']   
        folder='media/vedios/' 
        now = datetime.datetime.now()
        if request.method == 'POST' and request.FILES['vedio']:
            myfile = request.FILES['vedio']
            fs = FileSystemStorage(location=folder) #defaults to   MEDIA_ROOT  
            filename = fs.save(now.strftime("%d%m%Y%H%M%S")+'.mp4', myfile)
            file_url = fs.url(filename) 
            response = {
                                'file':filename # response message
                    }
        return JsonResponse(response)
    return render(request ,'Instagram/upload.html')

from main import livelines_algo
from main.models import Attendance, UserProfile, Request, Notification
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User, auth
from django.contrib import messages
import base64
from django.core.files.base import ContentFile
import json
import datetime;
from . import recogniser_algo, livelines_algo
# from .models import UserProfile
# from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def about(request):
    return render(request, 'about.html')


# def recognition(request):
#     if request.method == "POST":
#         _user = UserProfile.objects.get(user=request.user)
#         data = request.POST['image']
#         bias = int(request.POST['bias'])
#         format, imgstr = data.split(';base64,') 
#         ext = format.split('/')[-1] 
#         data = ContentFile(base64.b64decode(imgstr), name=f'{request.user.username}{datetime.date.today()}.' + ext)
#         if recogniser_algo.recognizer(str(request.POST['image']), _user.image.url):
#             att = Attendance(user_id=_user, image=data, date=datetime.date.today(), in_time=timezone.localtime(), out_time=timezone.localtime(), is_absent=False)
#             att.save()
#             msgDate = str(timezone.localtime())
#             messages.info(request, f'Hi, {request.user.first_name}, A very good morning to you. Your attedance has been recorde for {datetime.date.today()} at {msgDate[10:19]} Have a great day!')
#             return redirect('/')
#         else:
#             messages.info(request, f'It seems like there was an error with the last operation. Please take a moment to get another picture and try again. CONTACT SUPPORT TEAM IF ERROR PRESISTS!')
#             return render(request, 'index.html')
#     else:
#         return render(request, 'index.html')

# def recognition(request):
#     if request.method == "POST":
#         data = request.POST['image']
#         format, imgstr = data.split(';base64,') 
#         ext = format.split('/')[-1] 
#         data = ContentFile(base64.b64decode(imgstr), name=f'v_image{datetime.date.today()}.' + ext)
#         _user = recogniser_algo.recognizer(str(request.POST['image']))
#         if _user is not False:
#             att = Attendance(user_id=_user, image=data, date=datetime.date.today(), in_time=timezone.localtime(), out_time=timezone.localtime(), is_absent=False)
#             att.save()
#             msgDate = str(timezone.localtime())
#             messages.info(request, f'Hi, {_user.user.first_name}, A very good morning to you. Your attedance has been recorde for {datetime.date.today()} at {msgDate[10:19]} Have a great day!')
#             return redirect('/')
#         else:
#             messages.info(request, f'It seems like there was an error with the last operation. Please take a moment to get another picture and try again. CONTACT SUPPORT TEAM IF ERROR PRESISTS!')
#             return render(request, 'index.html')
#     else:
#         return render(request, 'index.html', {'subject': 'subject'})

def face_authentication(request):
    if request.method == "POST":
        subject = request.POST['subject']
        is_real = livelines_algo.liveliness_detection()
        if (is_real == 0):
            messages.info(request, f'We could not detect any face. Try improving the lightning condition in the room')
            return render(request, 'index.html', {'subject': subject})
        if (is_real == -1):
            messages.info(request, f'The system has identified your image as spoof. It may be an error on our side. Please try again.')
            return render(request, 'index.html', {'subject': subject})
        else:
            _user = recogniser_algo.recognizer()
            if _user is not False:
                is_taken = Attendance.objects.filter(date = datetime.date.today(), subject=subject, user_id=_user)
                if is_taken.exists():
                    messages.info(request, f'Dear, {_user.user.first_name}, Your attendance for this subject has been alredy recorded. Thankyou')
                    return render(request, 'index.html', {'subject': subject})
                att = Attendance(user_id=_user, date=datetime.date.today(), subject=subject, in_time=timezone.localtime(), is_absent=False)
                att.save()
                msgDate = str(timezone.localtime())
                messages.info(request, f'Hi, {_user.user.first_name}, A very good morning to you. Your attedance has been recorde for {datetime.date.today()} at {msgDate[10:19]} Have a great day!')
                return render(request, 'index.html',  {'subject': subject})
            else:
                messages.info(request, f'We could not identify you. Please try again!')
                return render(request, 'index.html', {'subject': subject})
    else:
        return render(request, 'index.html', {'subject': "MCA406"})


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if request.user.is_superuser:
                return redirect('/manage/all_profile')
            else:
                return redirect('/profile')
        else:
            messages.info(request, 'No record Found!!! Please provide correct details.')
            return redirect('/login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/login')



def profile(request):
    if request.user.is_superuser:
        return redirect('/manage/all_profile')
    else:
        data = UserProfile.objects.get(user=request.user)
        return render(request, 'profile.html', {'data': data})


def attendance(request):
    att = Attendance.objects.filter(user_id=request.user.id).order_by("-date")
    return render(request, 'attendance.html', { 'att':att })


def graphs(request):
    return render(request, 'graphs.html')


def cpassword(request):
    if request.method == "POST":
        old_pass = request.POST['old_pass']
        new_pass = request.POST['new_pass']
        u = User.objects.get(username=request.user.username)
        if u.check_password(old_pass):
            u.set_password(new_pass)
            u.save()
            messages.info(request, 'Password was successfully changed')
            return redirect('/login')
        else:
            messages.info(request, 'Given password was incorrect')
            return redirect('/cpassword')
    else:
        return render(request, 'password.html')


def change(request):
    if request.method == "POST":
        previous_req = Request.objects.filter(user_id=request.user.id, is_pending=True)
        if previous_req.count() > 3:
            messages.info(request, 'You can only have 3 pending requests at any time. Please wait till previous requests are reviewed')
            return redirect('/profile')
        data_dict = {
            "username":request.POST['username'],
            "fname":request.POST['fname'],
            "lname":request.POST['lname'],
            "email":request.POST['email'],
            "address":request.POST['address'],
            "contact":request.POST['contact'],
            "dob":request.POST['dob'],
            "join":request.POST['join']
        }
        data = json.dumps(data_dict, sort_keys=True)
        userid = UserProfile.objects.get(user=request.user)
        req = Request(user_id=userid, data=data, file=request.FILES['file'])
        req.save()
        messages.info(request, 'Request made successfully...')
        return redirect('/profile')
    else:
        data = UserProfile.objects.get(user=request.user)
        return render(request, "change.html", {'data': data})


def notification(request):
    if request.method == "POST":
        reqid = Request.objects.get(id=request.POST['reqid'])
        userid = request.POST['userid']
        msg = request.POST['msg']
        notify = Notification(user_id=userid, req_id=reqid, is_approved=False, message=msg)
        notify.save()
        req = Request.objects.get(id=request.POST['reqid'])
        req.is_pending = False
        req.save()
        return redirect('/manage/requests')
    else:
        req = Request.objects.filter(user_id=request.user.id, is_pending=True).order_by("-id")
        # req = Request.objects.filter(user_id=request.user.id)
        final = Notification.objects.filter(user_id=request.user.id).order_by("-id")
        # final = zip(req, data)
        return render(request, 'notifications.html', { 'req':req, 'final':final })
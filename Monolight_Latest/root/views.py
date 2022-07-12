from numpy import record
from main.models import Attendance, UserProfile, Request, Notification
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
# from .models import UserProfile
# from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def all_profile(request):
    if request.user.is_superuser:
    	data = UserProfile.objects.exclude(desg="Superuser")
    	return render(request, 'all_profile.html', {'data': data})
    else:
    	return render(request, '404.html')


def all_attendance(request):
    if request.user.is_superuser:
        if request.method == "POST":
            pass
        else:
            record = Attendance.objects.filter(subject='MCA4012')
            total = UserProfile.objects.filter(branch='MCA')
            data = {
                'subject': 'MCA4012',
                'date':record[0].date,
                'present': len(record),
                'total': 105
            }
            return render(request, 'all_attendance.html', {'record': record, 'data':data})
    else:
        return render(request, '404.html')


def all_graphs(request):
    if request.user.is_superuser:
        return render(request, 'all_graphs.html')
    else:
        return render(request, '404.html')



def requests(request):
    if request.user.is_superuser:
        req = Request.objects.exclude(is_pending=False).order_by("-id")
        # old = Request.objects.exclude(is_pending=True).order_by("-id")
        final = Notification.objects.all().order_by("-id")
        # final = zip(old, data)
        return render(request, 'request.html', {"req":req, "final":final})
    else:
        return render(request, '404.html')

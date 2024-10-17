from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Package,Subject
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
import uuid
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
import httpagentparser
from django.db import transaction
import uuid
import random ,time
import string
from django.core.mail import send_mail


def generate_code():
    return 'MTS'.join(random.choices(string.ascii_letters + string.digits, k=6))



def home(request):    
    video = Videos.objects.all()
    context = {
        'video' : video
    }
    return render(request,'index.html',context)


def exper(request):
    expr =  Services.objects.all()
    searched = ''
    if request.method == 'POST':
        searched = request.POST['searched']
        expr = Services.objects.filter(name__contains=searched)
        if expr:
            messages.add_message(request, messages.SUCCESS, ' طلبك موجود ✔️✔️')
        else:
            messages.add_message(request, messages.SUCCESS, ' طلبك غير موجود ❌❌')
            return redirect('exper')
    
    context = {
        'expr':expr,
        'searched':searched,

    }
    return render(request,'exper.html',context)





@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request, messages.SUCCESS, ' تم تغيير كلمة السر بنجاح')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'students/change_password.html', {'form': form})



@transaction.atomic
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            device_id = str(uuid.uuid4())  # Generate a unique ID for the device 
            user.profile.device_id = device_id
            user.profile.save()
            login(request, user)
            logout(request)
        # Set the device ID in the browser's cookies
            confirmation_code = generate_code()


            subject = 'كود خصم الأستاذة الدمرداش'
            message = f"""
                📝 **انسخ الكود الخاص بك وأرسله إلى الأستاذة لإكمال إجراءات الدفع:**
                         
                📧  **البريد الإلكتروني**: {user.email}    
                     
                💼 **اسم الباقة**: {user.package.name}

                🔑 **{confirmation_code}**

                🌐 يمكنك زيارة الرابط التالي لمزيد من التفاصيل:
                    https://t.me/AL_Demerdash12

                💡 **نصيحة**: قم بنسخ الكود واسم الباقة وإرسالها إلى تليغرام الأستاذة .
                """
            recipient_list  = [form.cleaned_data['email']]

            send_mail(subject,message,'mtsmy31@gmail.com', recipient_list,fail_silently=False)
            
            response = HttpResponseRedirect('/paid')

            response.set_cookie(
                'device_id',  # Cookie name
                device_id,  # Cookie value
                max_age=365*24*60*60,  # 1 year expiration
                httponly=True,  # Prevent JavaScript access
                secure=False,  # False for localhost, True for HTTPS
                samesite='Lax',  # Cross-site cookie handling
                path='/'  # Accessible throughout the site
            ) 
            return response # Redirect to a home page after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})



def custom_logout(request):
    if request.method == 'GET':
        logout(request)
        messages.success(request, 'تم تسجيل خروجك , ننتظر عودتك ')
        return HttpResponseRedirect(reverse('login'))  
    

    


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate user
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_paid:
                    cookie_device_id = request.COOKIES.get('device_id', None)
                    profile_device_id = user.profile.device_id
                    
                    if profile_device_id is not None:
                        if cookie_device_id and cookie_device_id == profile_device_id:
                            login(request, user)
                            return redirect('student')
                    
                        else:
                        # If the device ID doesn't match or is missing, deny login
                            messages.error(request, 'لا يمكنك تسجيل الدخول من جهاز ومتصفح مختلف.')
                            return redirect('login')
                    
                    
                    elif profile_device_id is None:
                        # Generate a new device_id and save it in the user's profile
                        new_device_id = str(uuid.uuid4())
                        user.profile.device_id = new_device_id
                        user.profile.save()
                        login(request, user)
                        # Set the new device_id in the cookie
                        response = HttpResponseRedirect('/student')
                        response.set_cookie(
                            'device_id',
                            new_device_id,
                            max_age=365*24*60*60,  # 1 year expiration
                            httponly=True,  # Prevent JavaScript access
                            secure=False,  # Set to True for HTTPS
                            samesite='Lax',
                            path='/'
                        )

                        return response


                else:
                    # Redirect to payment page if the user has not paid
                    messages.error(request, 'يجب عليك إكمال الدفع أولاً')
                    return redirect('paid')
            else:
                # Invalid credentials
                messages.error(request, 'اسم المستخدم أو كلمة المرور خطأ')
        else:
            # Form is not valid
            messages.error(request, 'اسم المستخدم أو كلمة المرور خطأ')
    else:
        # If it's a GET request, show the login form
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})




@login_required
def home_student(request):
    user = request.user
    user = User.objects.get(username=user.username)
    subjects = user.subjects.all()

    sub = Subject.objects.all()
    context = {
        'sub' : sub,
        'user': user,
        'subjects': subjects
    }
    return render(request,'students/home.html',context)



@login_required
def profile(request):
    user = request.user
    sub_name = Subject.objects.all()
    return render(request,'students/profile.html',{sub_name:'sub_name'})




def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'تم إرسال رسالتك وسيتم التواصل معك بأقرب وقت')
            return redirect('/')  # Redirect to a home page after registration
    else:
        form = ContactForm()
    context = {
        'form' : form
    }
    return render(request,'students/contact.html',context)




@login_required
def playlist(request,list_id):
    lists = get_object_or_404(Subject, id=list_id)
    context = {
        'lists' : lists
    }
   
    return render(request,'students/playlist.html',context)



def paid(request):
    return render(request,'paid.html')



@login_required  # Ensures that only logged-in users can access this view
def watch(request, video_id):
    video = get_object_or_404(Videos, id=video_id)
    # Check if the user is authenticated
    if request.user.is_authenticated:
        pdf_url = request.build_absolute_uri(video.subject.pdf)
    else:
        pdf_url = None  # Don't pass the PDF URL if the user isn't authenticated


    
    try:
        context = {
        'video': video,
        'pdf_url': pdf_url,
        
        }
        return render(request, 'students/watch-video.html', context)

        
    except Videos.DoesNotExist:
        return JsonResponse({'error': 'Video not found'}, status=404)




def pakages(request):
    package = Package.objects.all()
    context = {
        'package':package,
       
    }
    return render(request,'pakages.html',context)

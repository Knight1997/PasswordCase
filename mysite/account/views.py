from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, AddPasswordForm
from .models import Case, Profile, Passwords, Otp_database
from .encryption import encrypt
from .getPasswords import main
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as lgin ,logout as lgout
from .sendOTP import send_otp
import random
import datetime;
from django.utils import timezone
from django.utils.timezone import utc


def getFromId(id):
    objList = Case.objects.all()
    for obj in objList:
        if obj.place.id == id:
            return obj


def is_valid(request):
    u=request['username_input']
    p=request['password_input']
    m=request['number_input']
    if u != "" and p != "" and m != "":
        return True
    return False


def is_valid2(request):
    u = request['username_input']
    p = request['password_input']
    if u != "" and p!= "":
        return True
    return False


def is_valid3(request):
    w=request['website']
    e=request['email']
    p=request['password']
    if w != "" and e != "" and p != "":
        return True
    return False


def isExist(username):
    objList = Case.objects.all()
    for obj in objList:
        if str(obj.username) == str(username):
            return True
    return False


def register(request):
    #print(request.method)
    if request.method=='POST':
        #print(request.POST)
        #form = RegisterForm(request.POST)
        #print(form)
        if is_valid(request.POST):
            #Save input in database
            case = Case()
            case.username = request.POST['username_input']
            if isExist(case.username) or request.POST['username_input']=="mayadmin": #Checking if username is not same as taht of superuser.
                blank_form = RegisterForm()
                message = "Error! Username already exist. Please use some other username."
                flag = 1
                context = {'form': blank_form, 'message': message, 'flag': flag}
                return render(request, 'account/register.html', context)
            case.password = request.POST['password_input']
            x = encrypt(case.password)
            user = User.objects.create_user(case.username)
            user.set_password(x)
            user.save()
            case.password = x
            case.phone_number = request.POST['number_input']
            profile = Profile()
            profile.save()
            case.place = profile
            case.save()
            return redirect(login)
        else:
            blank_form = RegisterForm()
            message = "Error! Please fill all details and then submit."
            flag = 1
            context = {'form': blank_form, 'message': message, 'flag': flag}
            return render(request, 'account/register.html', context)
    else:   #if get method, create a blank form.
        blank_form = RegisterForm()
        message = ""
        flag = 0
        context = {'form': blank_form, 'message': message, 'flag': flag}
        return render(request, 'account/register.html', context)


def login(request):
    lgout(request)
    if request.method=='POST':
        inpusername = request.POST['username_input']
        inppassword = request.POST['password_input']
        x = encrypt(inppassword)
        user = authenticate(request, username=inpusername, password=x)
        if user is None:
            blank_form = LoginForm()
            message = "Error! Wrong username or password."
            flag = 1
            context = {'form': blank_form, 'message': message, 'flag': flag}
            return render(request, 'account/login.html', context)
        else:
            lgin(request, user)
            CaseObjList = Case.objects.all()
            ReqObj = None
            for obj in CaseObjList:
                if obj.username==inpusername and obj.password==x:
                    ReqObj = obj
                    break
            prof = ReqObj.place
            id = prof.id
            return redirect(profile, id=id)
    else:   #if get method, create a blank form.
        blank_form = LoginForm()
        message = ""
        flag = 0
        context = {'form': blank_form, 'message': message, 'flag': flag}
        return render(request, 'account/login.html', context)


def profile(request, id):
    #print(request.user)
    if request.user.is_authenticated: #Checks if any user is logged in or not.
        objList = Case.objects.all()
        myObj = None
        for obj in objList:
            if obj.username == str(request.user):
                myObj = obj
                break
        if int(myObj.place.id) != int(id): #So that user can access it's information at only it's specific url.
            return redirect(login)
        myDict = main(myObj)
        context = {'info': myDict, 'id': id}
        return render(request, 'account/hello.html', context)
    else:
        return redirect(login)


def addPassword(request, id):
    if request.user.is_authenticated: #Check if a user is user is logged in or not.
        objList = Case.objects.all()
        myObj = None
        for obj in objList:
            if obj.username == str(request.user):
                myObj = obj
                break
        if int(myObj.place.id) != int(id): #So that user can access it's information at only it's specific url.
            return redirect(login)
        #print(request)
        if request.method == 'POST':
            if is_valid3(request.POST):
                website = request.POST["website"]
                email = request.POST["email"]
                password = request.POST["password"]
                password = encrypt(password)
                obj = Passwords()
                obj.email = email
                obj.encrypted_password = password
                obj.website = website
                objList = Profile.objects.all()
                reqObj = None
                for obj1 in objList:
                    if int(obj1.id) == int(id):
                        reqObj = obj1
                        break
                obj.belongs_to = reqObj
                obj.save()
                return redirect(profile, id=id)
            else:
                blank_form = AddPasswordForm()
                message = "Error! Please fill all details and then submit."
                flag = 1
                context = {'form': blank_form, 'message': message, 'flag': flag, id: 'id'}
                return render(request, 'account/addPassword.html', context)
        else:
            blank_form = AddPasswordForm()
            message = ""
            flag = 0
            context = {'form': blank_form, 'message': message, 'flag': flag, 'id': id}
            return render(request, 'account/addPassword.html', context)
    else:
        return redirect(login)

#<================== OTP Functionality =========================>
def render_otp_request_page(request):
    return render(request, 'account/otp_request_page.html')

def change_password_view(request,username):
    if request.method == 'POST':
        p1=request.POST['password1']
        p2=request.POST['password2']
        if p1 == p2:
            obj=Case.objects.get(username=username)
            print(obj.password)
            obj.password=encrypt(p1)
            print(obj.password)
            obj.save()
            return redirect('login')
        context={'error': 404}
        return render(request,'account/change_password.html',context)
    else:
        print(username + " &&&")
        context={}
        return render(request,'account/change_password.html',context)
def render_otp_input_page(request,username):
    print(request)
    print(username + "$$$$$$")
    if request.method == 'POST':
        otp_input=request.POST['otp_number']
        # retrive OTP and other row from DB using username
        otp_database=Otp_database.objects.filter(username=username)
        print(otp_database)
        otp_num=otp_database.values('otp_text')[0]['otp_text']
        t_stamp=otp_database.values('timestamp')[0]['timestamp']
        print(otp_num)
        print(t_stamp)
        # if timeGap >  2min delete the OTP from DB and send alert OTP expired
        diff_time=datetime.datetime.utcnow().replace(tzinfo=utc) - t_stamp
        print(diff_time.total_seconds())
        if diff_time.total_seconds() > 120.0 :
            #delete from DB
            otp_database.delete()
            context={"error": 0}
            return render(request, 'account/otp_input_page.html', context)
        #if OTP didnt match , send Failure and delete the OTP
        if otp_input == otp_num:
            otp_database.delete()
            print(otp_input + "==" + otp_num)
            context={"username": username}
            return redirect('change_password', username)
        else:
            otp_database.delete()
            context={"error": 1}
            return render(request, 'account/otp_input_page.html', context)
    else:
        context={"username": username}
        return render(request, 'account/otp_input_page.html', context)

def sendOTP(request):
    details="heelo"
    print(details)
    context={'otp_details':details}
    print(request)
    uname=request.GET['input_username']
    print(uname)
    query=Case.objects.filter(username=uname).values('phone_number')
    if len(query)!=0:
        reg_mobile=query[0]['phone_number']
    else :
        context = {"error": "true"}
        return render(request, 'account/otp_request_page.html', context)
    #generate random number
    num=random.randint(100001,999999)
    print(num)
    print(reg_mobile)
    details = send_otp(reg_mobile, str(num))
    #print(details)
    #save username and OTP and OTP_id and Timestamp in DB
    opt_database=Otp_database()
    opt_database.username=uname
    opt_database.otp_text=num
    opt_database.otp_id='1'
    opt_database.timestamp=datetime.datetime.utcnow().replace(tzinfo=utc)
    opt_database.save()
    return redirect('one_time_password_enter', uname)
    #return render(request, 'account/otp_input_page.html', context) #how to send details data to front end?
    

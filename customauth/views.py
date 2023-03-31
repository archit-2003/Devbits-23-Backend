from django.shortcuts import render ,HttpResponse,redirect
from django.contrib import messages
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
from rest_framework import serializers,generics
from .models import UserAccount,Stocks
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from rest_framework.response import Response
from django.core.validators import RegexValidator
User = get_user_model()


def user_get_me(*, user: UserAccount):
    token,_ = Token.objects.get_or_create(user = user)
    return {
        'id': user.id,
        'fname': user.fname,
        'lname': user.lname,
        'email': user.email,
        'username':user.username,
        'token': token.key,
        'message': "Your registration was successfull!",
    }


def handleSignUp(request):
    # print(User.objects.username)
    context={
        'visibility':"none",
    }
    if request.method=="POST":
        fname = request.data["fname"]
        lname = request.data["lname"]
        username= request.data["username"]
        email = request.data["email"]
        pass1= request.data["pass1"]
        pass2= request.data["pass2"]
        # check for errorneous input
        print(username)
        print(fname)
        if len(username)> 10 :
            print('Hello1')
            messages.error(request, " Your user name must be under 10 characters")
            return redirect('signup')
        if not username.isalnum():
            print('Hello2')
            messages.error(request, " User name should only contain letters and numbers")
            return redirect('signup')
        if (pass1!= pass2):
             print('Hello3')
             messages.error(request, " Passwords do not match")
             return redirect('signup')
        if User.objects.filter(username=username).count()!=0 :
             print('Hello4')
             messages.error(request, "Username already taken")
             return redirect('signup')
        if User.objects.filter(email=email).count()!=0 :
             print('Hello5')
             messages.error(request, "Email already taken")
             return redirect('signup')
        if User.objects.filter(username=username).count()!=0 :
            print('Hello6')
            context['visibility']=""
            messages.success(request, "You have been already registered !!")
            return redirect('login')            
        print("HEllo1")
        user = User.objects.create_user(email,pass1)
        print("HEllo2")
        user.fname=fname
        user.lname=lname
        user.username=username
        if user is not None:
            user.save()
            print("HEllo2")
            print(user.email)
            print(user.username)
            print(user.fname)
            print(user.lname)
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            print("Detect")
            return HttpResponse("User Created")
            # return render(request, 'home.html',context)
        else:
            return render(request, 'signup.html',context)
    return render(request, 'signup.html',context)
    # context={
    #     'visibility':"none",
    # }
    # if request.method=="POST":
    #     #Get the POST parameters
    #     username=request.POST['loginusername']
    #     email=request.POST['email']
    #     fname=request.POST['fname']
    #     lname=request.POST['lname']
    #     pass1=request.POST['loginpassword']
    #     pass2=request.POST['confirmpassword']

    #     # check for errorneous input
    #     if len(username)> 10 :
    #         messages.error(request, " Your user name must be under 10 characters")
    #         return redirect('signup')
    #     if not username.isalnum():
    #         messages.error(request, " User name should only contain letters and numbers")
    #         return redirect('signup')

    #     if (pass1!= pass2):
    #          messages.error(request, " Passwords do not match")
    #          return redirect('signup')  
        
    #     if request.user.is_authenticated:
    #          print("Hello")
    #     # Create the user
    #     myuser = User.objects.create_user(username, email, pass1)
    #     myuser.first_name= fname
    #     myuser.last_name= lname
    #     myuser.save()
        
    #     messages.success(request, " Your AUTH System ID has been successfully created")
    #     return redirect('login')

    # else:
    #     return HttpResponse("404 - Not found") 
    
def handlelogin(request):
    context={
        "visibility":"none",
    }
    # if request.method=="POST":
    print(request.data)
    email= request.data["email"]
    password= request.data["password"]
    
    # print(username)
    # print(password)
    user=authenticate(email= email,password=password)
    # print(user)
    if user is not None:
        # messages.success(request, "Successfully Logged In")
        login(request, user)
        messages.success(request, "Successfully Logged In")
        # return render(request, 'home.html',context)
        return HttpResponse("PAwry")
    
    else:
        messages.error(request, "Invalid credentials! Please try again")
        return HttpResponse("Hello2")
        # return render(request, 'login.html',context)
    # return HttpResponse("Hello1")
    # return render(request, 'login.html',context)
    # if request.method=="POST":
    #     # Get the post parameters
    #     loginusername=request.POST['loginusername']
    #     loginpassword=request.POST['loginpassword']

    #     user=authenticate(username= loginusername, password= loginpassword)
    #     if user is not None:
    #         login(request, user)
    #         messages.success(request, "Successfully Logged In")
    #         return redirect("home")
    #     else:
    #         messages.error(request, "Invalid credentials! Please try again")
    #         return redirect("login")

    # return HttpResponse("404- Not found")


def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('login')  

class InputSerializer(serializers.Serializer):
        
        email = serializers.EmailField()
        fname = serializers.CharField(required=True)
        lname = serializers.CharField(required=True)
        username = serializers.CharField(required=True)
        # usermoney = serializers.CharField(required=True)
        pass1 = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
        pass2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

class LoginSerializer(serializers.Serializer):
        
        email = serializers.EmailField()
        password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )                     
        
class AccountSerializer(serializers.Serializer):
      email=serializers.EmailField()
      fname=serializers.CharField(required=True)
      lname=serializers.CharField(required=True)
      username= serializers.CharField(required=True)
      usermoney=serializers.IntegerField()
    #   pass1 = serializers.CharField(
    #     write_only=True,
    #     required=True,
    #     help_text='Leave empty if no change needed',
    #     style={'input_type': 'password', 'placeholder': 'Password'}
    # )
    #   pass2 = serializers.CharField(
    #     write_only=True,
    #     required=True,
    #     help_text='Leave empty if no change needed',
    #     style={'input_type': 'password', 'placeholder': 'Password'}
    # )
      
class UserInitApi(generics.GenericAPIView):
    serializer_class=InputSerializer
    
    def post(self, request, *args, **kwargs):
        context={
            "visibility":"none",
        }
        response1=response1=handleSignUp(request)
        print(response1)
        return HttpResponse("YO")
        
        return HttpResponse(response1)
        
class AddStock(generics.GenericAPIView):
    serializer_class=AccountSerializer
    
    def post(self,request,*args, **kwargs):
        print(request.data)
        # user=UserAccount.objects.filter(email=request.data["email"])
        # print(user)
        return HttpResponse("YO")
        # user.userstocks.append([])
        
    def delete(self,request,*args, **kwargs):
        user=UserAccount.objects.filter(email=request.data["email"])
        print(user)
        return HttpResponse("YO")
        # user.userstocks.remove([])

class LoginUserApi(generics.GenericAPIView):
    serializer_class=LoginSerializer
    
    def post(self, request, *args, **kwargs):
        # print(request.data["username"])
        response1=handlelogin(request)
        return HttpResponse(response1)
    
class StockSerializer(serializers.Serializer):
    email=serializers.EmailField()
    stockname=serializers.CharField(required=True)
    
class UserStock(generics.GenericAPIView):
    serializer_class=StockSerializer
    
    def post(self,request,*args, **kwargs):
        stock=Stocks.objects.filter(email=request.data["stock_user_email"])
           
             
        
    

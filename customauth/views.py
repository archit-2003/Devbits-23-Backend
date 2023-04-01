from django.shortcuts import render ,HttpResponse,redirect
from django.contrib import messages
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import get_user_model
from rest_framework import serializers,generics,status
from .models import UserAccount,Stock
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
        
        
class StockSerializer(serializers.ModelSerializer):
    stock_name=serializers.CharField()
    stock_originalprice=serializers.IntegerField()
    stock_time=serializers.CharField()
    stock_date=serializers.CharField()
    stock_user_email=serializers.EmailField()
    cnt=serializers.IntegerField(default=0)

    def save(self, **kwargs):
        data = self.validated_data
        stock_name = data["stock_name"]
        stock_originalprice = data["stock_originalprice"]
        stock_time = data["stock_time"]
        stock_date = data["stock_date"]
        stock_user_email = data["stock_user_email"]
        cnt = data["cnt"]
        stock_status=data["stock_status"]
        
        stock = Stock.objects.create(
            stock_name=stock_name,
            stock_originalprice=stock_originalprice,
            stock_time=stock_time,
            stock_date=stock_date,
            stock_user_email=stock_user_email,
            cnt=cnt,      
            stock_status=stock_status,
        )
        return stock
    
    class Meta:
        model = Stock
        fields = [
            "stock_name",
            "stock_originalprice",
            "stock_time",
            "stock_date",
            "stock_user_email",
            "cnt",
            "stock_status",
        ]
        
class AddStock(generics.GenericAPIView):
    serializer_class=StockSerializer
    def get_queryset(self):
        return UserAccount.objects.all()
    def post(self,request,*args, **kwargs):
        user=UserAccount(email=request.data["stock_time"])
        totalamount=int(request.data["cnt"])*int(request.data["stock_originalprice"])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # if totalamount <= user.usermoney:
        serializer.save()
        return HttpResponse("DONE") 
        # else:
        #     return HttpResponse("NOT ENOUGH MONEY")            
        # print(user)
        # user.userStock.append([])
    def get(self,request):
        queryset = Stock.objects.all()
        context=[]
        for event in queryset:
            context.append({
                "stock_name": event.stock_name,
                "stock_originalprice": event.stock_originalprice,
                "stock_time": event.stock_time,
                "stock_date": event.stock_date,
                "stock_user_email":event.stock_user_email,
                "cnt":event.cnt,
                "stock_status":event.stock_status,
            })
        return Response(context, status=status.HTTP_200_OK)
        
class MyUserInfo(generics.ListAPIView):
    serializer_class=AccountSerializer
    def get_queryset(self):
        return UserAccount.objects.all()
    def get(self,request):
        queryset1 = UserAccount.objects.all()
        context=[]
        print(queryset1)
        for event1 in queryset1:
            print(event1)
            for event in UserAccount.objects.filter(email=event1.email):
                print(event.fname)
                context.append({
                    "email": event.email,
                    "fname": event.fname,
                    "lname": event.lname,
                    "username": event.username,
                    "usermoney":event.usermoney,
                })
        print(context)
        return Response(context, status=status.HTTP_200_OK)
class LoginUserApi(generics.GenericAPIView):
    serializer_class=LoginSerializer
    
    def post(self, request, *args, **kwargs):
        # print(request.data["username"])
        response1=handlelogin(request)
        return HttpResponse(response1)
    
class UserStock(generics.GenericAPIView):
    serializer_class=StockSerializer
    
    def post(self,request,*args, **kwargs):
        stock=Stock.objects.filter(email=request.data["stock_user_email"])
           
             
        
    

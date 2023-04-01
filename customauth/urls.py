from customauth import views
from urllib.parse import urldefrag
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from .views import AddStock,UserInitApi,UserStock,LoginUserApi,MyUserInfo,WatchApi


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('login', TemplateView.as_view(template_name='login.html'), name='login'),
    path('signup', TemplateView.as_view(template_name='signup.html'), name='signup'),
    # path('^accounts/', include('django.contrib.auth.urls')),
    path('postlogin', views.handlelogin),
    path('postsignup', views.handleSignUp),
    path('logout', views.handlelogout),
    # path('accounts/profile', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),
    path('', include('social_django.urls', namespace='social')),
    path('addStock/', AddStock.as_view(), name='addStock'),
    path('createuser/', UserInitApi.as_view(), name='createuser'),
    path('StockUser/', UserStock.as_view(), name='StockUser'),
    path('loginuser/', LoginUserApi.as_view(), name='loginuser'),
    path('userInfo/', MyUserInfo.as_view(), name='userInfo'),
    path('watchlist/', WatchApi.as_view(), name='watchlist'),
    
]

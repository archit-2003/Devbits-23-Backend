"""DevbitsProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView

admin.site.site_header = "Devbits-23 Backend Administration"

# urlpatterns = [
#     path("admin/", admin.site.urls),
# ]

schema_view = get_schema_view(
    openapi.Info(
        title="Devbits-23 Site API",
        default_version="v1",
        description="This is the Devbits-23 Site API.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('broadcastMail', TemplateView.as_view(template_name='broadcastMail.html'), name='broadcastMail'),
    path("auth/", include("customauth.urls")),
    path('accounts/', include('allauth.urls')),
    # 'django.contrib.sites',
    path('accounts/profile', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),
    # path('api/', include("udyamHelper.urls")),
    # path(r'^ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    # swagger API pages not visible on production
    urlpatterns += [
        path(
            "",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "auth/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

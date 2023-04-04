"""framespik URL Configuration

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
import debug_toolbar
from users.views import UserViewSet
from django.conf import settings
from django.conf.urls.static import static
from event.views import eventwebpage,albumimagewebpage,getEventInvitation,imageSelection
from organization.views import organizationWebPage,getOrganizationEcard
from users.views import phone_login,verify,logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api/', include('api.urls')),
    path('auth/',include('djoser.urls.jwt')),
    path('auth/users/', UserViewSet.as_view({'post': 'create'}), name='user-list'),
    path('auth/users/<int:id>/', UserViewSet.as_view({'get': 'retrieve' }), name='user-detail'),
    path('auth/users/me/', UserViewSet.as_view({'get': 'me'}), name='me'),
    path('auth/',include('djoser.urls')),
    path('memories/<uniquecode>',eventwebpage),
    path('memories/<uniquecode>/a/<int:pk>',albumimagewebpage),
    path('event/invite/<uniquecode>',getEventInvitation),
    path('organization/<uniquecode>',organizationWebPage),
    path('organization/ecard/<uniquecode>',getOrganizationEcard),
    path('imageselection/<int:event_id>/<int:album_id>',imageSelection),
    path('login/', phone_login, name='login'),
    path('verify/', verify, name='verify'),
    path('logout/', logout_view, name='logout'),

    ]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
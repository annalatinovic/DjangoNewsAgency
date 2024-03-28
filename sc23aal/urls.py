"""
URL configuration for sc23aal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from newsagency.views import Login, LogOut, PostStory, GetStory, DeleteStory, List

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', Login),
    path('api/logout/', LogOut),
    path('api/stories', GetStory),
    path('api/stories/', PostStory),
    path('api/directory/', List),
    path('api/stories/<int:key>', DeleteStory)
]

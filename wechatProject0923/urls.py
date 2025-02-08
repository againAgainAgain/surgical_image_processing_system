"""
URL configuration for wechatProject0923 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
# 导入app下的视图
from app import views
from app.views import UserView, LoginView

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 访问 网址/index，就会执行views.index()这个函数
    path('', views.index),
    path('login/', views.login, name='login'),
    path('api/user/', UserView.as_view()),
    path('tologin/', LoginView.as_view(), name='tologin'),
    path('upload/',views.upload, name='upload'),
    path('restore/',views.restore, name='restore'),
    path('captcha/', include('captcha.urls')),  # 包含 captcha 的 URL 配置
]

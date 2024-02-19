"""calculator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

import calculator.views.calculate
import calculator.views.main
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/calculate/', calculator.views.calculate.calculate, name='calculate'),
    path('', calculator.views.main.calculate, name='main/calculate'),
    path('together-todo', calculator.views.main.toto, name='main/toto'),
    path('test', calculator.views.main.test, name='main/test'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

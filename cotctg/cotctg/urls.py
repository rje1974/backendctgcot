"""cotctg URL Configuration0

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from backend.views import GoogleLogin
from rest_framework import routers
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from backend.viewsets import CTGViewSet, LocalidadViewSet, EntidadViewSet,\
    CosechaViewSet, EspecieViewSet, EstablecimientoViewSet, OperacionViewSet,\
    COTViewSet, CredencialViewSet


router = routers.DefaultRouter()
router.register('ctg', CTGViewSet, base_name='ctg')
router.register('cot', COTViewSet, base_name='cot')
router.register('localidades', LocalidadViewSet, base_name='localidades')
router.register('entidades', EntidadViewSet, base_name='entidades')
router.register('cosechas', CosechaViewSet, base_name='cosechas')
router.register('especies', EspecieViewSet, base_name='especies')
router.register('establecimientos', EstablecimientoViewSet, base_name='establecimientos')
router.register('operaciones', OperacionViewSet, base_name='operaciones')
router.register('credenciales', CredencialViewSet, base_name='credenciales')


urlpatterns = [
    url(r'^rest/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/google/$', GoogleLogin.as_view(), name='google_login'),
]
#urlpatterns += staticfiles_urlpatterns()
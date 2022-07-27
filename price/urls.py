from django.conf.urls import include, url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'home', views.home,name='home'),
    # url(r'search', views.search,name='search'),
]



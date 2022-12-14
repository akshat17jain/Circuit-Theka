from django.urls import path 
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
#Django Admin
path('', HomePageView, name='HomePageView'), 

#Local Apps
path('result/', ResultView, name='ResultView'),
path('about-project/', AboutProjectPageView.as_view(), name='AboutProjectPageView'), 
path('developers/', DevelopersPageView.as_view(), name='DevelopersPageView'), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
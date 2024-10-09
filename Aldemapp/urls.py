from django.urls import path,re_path
from . import views
from django.views.static import serve
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from .sitemap import YourModelSitemap


sitemaps = {
    'services': YourModelSitemap,
}


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$',serve,{'document_root':settings.STATIC_ROOT}),
    path('', views.home ,name='index'),
    path('exper', views.exper ,name='exper'),
    path('register', views.register_view, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('student', views.home_student ,name='student'),
    path('profile', views.profile ,name='profile'),
    path('contact', views.contact ,name='contact'),
    path('change_password/',views.change_password, name='change_password'),
    path('playlists/<int:list_id>/', views.playlist ,name='playlist'),
    path('watch/<int:video_id>', views.watch ,name='watch_video'),
    path('paid', views.paid ,name='paid'),
    path('pakages', views.pakages ,name='pakages'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),







    
]

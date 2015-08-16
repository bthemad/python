from django.conf.urls import include, url
from django.contrib import admin

from views import HomePageView, SignUpView, LoginView, logout_view


urlpatterns = [
    url(r'^talks/', include('talks.urls', namespace='talks')),

    url(r'^accounts/register/$', SignUpView.as_view(), name='signup'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', logout_view, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePageView.as_view(), name='home'),
]

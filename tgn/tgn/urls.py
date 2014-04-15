from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tgn.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^accounts/', include('django_facebook.auth_urls')),
    url(r'^$', 'tgn.views.test'),
    url(r'^profile/', 'tgn.views.profile'),                   
    url(r'^otherProfile/', 'tgn.views.otherProfile'),               
    url(r'^otherNonprofit/', 'tgn.views.otherNonprofit'),
    url(r'^myNonprofit/', 'tgn.views.myNonprofit'),
    url(r'fbtest/', 'tgn.views.fbtest'),
    url(r'^tgn/api/loginWithFacebook', 'tgn.api.loginWithFacebook'),
    url(r'^tgn/api/updateProfile', 'tgn.api.updateProfile'),
    url(r'^tgn/api/createNonprofit', 'tgn.api.createNonprofit')
)

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
    url(r'^$', 'tgn.views.index'),
    url(r'^partials/login', 'tgn.views.login'),
    url(r'^partials/myProfile', 'tgn.views.myProfile'),
    url(r'^partials/otherProfile', 'tgn.views.otherProfile'),
    url(r'^partials/otherNonprofit', 'tgn.views.otherNonprofit'),
    url(r'^partials/myNonprofit', 'tgn.views.myNonprofit'),
    url(r'^tgn/api/loginWithFacebook', 'tgn.api.loginWithFacebook'),
    url(r'^tgn/api/updateProfile', 'tgn.api.updateProfile'),
    url(r'^tgn/api/createNonprofit', 'tgn.api.createNonprofit'),
    url(r'^tgn/api/updateNonprofit', 'tgn.api.updateNonprofit'),
    url(r'^tgn/api/viewOtherProfile', 'tgn.api.viewOtherProfile'),
    url(r'^tgn/api/viewJob', 'tgn.api.viewJob'),
    url(r'^tgn/api/viewNonprofit', 'tgn.api.viewNonprofit'),
    url(r'^tgn/api/getPostedJobs', 'tgn.api.getPostedJobs'),
    url(r'^tgn/api/getNonprofits', 'tgn.api.getNonprofits'),
    url(r'^tgn/api/getOtherUsers', 'tgn.api.getOtherUsers'),
    url(r'^tgn/api/applyToJob/', 'tgn.api.applyToJob'),
    url(r'^tgn/api/acceptApplicant', 'tgn.api.acceptApplicant'),
    url(r'^tgn/api/requestAffiliation', 'tgn.api.requestAffiliation')


)

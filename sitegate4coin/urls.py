from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'sitegate4coin.views.home', name='home'),
    url(r'^$', RedirectView.as_view(url='/about/')),
    # url(r'^sitegate4coin/', include('sitegate4coin.foo.urls')),
    url(r'^hdwallet/', include('hdwallet.urls')),
    url(r'^about/', include('about.urls')),
    url(r'^accounts/', include('sgaccount.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

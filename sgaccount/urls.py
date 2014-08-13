from django.conf.urls.defaults import *
from django.views.generic import TemplateView
from views import *

urlpatterns = patterns("",
    url(r"^login/$", login, name="login"),
    url(r"^register/$", register, name="register"),
    url(r'^entrance/$', entrance, name='entrance'),
    url(r"^logout/$", logout_view, name="logout"),

)

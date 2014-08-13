# Create your views here.

from django.shortcuts import render

# Import a flow class to use.
from sitegate.signin_flows.classic import ClassicSignin
from sitegate.decorators import signin_view

# And use that class for sign in.
@signin_view(flow=ClassicSignin)
def login(request):
    return render(request, 'login.html', {'title': 'Sign in'})


# Import a flow class to use.
from sitegate.signup_flows.classic import ClassicSignup
from sitegate.decorators import signup_view

# And use that class for registration.
@signup_view(flow=ClassicSignup)
def register(request):
    return render(request, 'register.html', {'title': 'Sign up'})


from sitegate.decorators import sitegate_view

@sitegate_view  # This also prevents logged in users from accessing our sign in/sign up page.
def entrance(request):
    return render(request, 'entrance.html', {'title': 'Sign in & Sign up'})

# logout
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('about'))



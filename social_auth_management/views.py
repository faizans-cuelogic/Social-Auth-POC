from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import render
from social.apps.django_app.default.models import UserSocialAuth
from django.views.generic import RedirectView
from django.contrib.auth.views import logout as auth_logout


class LoginView(TemplateView):

    template_name = 'login.html'


class HomePageView(TemplateView):

    template_name = 'home.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(HomePageView, self).dispatch(*args, **kwargs)

    def get(self, request):
        if request.user.is_authenticated:
            user_detail = UserSocialAuth.objects.get(user=request.user)
            request.session['access_token_secret'] = user_detail.extra_data['access_token']['oauth_token_secret']
            request.session['access_token'] = user_detail.extra_data['access_token']["oauth_token"]
        return render(request, 'home.html')


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        try:
            del request.session['access_token_secret']
            del request.session['access_token']
        except KeyError:
            pass
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:
    def process_request(self, request):
        assert hasattr(request, 'user') 
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            print path
            if not any(m.match(path) for m in EXEMPT_URLS):
		redirect_path = settings.LOGIN_URL + "?ref=" + request.path
                return HttpResponseRedirect(redirect_path)
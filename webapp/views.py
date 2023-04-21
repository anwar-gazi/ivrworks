from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views import View
from django.shortcuts import render, resolve_url, reverse
from django.conf import settings

# import traceback

from webapp.forms import AuthForm


# TODO NEED FIX
class CallWorksLoginView(LoginView):
    form_class = AuthForm
    redirect_authenticated_user = settings.REDIRECT_AUTHENTICATED_USER

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            print("user is authenticated")
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            # print(f'pre-dispatch auth user is {self.request.user}')
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        print(f'dispatch user is {self.request.user}')
        # print(self.request.session.session_key)
        # traceback.print_stack()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        print(f'auth_login user is {self.request.user.email}')
        # traceback.print_stack()
        # print(self.request.session.session_key)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_context_data(self, **kwargs):
        print(f'context request user is {self.request.user}')
        # traceback.print_stack()
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context


class UserProfileView(View):
    template_name = "default/webapp/userprofile.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"msg": ''})


class CustomizedAdminLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            pass
        redirect_to = request.GET.get('next', '/')
        if redirect_to:
            pass

        defaults = {
            'extra_context': {},
            'template_name': 'admin/login.html',
        }
        return LoginView.as_view(**defaults)(request)

    def post(self, request):
        from django.contrib.admin.sites import AdminSite
        adminsite = AdminSite(name='admin')
        return adminsite.login(request, {})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


class DashboardView(View):
    template_name = "default/webapp/dashboard.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"msg": ''})

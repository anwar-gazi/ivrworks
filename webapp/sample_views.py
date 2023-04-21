from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from django import forms


class SampleForm(forms.Form):
    pass


class SampleView(View):
    form_class = SampleForm
    template_name = "sample.html"
    message = "Asslamualaikom"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"msg": self.message})


@method_decorator(login_required, name="dispatch")
class SampleView2(View):
    pass


@method_decorator([login_required], name="dispatch")
class SampleView3(View):
    pass


class SampleView4(LoginRequiredMixin, View):
    pass


@login_required
def index(request):
    return redirect('dashboard')


@login_required
def dashboard(request):
    data = {}
    return render(request, 'default/webapp/dashboard.html', data)

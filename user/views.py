from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from .forms import LoginForm
from .models import User


# Create your views here.
class LoginView(FormView):
    """login view"""

    form_class = LoginForm
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(
                'user:profile',
                kwargs={'pk': self.request.user.pk}
            ))
        return super(LoginView, self).get(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'user:profile',
            kwargs={'pk': self.request.user.pk}
        )

    def form_invalid(self, form):
        for key, value in form.errors.items():
            for msg in value:
                messages.error(self.request, f"{key}: {msg}")
        return super(LoginView, self).form_invalid(form)

    def form_valid(self, form):
        """ process user login"""
        user = authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password'])

        if user is not None:
            if user.is_active:
                login(self.request, user)
                self.request.session.set_expiry(1209600)
                return HttpResponseRedirect(self.get_success_url())
            else:
                messages.error(self.request, 'Please activate your account.')
        else:
            messages.error(self.request, 'Please check your credentials')

        return HttpResponseRedirect(reverse_lazy('login'))


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user_sessions'] = self.object.user_sessions.all().order_by('-start')
        return context

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import DetailView

from .models import UserSession, TimeFrame
from .tasks import take_screenshots


def TakeScreenshotView(request):
    """
    Runs the 'take screenshot' task from celery
    """
    take_screenshots.delay()
    session = request.user.user_sessions.filter(current=True).first()
    return HttpResponseRedirect(
        reverse_lazy(
            'timetracker:session_details',
            kwargs={'pk': session.id}
        )
    )


def NewTimeFrameView(request):
    """
    Creates a new time frame
    """
    session = request.user.user_sessions.filter(current=True).first()
    TimeFrame.objects.create(session=session, current=True)
    take_screenshots.delay()
    return HttpResponseRedirect(
        reverse_lazy(
            'timetracker:session_details',
            kwargs={'pk': session.id}
        )
    )


def NewSessionView(request):
    """
    Creates a new session and timeframe
    """
    user = request.user

    update_data = {
        'current': False,
        'end': timezone.now()
    }
    UserSession.objects.filter(
        user__id=user.id,
        current=True
    ).update(**update_data)

    session = UserSession.objects.create(user=user, current=True)
    TimeFrame.objects.create(session=session, current=True)
    take_screenshots.delay()

    return HttpResponseRedirect(
        reverse_lazy(
            'timetracker:session_details',
            kwargs={'pk': session.id}
        )
    )


class SessionDetailsView(LoginRequiredMixin, DetailView):
    model = UserSession
    template_name = 'session_details.html'

    def get_context_data(self, **kwargs):
        context = super(SessionDetailsView, self).get_context_data(**kwargs)
        context['sessions_time_frames'] = self.object.sessions_time_frames.all().order_by('-start')
        return context

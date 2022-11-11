from __future__ import unicode_literals

import os

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

optional = {
    'blank': True,
    'null': True
}


class UserSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        to_field='email',
        related_name='user_sessions'
    )
    start = models.DateTimeField(_('session start time'), auto_now_add=True)
    end = models.DateTimeField('session end time', **optional)
    current = models.BooleanField(default=False)

    def __str__(self):
        if self.end:
            return f"{self.user.email}: {self.start} - {self.end}"
        return f"{self.user.email}: {self.start}"

    def get_current_time_frame(self):
        return TimeFrame.objects.filter(
            session__id=self.id,
            current=True
        ).first()


class TimeFrame(models.Model):
    session = models.ForeignKey(
        UserSession,
        on_delete=models.CASCADE,
        related_name='sessions_time_frames'
    )
    start = models.DateTimeField(_('start time'), auto_now_add=True)
    end = models.DateTimeField('end time', **optional)
    current = models.BooleanField(default=False)

    def __str__(self):
        if self.end:
            return f"{self.session.user.email}: {self.start} - {self.end}"
        return f"{self.session.user.email}: {self.start}"

    def save(self, *args, **kwargs):
        if not self.pk:
            current_tf = self.session.get_current_time_frame()
            if current_tf:
                current_tf.current = False
                current_tf.end = timezone.now()
                current_tf.save()
        return super(TimeFrame, self).save(*args, **kwargs)


class Screenshot(models.Model):
    time_frame = models.ForeignKey(
        TimeFrame,
        on_delete=models.CASCADE,
        related_name='time_frame_screenshots'
    )
    photo = models.ImageField(upload_to="screenshots", **optional)
    date_created = models.DateTimeField(_('date created'), auto_now_add=True)

    def __str__(self):
        return os.path.basename(self.photo.name)

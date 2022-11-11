import io
import os
import pyautogui
import time

from celery import shared_task

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

from .models import UserSession, Screenshot


def screenshot(session):
    """
    This will take a screenshot of the current screen and save it into a
    'Screenshot' instance.
    """
    try:
        current_time_frame = session.get_current_time_frame()
        if current_time_frame:
            file_name = (
                f"{session.id}-{current_time_frame.id}-"
                f"{timezone.now().strftime('%Y_%m_%d-%H_%M_%S')}.png"
            )
            media_dir = os.path.join(settings.MEDIA_ROOT, f"screenshots")
            file_path = f"{media_dir}/{file_name}"
            pil_image = pyautogui.screenshot()  # take a screenshot
            img_io = io.BytesIO()
            pil_image.save(img_io, format='png')  # create image file
            image_file = InMemoryUploadedFile(
                img_io,
                None,
                file_path,
                'image/jpeg',
                img_io.tell,
                None
            )

            # Create the Screenshot instance
            Screenshot.objects.create(
                time_frame=current_time_frame,
                photo=image_file
            )
    except Exception:
        return False
    return True


@shared_task
def take_screenshots():
    """
    This searches for all 'current' sessions and calls the 'screenshot'
    function to initiate the screenshot process.

    It is currently limited to a maximum of 5 screenshots for
    testing purposes only.
    """
    sessions = UserSession.objects.filter(current=True)

    counter = 0
    for s in sessions:
        for i in range(5):
            time.sleep(5)
            screenshot(s)
            counter += 1

    # Message will appear on the celery server
    return f'Task took {counter} screenshots in total.'

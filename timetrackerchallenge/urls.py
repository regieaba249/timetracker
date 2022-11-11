from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from user import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('timetracker/', include(('timetracker.urls', 'timetracker'), namespace='timetracker')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

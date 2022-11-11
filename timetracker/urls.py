from django.urls import path

from . import views

urlpatterns = [
    path('new_session', views.NewSessionView, name='new_session'),
    path('new_time_frame', views.NewTimeFrameView, name='new_time_frame'),
    path('take_screenshot', views.TakeScreenshotView, name='take_screenshot'),
    path('<int:pk>/', views.SessionDetailsView.as_view(), name='session_details'),
]

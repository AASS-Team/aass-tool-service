from django.urls import path

from . import views

urlpatterns = [
    path("", views.ToolsList.as_view()),
    path("<uuid:id>", views.ToolDetail.as_view()),
    path("bulk", views.BulkToolsList.as_view()),
]

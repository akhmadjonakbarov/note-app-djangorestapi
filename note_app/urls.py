from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListNoteView.as_view(), name="all-notes"),
    path('add', views.AddNoteView.as_view(), name="add-note"),
    path('update/<int:id>', views.UpdateNoteView.as_view(), name="update-note"),
    path('delete/<int:id>', views.DeleteNoteView.as_view(), name="delete-note")
]

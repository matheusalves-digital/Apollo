from django.urls import path
from .views import TriageCreateView, TriageListView, TriageDetailView, TriageUpdateView

urlpatterns = [
    path('create_triage/', TriageCreateView.as_view(), name='triage-create'),
    path('list_triage/', TriageListView.as_view(), name='triage-list'),
    path('<str:pk>/', TriageDetailView.as_view(), name='triage-detail'),
    path('<str:pk>/update/', TriageUpdateView.as_view(), name='triage-update'),
]

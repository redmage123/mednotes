from django.urls import include, path

urlpatterns = [
    path('admin/', include('admin.urls')),
    path('client/', include('client_connectivity_service.urls')),
    path('question_detection/', include('question_detection.urls')),
    path('question_comparison/', include('question_comparison.urls')),
]


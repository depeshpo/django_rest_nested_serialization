from django.urls import include, path
from rest_framework.routers import DefaultRouter

from question import views

router = DefaultRouter()
router.register('question', views.QuestionViewSet, base_name='question')

urlpatterns = [
    path('api/', include(router.urls))
]

"""
URL configuration for Algonova_Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from feedbacks.views import FeedbackViewSet, generate_feedback_pdf
from groups.views import GroupViewSet
from lessons.views import LessonViewSet
from students.views import StudentViewSet
from utils.token import MyTokenObtainPairView, exchange_token

router = routers.DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'feedbacks', FeedbackViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/exchange-token/', exchange_token, name='token_exchange'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('feedback/download-all/', generate_feedback_pdf, name='feedback_download'),
    path('feedback/download/<str:task_id>/', generate_feedback_pdf, name='feedback_group_download'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
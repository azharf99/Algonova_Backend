from django.shortcuts import render
from rest_framework import viewsets
from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from utils.whatsapp import create_schedule
# Create your views here.

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    pagination_class = PageNumberPagination
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
    ]

    def perform_create(self, serializer):
        feedback = serializer.save()
        data = {
            'phone': '6281218xxxxxx',
            'date': '2022-05-20',
            'time': '13:20:00',
            'timezone': 'Asia/Jakarta',
            'message': 'hello',
            'isGroup': 'true',
        }
        create_schedule(data)


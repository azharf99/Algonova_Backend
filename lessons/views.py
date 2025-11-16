from django.shortcuts import render
from rest_framework import viewsets
from lessons.models import Lesson
from lessons.serializers import LessonSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = PageNumberPagination
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
    ]
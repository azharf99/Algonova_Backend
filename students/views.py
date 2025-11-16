from django.shortcuts import render
from rest_framework import viewsets
from students.models import Student
from students.serializers import StudentSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = PageNumberPagination
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
    ]

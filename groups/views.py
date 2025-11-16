from django.shortcuts import render
from rest_framework import viewsets
from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
# Create your views here.

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = PageNumberPagination
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
    ]


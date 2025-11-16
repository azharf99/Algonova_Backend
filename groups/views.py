from django.shortcuts import render
from rest_framework import viewsets
from groups.models import Group
from groups.serializers import GroupSerializer
from utils.pagination import StandardResultsSetPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
# Create your views here.

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
    ]


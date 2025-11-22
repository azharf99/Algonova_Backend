import csv
from datetime import timedelta
import io
import json
from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, status
from groups.models import Group
from lessons.models import Lesson
from lessons.serializers import LessonSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from utils.pagination import StandardResultsSetPagination
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
# Create your views here.

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
    ]


    @action(detail=False, methods=['post'], url_path='import', url_name='Import Lessons from CSV')
    def import_csv(self, request, *args, **kwargs):
        lessons_data = request.data.get('file')

        # If data is sent as a JSON string in FormData, parse it.
        if isinstance(lessons_data, str):
            try:
                lessons_data = json.loads(lessons_data)
            except json.JSONDecodeError:
                return Response({"detail": "Invalid JSON format in 'file' field."}, status=status.HTTP_400_BAD_REQUEST)
        # If data is sent as raw JSON, request.data will already be a list.
        elif isinstance(request.data, list):
            lessons_data = request.data

        if not isinstance(lessons_data, list):
            return Response({"detail": "Invalid data format. Expected a list of lessons objects."}, status=status.HTTP_400_BAD_REQUEST)
        
        created_count = 0
        updated_count = 0
        errors = []
        
        try:
            with transaction.atomic():
                for row in lessons_data:
                    id = row.get('id')
                    group_id = row.get('group_id')
                    if not id or not group_id:
                        errors.append({"row": row, "error": "Missing 'id' or 'group_id' field."})
                        continue  # Skip rows without an ID
                    group_ids = map(int, group_id.split(", "))
                    groups_qs = Group.objects.prefetch_related('students').filter(id__in=group_ids)

                    for group in groups_qs:
                        shift_days = int(row.get('number'))-1
                        lesson, created = Lesson.objects.update_or_create(
                            id=id,
                            defaults={
                                'title': row.get('title'),
                                'category': row.get('category'),
                                'module': row.get('module'),
                                'level': row.get('level'),
                                'number': row.get('number'),
                                'group': group,
                                'description': row.get('description'),
                                'meeting_link': group.meeting_link,
                                'date_start': group.first_lesson_date + timedelta(days=7*shift_days) if group.first_lesson_date else row.get('date_start'),
                                'time_start': group.first_lesson_time,
                                'is_active': True if row.get('is_active', 'True').lower() == 'true' else False,
                            }
                        )

                        if created:
                            created_count += 1
                        else:
                            updated_count += 1

        except Exception as e:
            return Response({"detail": f"An error occurred during import: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "detail": "Import process finished.",
            "created": created_count,
            "updated": updated_count,
            "errors": errors
        }, status=status.HTTP_200_OK)
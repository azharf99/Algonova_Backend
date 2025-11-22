import csv
import io
import json
from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, status
from groups.models import Group
from groups.serializers import GroupSerializer
from students.models import Student
from utils.pagination import StandardResultsSetPagination
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
# Create your views here.

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
    ]

    @action(detail=False, methods=['post'], url_path='import', url_name='Import Groups from CSV')
    def import_csv(self, request, *args, **kwargs):
        groups_data = request.data.get('file')

        # If data is sent as a JSON string in FormData, parse it.
        if isinstance(groups_data, str):
            try:
                groups_data = json.loads(groups_data)
            except json.JSONDecodeError:
                return Response({"detail": "Invalid JSON format in 'file' field."}, status=status.HTTP_400_BAD_REQUEST)
        # If data is sent as raw JSON, request.data will already be a list.
        elif isinstance(request.data, list):
            groups_data = request.data

        if not isinstance(groups_data, list):
            return Response({"detail": "Invalid data format. Expected a list of group objects."}, status=status.HTTP_400_BAD_REQUEST)
        
        created_count = 0
        updated_count = 0
        errors = []
        
        try:
            with transaction.atomic():
                for row in groups_data:
                    id = row.get('id')
                    if not id:
                        errors.append({"row": row, "error": "Missing 'id' field."})
                        continue  # Skip rows without an ID
                    
                    group, created = Group.objects.update_or_create(
                        id=id,
                        defaults={
                            'name': row.get('group_name'),
                            'description': row.get('description'),
                            'type': row.get('type'),
                            'group_phone': row.get('group_phone'),
                            'meeting_link': row.get('meeting_link'),
                            'recordings_link': row.get('recordings_link'),
                            'first_lesson_date': row.get('first_lesson_date'),
                            'first_lesson_time': row.get('first_lesson_time'),
                            'is_active': True if row.get('is_active', 'True').lower() == 'true' else False,
                        }
                    )

                    # Handle Many-to-Many for teachers
                    students_ids = row.get('students', '')
                    if students_ids:
                        students_ids = [int(id.strip()) for id in students_ids.split(', ') if id.strip().isdigit()]
                        students = Student.objects.filter(id__in=students_ids)
                        group.students.set(students)

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

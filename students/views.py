import csv
import io
import json
from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, status
from students.models import Student
from students.serializers import StudentSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from utils.pagination import StandardResultsSetPagination
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
# Create your views here.

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
    ]

    @action(detail=False, methods=['post'], url_path='import', url_name='Import Students from CSV')
    def import_csv(self, request, *args, **kwargs):
        students_data = request.data.get('file')

        # If data is sent as a JSON string in FormData, parse it.
        if isinstance(students_data, str):
            try:
                students_data = json.loads(students_data)
            except json.JSONDecodeError:
                return Response({"detail": "Invalid JSON format in 'file' field."}, status=status.HTTP_400_BAD_REQUEST)
        # If data is sent as raw JSON, request.data will already be a list.
        elif isinstance(request.data, list):
            students_data = request.data

        if not isinstance(students_data, list):
            return Response({"detail": "Invalid data format. Expected a list of student objects."}, status=status.HTTP_400_BAD_REQUEST)
        
        created_count = 0
        updated_count = 0
        errors = []
        
        try:
            with transaction.atomic():
                for row in students_data:
                    id = row.get('id')
                    if not id:
                        errors.append({"row": row, "error": "Missing 'id' field."})
                        continue  # Skip rows without an ID
                    
                    student, created = Student.objects.update_or_create(
                        id=id,
                        defaults={
                            'fullname': row.get('fullname'),
                            'surname': row.get('surname'),
                            'username': row.get('username'),
                            'password': row.get('password'),
                            'phone_number': row.get('phone_number'),
                            'parent_name': row.get('parent_name'),
                            'parent_contact': row.get('parent_contact'),
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

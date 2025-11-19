import csv
import io
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

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser], url_path='import', url_name='Import Students from CSV')
    def import_csv(self, request, *args, **kwargs):
        file_obj = request.data.get('file')

        if not file_obj:
            return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)
        if not file_obj.name.endswith('.csv'):
            return Response({"detail": "File must be a CSV."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = file_obj.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)

            with transaction.atomic():
                for row in reader:
                    id = row.get('id')
                    if not id:
                        continue # Skip rows without a ID

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

        except Exception as e:
            return Response({"detail": f"An error occurred during import: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Students imported successfully."}, status=status.HTTP_201_CREATED)

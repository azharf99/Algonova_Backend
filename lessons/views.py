import csv
import io
from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets, status
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
            return Response({"detail": "Invalid data format. Expected a list of student objects."}, status=status.HTTP_400_BAD_REQUEST)
        
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
                    
                    lesson, created = Lesson.objects.update_or_create(
                        id=id,
                        defaults={
                            'title': row.get('title'),
                            'category': row.get('category'),
                            'module': row.get('module'),
                            'level': row.get('level'),
                            'number': row.get('number'),
                            'group_id': row.get('group'),
                            'description': row.get('description'),
                            'meeting_link': row.get('meeting_link'),
                            'date_start': row.get('date_start'),
                            'time_start': row.get('time_start'),
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

    @action(detail=False, methods=['post'], parser_classes=[MultiPartParser], url_path='import')
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

                    lesson, created = Lesson.objects.update_or_create(
                        id=id,
                        defaults={
                            'title': row.get('title'),
                            'category': row.get('category'),
                            'module': row.get('module'),
                            'level': row.get('level'),
                            'number': row.get('number'),
                            'group_id': row.get('group'),
                            'description': row.get('description'),
                            'date_start': row.get('date_start'),
                            'time_start': row.get('time_start'),
                            'is_active': True if row.get('is_active', 'True').lower() == 'true' else False,
                        }
                    )

        except Exception as e:
            return Response({"detail": f"An error occurred during import: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Students imported successfully."}, status=status.HTTP_201_CREATED)
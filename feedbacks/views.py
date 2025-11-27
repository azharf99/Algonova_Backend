from datetime import datetime, timedelta
import os
from pathlib import Path
import random
from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from lessons.models import Lesson
from students.models import Student
from utils.feedback_seeder import feedback_seeder
from utils.level import get_course_level
from utils.pagination import StandardResultsSetPagination
from django.views import View
from django.template.loader import render_to_string
from django.http import  JsonResponse
from weasyprint import HTML, CSS
from utils.topic import get_competency, get_result, get_topic
from utils.tutor_feedback import get_feedback, get_tutor_feedback
from utils.whatsapp import create_schedule, upload_files_to_wablas
from dotenv import load_dotenv
load_dotenv()
from django.http import JsonResponse
# Create your views here.

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
    ]
    filterset_fields = ['student', 'number', 'group_name']

    def update(self, request, *args, **kwargs):
        data = request.data
        if settings.DEBUG:
            async_pdf_generator(data['student'], data['course'], data['number'])
        return super().update(request, *args, **kwargs)

    @permission_classes(permissions.IsAuthenticated)
    @action(detail=False, methods=['get'], url_path='generate', url_name='Generate Feedbacks')
    def generate_feedback(self, request, *args, **kwargs):
        group_id = request.GET.get("group_id")
        if group_id:
            is_success = feedback_seeder(Lesson, Feedback, True, group_id)
        else:
            is_success = feedback_seeder(Lesson, Feedback, False, all=False) #disable sementara
        if is_success:
            return Response({
                "detail": "Import process finished.",
                "group_id": group_id
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": "Import failed or disable temporary!.",
                "group_id": group_id
            }, status=status.HTTP_200_OK)





# celery -A Algonova_Backend worker -l info -P eventlet
# celery -A Algonova_Backend purge

if settings.DEBUG:
    from celery.result import AsyncResult
    from utils.generator_pdf import async_pdf_generator
    
    def pdf_status(request, task_id):
        result = AsyncResult(task_id)

        if result.ready():
            return JsonResponse({
                "status": "finished",
                "file": result.get()
            })
        else:
            return JsonResponse({"status": "processing"})


    @api_view(['GET'])
    @permission_classes([permissions.IsAuthenticated])
    def generate_feedback_pdf(request):
        student_id = request.GET.get('student_id')
        course = request.GET.get('course')
        number = request.GET.get('number')
        response = async_pdf_generator(student_id, course, number)
        return JsonResponse(response, safe=False)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def send_feedback_pdf(request):
    feedback_id = request.GET.get('feedback_id')
    if feedback_id:
        queryset = Feedback.objects.select_related('student').filter(id=feedback_id, is_sent=False)
    else:
        queryset = Feedback.objects.select_related('student').filter(is_sent=False)
    data_list = []
    for feedback in queryset:
        response_file = upload_files_to_wablas(feedback.group_name, feedback.student.fullname, feedback.course, feedback.number)
        current_time = timedelta(hours=queryset.lesson_time.hour, minutes=queryset.lesson_time.minute, seconds=queryset.lesson_time.second)
        data = {
            'category': 'document',
            'phone': feedback.student.parent_contact,
            'scheduled_at': f"{feedback.lesson_date} {current_time+timedelta(hours=2, seconds=random.randint(1, 59))}",
            'url': response_file['data']['messages']['url'],
            'text': feedback.tutor_feedback,
        }
        data_list.append(data)
    response = create_schedule(data_list)

    return JsonResponse(response)




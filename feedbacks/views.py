from datetime import datetime, timedelta
import os
from pathlib import Path
from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from lessons.models import Lesson
from utils.fedback_seeder import feedback_seeder
from utils.level import get_course_level
from utils.pagination import StandardResultsSetPagination
from django.views import View
from django.template.loader import render_to_string
from django.http import  JsonResponse
from weasyprint import HTML, CSS
from utils.topic import get_competency, get_result, get_topic
from utils.tutor_feedback import get_feedback, get_tutor_feedback
from utils.whatsapp import create_schedule
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


# celery -A Algonova_Backend worker -l info -P eventlet
# celery -A Algonova_Backend purge

if settings.DEBUG:
    from celery.result import AsyncResult
    from .tasks import generate_pdf_async


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
        number = request.GET.get('number')
        if number:
            number = map(int, number.split(","))
        response = []
        if student_id and number:
            queryset = Feedback.objects.select_related('student').filter(is_sent=False, student_id=student_id, number__in=number)
        elif student_id:
            queryset = Feedback.objects.select_related('student').filter(is_sent=False, student_id=student_id)
        else:
            queryset = Feedback.objects.select_related('student').filter(is_sent=False)
        for feedback in queryset:
            task = generate_pdf_async.delay({
                "student_name": feedback.student.fullname,
                "student_month_course": feedback.number,
                "student_class": feedback.course,
                "student_level": feedback.level,
                "student_project_link": feedback.project_link,
                "student_referal_link": 'https://algonova.id/invite?utm_source=refferal&utm_medium=employee&utm_campaign=social_network&utm_content=hidin466" target="_blank',
                "student_module_link": "https://drive.google.com/drive/u/0/folders/1lErW_RKjHOkAgqCr9yymELg3yUZzvBEb",
                "module_topic": feedback.topic,
                "module_result": feedback.result,
                "skill_result": feedback.competency,
                "teacher_feedback": get_feedback(feedback.student.fullname, int(feedback.attendance_score), int(feedback.activity_score), int(feedback.task_score)),
                },
                "index.html",
                f"{feedback.student.groups.first().name}/Rapor {feedback.student.fullname} Bulan ke-{feedback.number}.pdf"
            )
            response.append({
                "task_id": task.id,
                "status": "processing"
            })

        return JsonResponse(response, safe=False)



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def send_feedback_pdf(request):
    student_id = request.GET.get('student_id')
    if student_id:
        queryset = Feedback.objects.select_related('student').filter(is_sent=False, student_id=student_id)
    else:
        queryset = Feedback.objects.select_related('student').filter(is_sent=False)
    data_list = []
    for feedback in queryset:
        group_phone = feedback.student.groups.first().group_phone
        current_time = timedelta(hours=queryset.lesson_time.hour, minutes=queryset.lesson_time.minute, seconds=queryset.lesson_time.second)

        if group_phone is not None:
            data = {
                'type': 'document',
                'phone': student_phone,
                'scheduled_at': f"{feedback.lesson_date} {current_time+timedelta(hours=2)}",
                'text': feedback.tutor_feedback,
                'url' : ''
            }
            data_list.append(data)
            continue

        student_phone = feedback.student.phone_number
        if student_phone is not None:
            data = {
                'type': 'text',
                'phone': student_phone,
                'scheduled_at': f"{feedback.lesson_date} {current_time+timedelta(hours=2)}",
                'text': feedback.tutor_feedback,
            }
            data_list.append(data)
        data = {
            'type': 'text',
            'phone': feedback.student.parent_contact,
            'scheduled_at': f"{feedback.lesson_date} {current_time+timedelta(hours=2)}",
            'text': feedback.tutor_feedback,
        }
        data_list.append(data)
        response = create_schedule(data_list)

    return JsonResponse(response)




import os
from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from utils.pagination import StandardResultsSetPagination
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from weasyprint import HTML, CSS
from utils.whatsapp import create_schedule
from dotenv import load_dotenv
load_dotenv()
from .tasks import generate_pdf_async
from django.http import JsonResponse
from celery.result import AsyncResult
# Create your views here.

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    pagination_class = StandardResultsSetPagination
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
    ]

    # def perform_create(self, serializer):
    #     feedback = serializer.save()
    #     phone_numbers = []
    #     for student in feedback.group.students.all():
    #             phone_numbers.append(student.parent_contact)

    #     data = {
    #         'phone': '6281218xxxxxx',
    #         'date': '2022-05-20',
    #         'time': '13:20:00',
    #         'timezone': 'Asia/Jakarta',
    #         'message': 'hello',
    #         'isGroup': 'true',
    #     }
    #     create_schedule(data)

    # celery -A Algonova_Backend worker -l info -P eventlet


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def generate_feedback_pdf(request):
    task = generate_pdf_async.delay(
        {
            "student_name": "Azhar",
            "student_month_course": "Azhar",
            "student_class": "Azhar",
            "student_level": "Azhar",
            "student_project_link": "Azhar",
            "student_referal_link": 'https://algonova.id/invite?utm_source=refferal&utm_medium=employee&utm_campaign=social_network&utm_content=hidin466" target="_blank',
            "student_module_link": "https://drive.google.com/drive/u/0/folders/1lErW_RKjHOkAgqCr9yymELg3yUZzvBEb",
            "module_topic": "Azhar",
            "module_result": "Azhar",
            "skill_result": "Azhar",
            "teacher_feedback": ["Azhar", "Azhar", "Azhar", "Azhar"],
        }, 
        "index.html",
    )

    return JsonResponse({
        "task_id": task.id,
        "status": "processing"
    })




def pdf_status(request, task_id):
    result = AsyncResult(task_id)

    if result.ready():
        return JsonResponse({
            "status": "finished",
            "file": result.get()
        })
    else:
        return JsonResponse({"status": "processing"})

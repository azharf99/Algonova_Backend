from datetime import datetime
import os
from pathlib import Path
from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from lessons.models import Lesson
from utils.pagination import StandardResultsSetPagination
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from weasyprint import HTML, CSS
from utils.topic import get_competency, get_result, get_topic
from utils.tutor_feedback import get_tutor_feedback
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

    def list(self, request, *args, **kwargs):
        lessons = Lesson.objects.prefetch_related('group__students', 'students_attended').select_related('group').filter(is_active=True)
        for lesson in lessons:
            # Create monthly feedback
            if lesson.number % 4 == 0:
                for student in lesson.group.students.all():
                    feedback, is_created = Feedback.objects.select_related('group').prefetch_related('group__students').update_or_create(
                        group = lesson.group,
                        number = lesson.number // 4,
                        defaults={
                            'topic': get_topic(lesson.module, lesson.number // 4),
                            'result': get_result(lesson.module, lesson.number // 4),
                            'competency': get_competency(lesson.module, lesson.number // 4),
                            'tutor_feedback': get_tutor_feedback(student.fullname),
                            'lesson_date': lesson.date_start,
                            'lesson_time': lesson.time_start,
                            'is_sent': False,
                        }

                    )

        return super().list(request, *args, **kwargs)

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

    base_url = Path(settings.BASE_DIR, "static").resolve().as_uri()
    # Render HTML
    html_string = render_to_string("index.html",
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
        }
    )

    pdf = HTML(string=html_string, base_url=base_url).write_pdf()

    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    save_path = Path(settings.MEDIA_ROOT) / filename

    with open(save_path, "wb") as f:
        f.write(pdf)

    return settings.MEDIA_URL + filename

    return JsonResponse({
        "task_id": task.id,
        "status": "processing"
    })



# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def generate_feedback_pdf(request):
#     task = generate_pdf_async.delay(
        # {
        #     "student_name": "Azhar",
        #     "student_month_course": "Azhar",
        #     "student_class": "Azhar",
        #     "student_level": "Azhar",
        #     "student_project_link": "Azhar",
        #     "student_referal_link": 'https://algonova.id/invite?utm_source=refferal&utm_medium=employee&utm_campaign=social_network&utm_content=hidin466" target="_blank',
        #     "student_module_link": "https://drive.google.com/drive/u/0/folders/1lErW_RKjHOkAgqCr9yymELg3yUZzvBEb",
        #     "module_topic": "Azhar",
        #     "module_result": "Azhar",
        #     "skill_result": "Azhar",
        #     "teacher_feedback": ["Azhar", "Azhar", "Azhar", "Azhar"],
        # }, 
#         "index.html",
#     )

#     return JsonResponse({
#         "task_id": task.id,
#         "status": "processing"
#     })




# def pdf_status(request, task_id):
#     result = AsyncResult(task_id)

#     if result.ready():
#         return JsonResponse({
#             "status": "finished",
#             "file": result.get()
#         })
#     else:
#         return JsonResponse({"status": "processing"})

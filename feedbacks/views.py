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
from utils.level import get_course_level
from utils.pagination import StandardResultsSetPagination
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from weasyprint import HTML, CSS
from utils.topic import get_competency, get_result, get_topic
from utils.tutor_feedback import get_feedback, get_tutor_feedback
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

    # def list(self, request, *args, **kwargs):
    #     lessons = Lesson.objects.prefetch_related('group__students', 'students_attended').select_related('group').filter(is_active=True)
    #     updated_count = 0
    #     created_count = 0
    #     counter = 1
    #     for lesson in lessons:
    #         # Create monthly feedback
    #         if lesson.level == "M1L1":
    #             counter = 1
    #         if counter % 4 == 0:
    #             for student in lesson.group.students.all():
    #                 feedback, is_created = Feedback.objects.select_related('student').update_or_create(
    #                     student = student,
    #                     number = counter // 4,
    #                     defaults={
    #                         'topic': get_topic(lesson.module, counter // 4),
    #                         'result': get_result(lesson.module, counter // 4),
    #                         'competency': get_competency(lesson.module, counter // 4),
    #                         'tutor_feedback': get_tutor_feedback(student.fullname),
    #                         'lesson_date': lesson.date_start,
    #                         'lesson_time': lesson.time_start,
    #                         'is_sent': False,
    #                         'level' : get_course_level(lesson.module),
    #                         'course' : lesson.module,
    #                         'project_link' : lesson.group.recordings_link,
    #                     }
    #                 )
                    
    #                 if is_created:
    #                     created_count += 1
    #                 else:
    #                     updated_count += 1
    #         counter += 1

    #     print(f"Created feedbacks: {created_count}, Updated feedbacks: {updated_count}")

    #     return super().list(request, *args, **kwargs)

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
    # celery -A Algonova_Backend purge


# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def generate_feedback_pdf(request):

#     base_url = Path(settings.BASE_DIR, "static").resolve().as_uri()
#     # Render HTML
#     queryset = Feedback.objects.select_related('student').filter(is_sent=False)
#     for feedback in queryset:
#         html_string = render_to_string("index.html",
#             {
#                 "student_name": feedback.student.fullname,
#                 "student_month_course": feedback.number,
#                 "student_class": feedback.course,
#                 "student_level": feedback.level,
#                 "student_project_link": feedback.project_link,
#                 "student_referal_link": 'https://algonova.id/invite?utm_source=refferal&utm_medium=employee&utm_campaign=social_network&utm_content=hidin466" target="_blank',
#                 "student_module_link": "https://drive.google.com/drive/u/0/folders/1lErW_RKjHOkAgqCr9yymELg3yUZzvBEb",
#                 "module_topic": feedback.topic,
#                 "module_result": feedback.result,
#                 "skill_result": feedback.competency,
#                 "teacher_feedback": get_feedback(feedback.student.fullname, feedback.attendance_score, feedback.activity_score, feedback.task_score),
#             }
#         )

#         pdf = HTML(string=html_string, base_url=base_url).write_pdf()

#         filename = f"{feedback.student.groups.first().name}/Rapor {feedback.student.fullname} Bulan ke-{feedback.number}.pdf"
#         save_path = Path(settings.MEDIA_ROOT) / filename

#         with open(save_path, "wb") as f:
#             f.write(pdf)

#     return JsonResponse({
#         "Pdf has been generated!"
#     })



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def generate_feedback_pdf(request):
    student_id = request.GET.get('student_id')
    if student_id:
        queryset = Feedback.objects.select_related('student').filter(is_sent=False, student_id=student_id)
    else:
        queryset = Feedback.objects.select_related('student').filter(is_sent=False)
    response = []
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
        if group_phone is not None:
            data = {
                'phone': student_phone,
                'date': feedback.lesson_date,
                'time': feedback.lesson_time,
                'timezone': 'Asia/Jakarta',
                'message': feedback.tutor_feedback,
                'isGroup': 'true',
            }
            data_list.append(data)
            continue

        student_phone = feedback.student.phone_number
        if student_phone is not None:
            data = {
                'phone': student_phone,
                'date': feedback.lesson_date,
                'time': feedback.lesson_time,
                'timezone': 'Asia/Jakarta',
                'message': feedback.tutor_feedback,
                'isGroup': 'false',
            }
            data_list.append(data)
        data = {
            'phone': '6281218xxxxxx',
            'phone': feedback.student.parent_contact,
            'date': feedback.lesson_date,
            'time': feedback.lesson_time,
            'timezone': 'Asia/Jakarta',
            'message': feedback.tutor_feedback,
            'isGroup': 'false',
        }
        response = create_schedule(data_list)

    return JsonResponse(response)




def pdf_status(request, task_id):
    result = AsyncResult(task_id)

    if result.ready():
        return JsonResponse({
            "status": "finished",
            "file": result.get()
        })
    else:
        return JsonResponse({"status": "processing"})

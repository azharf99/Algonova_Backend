from django.conf import settings
from feedbacks.models import Feedback
from rest_framework.response import Response
from rest_framework import status
from utils.tutor_feedback import get_feedback


if settings.DEBUG:
    from feedbacks.tasks import generate_pdf_async

    def async_pdf_generator(student_id=None, feedback_course=None, feedback_number=None, all=False):
        if student_id and feedback_course and feedback_number:
            queryset = Feedback.objects.filter(student_id=student_id, course=feedback_course, number=feedback_number, is_sent=False)
        elif student_id and feedback_course:
            queryset = Feedback.objects.filter(student_id=student_id, course=feedback_course, is_sent=False)
        elif student_id and feedback_number:
            queryset = Feedback.objects.filter(student_id=student_id, number=feedback_number, is_sent=False)
        elif student_id and all:
            queryset = Feedback.objects.filter(student_id=student_id)
        elif student_id:
            queryset = Feedback.objects.filter(student_id=student_id, is_sent=False)
        else:
            queryset = Feedback.objects.filter(is_sent=False)
        
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
        return response
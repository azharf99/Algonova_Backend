from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from utils.pagination import StandardResultsSetPagination
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from weasyprint import HTML
from utils.whatsapp import create_schedule
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


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def generate_feedback_pdf(request, group_id=None):
    html = render_to_string('index.html', {
        'data': "Aku",
    })
    pdf = HTML(string=html).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Feedbacks.pdf"'
    return response
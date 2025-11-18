from rest_framework import viewsets
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        for feedback in queryset:
            print(feedback.group.lessons.filter(title__icontains='Python'))
            for student in feedback.group.students.all():
                print(student.phone_number)

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



class FeedbackDownloadPDFView(LoginRequiredMixin, PermissionRequiredMixin, View):
    raise_exception = False
    permission_required = 'feedbacks.view_feedback'
    queryset = Feedback.objects.select_related("group").all()

    def get(self, request, *args, **kwargs):
        html = render_to_string('index.html', {
            'data': "Aku",
        })
        pdf = HTML(string=html).write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Feedbacks.pdf"'
        return response
import os
from pathlib import Path
from django.conf import settings
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from datetime import datetime

from django.conf import settings

if settings.DEBUG:
    from celery import shared_task
    @shared_task
    def generate_pdf_async(context_data, template_name, filename):

        base_url = Path(settings.BASE_DIR, "static").resolve().as_uri()
        # Render HTML
        html_string = render_to_string(template_name, {
            **context_data,
            "base_url": base_url
        })

        pdf = HTML(string=html_string, base_url=base_url).write_pdf()

        save_path = Path(settings.MEDIA_ROOT) / filename

        with open(save_path, "wb") as f:
            f.write(pdf)

        return settings.MEDIA_URL + filename

from django.conf import settings

def student_data(request):
    return {
        "student_name": settings.STUDENT_NAME,
        "student_section": settings.STUDENT_SECTION,
        "student_year": settings.STUDENT_YEAR,
    }

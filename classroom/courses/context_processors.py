from .models import Course

def sidebar_courses(request):
    if request.user.is_authenticated:
        return {
            'courses': Course.objects.all()
        }
    return {}
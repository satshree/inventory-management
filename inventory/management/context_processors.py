from .models import Company

def company(request):
    try:
        return {'company':Company.objects.first()}
    except:
        return {'company':None}
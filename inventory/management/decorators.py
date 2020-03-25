from django.http import JsonResponse

def permission_required(perm):
    def check(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            print(request, args, kwargs)
            if request.user.has_perm(perm):
                return func(*args, **kwargs)
            else:
                return JsonResponse({
                    'status':False,
                    'icon':'warning',
                    'msg':'You are not authorized to do so!'
                })
        return wrapper
    return check

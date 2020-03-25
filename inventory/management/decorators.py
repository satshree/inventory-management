from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.handlers.wsgi import WSGIRequest

def permission_required(*perm):
    def check(func):
        def wrapper(*args, **kwargs):
            for arguments in args:
                if isinstance(arguments, WSGIRequest):
                    request = arguments
                    break

            json_resp = False
            for permission in perm:
                if request.user.has_perm(permission):
                    allow = True
                else:
                    allow = False
                
                if "delete" in permission:
                    json_resp = True

            if allow:
                return func(*args, **kwargs)
            else:
                if json_resp:
                    return JsonResponse({
                        'icon':'warning',
                        'msg':'You are not authorized to do so!'
                    })
                else:
                    messages.error(request, "You are not authorized to do so!")
                    return HttpResponseRedirect(request.get_full_path())
        return wrapper
    return check

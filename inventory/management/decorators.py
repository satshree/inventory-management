from django.http import HttpResponse

def permission_required(perm):
    def check(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            if request.user.has_perm(perm):
                return func(*args, **kwargs)
            else:
                return HttpResponse('<script>alert("You are not authorized to do so!");</script>')
        return wrapper
    return check

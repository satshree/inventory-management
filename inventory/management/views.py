from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.transaction import atomic
from django.db.models import Count
from django.db import IntegrityError
from datetime import datetime, date
from management.models import Brand, Device
from management.utilities import log
from management.extra_views import search
from management.decorators import permission_required

### CLASSES ###
class LogInView(TemplateView):
    """ Sign In Page. """
    template_name = 'registration/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        authentication = authenticate(
            username = username, 
            password = password
        )

        if authentication is not None:
            login(request, authentication)
            return redirect(reverse("management:overview"))
        else:
            messages.error(request, 'Authentication Failed!')
        
        return self.get(request, *args, **kwargs)

class HomePageView(LoginRequiredMixin, TemplateView):
    """ Home Page. """
    login_url = ''
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Overview' 
        context["total"] = Device.objects.all().count()
        context["current"] = 'Overview'

        brands_label = []
        brands_data = []
        brands = Device.objects.all().values('brand').annotate(total=Count('brand')).order_by('brand')
        
        for each in brands:
            brands_label.append(each['brand'])
            brands_data.append(each['total'])
         
        context['brands'] = brands
        context['brands_label'] = brands_label
        context['brands_data'] = brands_data
    
        location_label = []
        location_data = []
        location = Device.objects.all().values('location').annotate(total=Count('location')).order_by('location')
        
        for each in location:
            location_label.append(each['location'])
            location_data.append(each['total'])
         
        context['location'] = location
        context['location_label'] = location_label
        context['location_data'] = location_data

        working = 0
        not_working = 0
        status_data = []
        status = Device.objects.all().values('status').annotate(total=Count('status')).order_by('status')
        
        for each in status:
            status_data.append(each['total'])
            if each['status']:
                working = each['total']
            else:
                not_working = each['total']
        
        context['working'] = working
        context['not_working'] = not_working
        context['status_data'] = status_data

        return context
    
class DashboardView(LoginRequiredMixin, ListView):
    """ Dashboard View. """
    login_url = ''
    template_name = "dashboard.html"
    context_object_name = "devices"
    model = Device
    paginate_by = 5

    def get_queryset(self):
        if "q" in self.request.GET:
            return search(self.request)
        else:
            return self.model.objects.all()

    @permission_required("management.add_brand")
    def post(self, request, *args, **kwargs):
        brand_name = request.POST.get('brand')

        if not "serial" in request.POST:
            try:
                Brand.objects.create(
                    brand=brand_name.upper()
                )
            except IntegrityError:
                messages.error(request, '"{}" Already Exists!'.format(brand_name))
            except Exception as e:
                log("Exception caught on 'DashboardView' on adding Brand.", str(e))
                messages.error(request, "Something went wrong.")
            else:
                messages.success(request, '"{}" Added!'.format(brand_name))
        else:
            serial_number = request.POST.get('serial')
            status = request.POST.get('status')
            location = request.POST.get('location')
            model = request.POST.get('model')
            manufactured_date = request.POST.get('manufacture')
            remarks = request.POST.get('remarks')

            try:
                with atomic():
                    brand = Brand.objects.get(brand = brand_name)

                    device_model, created = Device.objects.get_or_create(
                        brand = brand,
                        serial_number = serial_number,
                        model = model,
                        status = bool(status),
                        location = location.upper(),
                        manufactured_date = manufactured_date
                    )

                    device_model.remarks = remarks
                    device_model.save()
            except Brand.DoesNotExist:
                messages.error(request, '"{}" Brand Does Not Exist!'.format(brand_name))
            except Exception as e:
                log("Exception caught on 'DashboardView' on adding Device.", str(e))
                messages.error(request, 'Something went wrong.')
            else:
                if created:
                    messages.success(request, 'Device "{}" added.'.format(model))
                else:
                    messages.error(request, '{} {} ({}) Already Exists!'.format(brand_name, model, serial_number))

        return redirect(reverse("management:dashboard"))
        # return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brands"] = Brand.objects.all()
        context["current"] = 'Inventory Management Dashboard'
        context["title"] = 'Dashboard'
        return context

class ProfileView(LoginRequiredMixin, TemplateView):
    """ Profile View. """
    login_url = ''
    template_name = "profile.html"

    def post(self, request, *args, **kwargs):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        # Validate password
        if password:
            if password != repassword:
                messages.error(request, 'Passwords Did Not Match.')
                return self.get(request, *args, **kwargs)

        # Validate email
        if not ('@' in email and '.com' in email):
            messages.error(request, 'Please Enter Email Address In Correct Format')
            return self.get(request, *args, **kwargs)

        try:
            with atomic():
                user_model = User.objects.get(username=username)

                user_model.first_name = firstname
                user_model.last_name = lastname
                user_model.email = email
                user_model.username = username

                if password:
                    user_model.set_password(password)
            
                user_model.save()
        except Exception as e:
            log("Exception caught on 'Profile View'.", str(e))
            messages.error(request, 'Something went wrong')
        else:
            messages.success(request, 'Your profile details has been updated.')

        return redirect(reverse("management:profile"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current"] = 'Profile'
        context["title"] = 'Profile'
        return context


class RegisterView(TemplateView):
    """ Register Page. """
    template_name = "registration/newuser.html"

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate email
        if not ('@' in email and '.com' in email):
            return JsonResponse({
                'status':False,
                'msg':'Please Enter Email Address In Correct Format'
            })

        try:
            with atomic():
                user_model = User.objects.create_user(
                    first_name = first_name, 
                    last_name = last_name,
                    username = username,
                    email = email,
                    password = password,
                    is_active=False
                )

                user_model.save()

                return JsonResponse({
                    'status': True,
                    'title':'User {} Registered.'.format(username),
                    'msg':'You can sign in once super user approves your profile.'
                })
        except IntegrityError:
            return JsonResponse({
                'status':False,
                'msg':'"{}" already exists!'.format(username)
            })
        except Exception as e:
            log("Exception caught on 'RegisterView'.", str(e))
            return JsonResponse({
                'status':False,
                'msg':'Something went wrong.'
            })

class DeviceEditView(LoginRequiredMixin, TemplateView):
    """ Edit page. """ 
    template_name = 'edit.html'

    def post(self, request, *args, **kwargs):
        pk=request.POST.get("pk")
        brand_name = request.POST.get('brand')
        serial_number = request.POST.get('serial_number')
        status = request.POST.get('status')
        location = request.POST.get('location')
        model = request.POST.get('model')
        manufactured_date = request.POST.get('manufacture')
        remarks = request.POST.get('remarks')

        # Validate empty strings
        if not brand_name:
            messages.error(request, 'Brand not chosen.')
            return self.get(request, *args, **kwargs)
        
        if not status:
            messages.error(request, 'Status not chosen.')
            return self.get(request, *args, **kwargs)

        try:
            with atomic():
                brand = Brand.objects.get(brand=brand_name)
                device = Device.objects.get(pk=int(pk))

                device.brand = brand
                device.serial_number = serial_number
                device.status = bool(status)
                device.location = location.upper()
                device.model = model
                device.manufactured_date = manufactured_date
                device.remarks = remarks

                device.save()
        except Exception as e:
            log("Exception caught on 'DeviceEditView'.", str(e))
            messages.error(request, "Something went wrong.")
        else:
            messages.success(request, 'Device Information Updated.')
            return redirect("management:edit-device", pk=device.pk)
        
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = Device.objects.get(pk=kwargs['pk'])
        context['title'] = 'Edit Device'
        context['current'] = context['title']
        context['brands'] = Brand.objects.all()
        context["device"] = device
        context["date"] = datetime.strftime(device.manufactured_date, '%Y-%m-%d')
        return context
    

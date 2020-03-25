from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.db.transaction import atomic
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from management.models import Brand, Device
from management.decorators import permission_required
from management.utilities import log

### FUNCTIONS ###
def log_user_out(request):
    """ End User Session """
    logout(request)
    return HttpResponseRedirect('/')

def delete_user(request):
    """ Delete the given user. """ 

    # Retrieve username
    username = request.POST.get('username')

    # Get user
    delete_user = User.objects.get(username=username)

    # Delete user
    delete_user.delete()

    # Render sign in page
    return JsonResponse({
        'msg':'Your Profile Has Been Deleted.'
    })

@permission_required('management.add_brand')
def create_brand(request, brand_name):
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

@permission_required('management.delete_brand')
def delete_brand(request):
    """ Remove the given brand. """

    # Retrieve values
    brand_name = request.POST.get('brand')

    try:
        # Delete the given brand
        Brand.objects.get(brand=brand_name).delete()

        return JsonResponse({
            'icon':'success',
            'msg':'"{}" Deleted!'.format(brand_name)
        })
    except:
        # If the brand does not exist
        return JsonResponse({
            'icon':'error',
            'msg':'"{}" Does Not Exist!'.format(brand_name)
        })

@permission_required("management.add_device")
def add_device(request, brand_name):
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

@permission_required('management.delete_device')
def delete_device(request):
    """ Delete the given device. """

    # Retrieve values
    brand_name = request.POST.get('brand')
    serial_number = request.POST.get('serial_number')   
    model = request.POST.get('model')

    try:
        # Delete the given brand
        Device.objects.get(
            brand = brand_name,
            serial_number = serial_number,
            model = model
        ).delete()

        return JsonResponse({
            'icon':'success',
            'msg':'{} {} Deleted!'.format(brand_name, model)
        })
    except:
        # If the brand does not exist
        return JsonResponse({
            'icon':'error',
            'msg':'{} {} Does Not Exist!'.format(brand_name, model)
        })

def search(request):
    search_request = request.GET.get('q')

    try:
        # If search queries for brand
        brand = Brand.objects.get(brand__icontains=search_request)
        search_result = Device.objects.filter(brand=brand)
    except:
        # If search queries for model
        search_result = Device.objects.filter(model__icontains=search_request)

        if not search_result:
            # If search queries for serial number
            search_result = Device.objects.filter(serial_number__icontains=search_request)
        
        if not search_result:
            # If search queries for location
            search_result = Device.objects.filter(location__icontains=search_request)
        
        if not search_result:
            # If search queries for manufactured date

            # Validate date format
            try:
                manufactured = datetime.strptime(search_request, '%b. %d, %Y')
                search_result = Device.objects.filter(manufactured_date=manufactured)
            except:
                try:
                    manufactured = datetime.strptime(search_request, '%Y-%m-%d')
                    search_result = Device.objects.filter(manufactured_date=manufactured)
                except:
                    try:
                        manufactured = datetime.strptime(search_request, '%B %d, %Y')
                        search_result = Device.objects.filter(manufactured_date=manufactured)
                    except:
                        pass

    return search_result

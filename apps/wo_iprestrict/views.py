from django.shortcuts import render, get_object_or_404, redirect
import json

from service.format_response import api_response

from iprestrict.models import IPRange
from .form import IPRangeForm


def ip_range_list(request):
    ip_ranges = IPRange.objects.filter(ip_group_id=2).values()
    ip_ranges_json = list(ip_ranges)
    return api_response(200, 'success', ip_ranges_json)

def ip_range_detail(request, pk):
    ip_range = IPRange.objects.filter(id=pk).values().first()
    return api_response(200, 'success', ip_range)

def ip_range_create(request):
    if request.method == 'POST':
        payload = json.loads(request.body)  # Parse the JSON payload
        payload['ip_group'] = 2
        form = IPRangeForm(payload)
        if form.is_valid():
            form.save()
            return api_response(200, 'sucess')
    print(form.errors.as_data())
    errors = {field: [str(error) for error in error_list] for field, error_list in form.errors.as_data().items()}

    return api_response(400, 'validation error', errors)

def ip_range_update(request, pk):
    ip_range = get_object_or_404(IPRange, pk=pk)
    payload = json.loads(request.body)  # Parse the JSON payload
    payload['ip_group'] = 2
    form = IPRangeForm(payload, instance=ip_range)
    if form.is_valid():
        form.save()
        return api_response(200, 'sucess')
    else:
        print(form.errors.as_data())
        errors = {field: [str(error) for error in error_list] for field, error_list in form.errors.as_data().items()}
    return api_response(400, 'validation error', errors)

def ip_range_delete(request, pk):
    ip_range = get_object_or_404(IPRange, pk=pk)
    print(ip_range)
    ip_range.delete()
    return api_response(200, 'sucess')

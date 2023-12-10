from django.shortcuts import render, get_object_or_404, redirect
import json, platform, subprocess

from service.format_response import api_response

from iprestrict.models import IPRange, Rule
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
            reload_rules_command()
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
        reload_rules_command()
        return api_response(200, 'sucess')
    else:
        print(form.errors.as_data())
        errors = {field: [str(error) for error in error_list] for field, error_list in form.errors.as_data().items()}
    return api_response(400, 'validation error', errors)

def ip_range_delete(request, pk):
    ip_range = get_object_or_404(IPRange, pk=pk)
    print(ip_range)
    ip_range.delete()
    reload_rules_command()
    return api_response(200, 'sucess')


def reload_rules_command():
    current_os = platform.system()
    print("Current OS:", current_os)

    if current_os == 'Linux':
        command = [
            "bash",
            "-c",
            "source venv/bin/activate && python3 manage.py reload_rules"
        ]
    elif current_os == 'Windows':
        command = "venv\\Scripts\\activate && python manage.py reload_rules"
    else:
        raise NotImplementedError(f"Unsupported operating system: {current_os}")

     # Capture the output
    result = subprocess.run(command, capture_output=True, text=True, shell=False)

    # Access the output
    output = result.stdout
    print('outer cmd is => \n', output)
    
def ip_restrict_turn(request):
    if request.method == 'GET':
        rule = Rule.objects.filter(ip_group_id=1).values().first()
        print(rule)
        return api_response(200, 'success', rule)
    else:
        rule_to_update = Rule.objects.get(ip_group_id=1)
        if rule_to_update.action == "D":
            new_action = "A"
        else:
            new_action = "D"

        # Update the fields
        rule_to_update.action = new_action
        # Save the changes
        rule_to_update.save()
        reload_rules_command()
        return api_response(200, 'sucess')
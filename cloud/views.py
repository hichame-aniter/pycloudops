from django.shortcuts import redirect, render
import boto3
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def list_ec2_instances(request):
    client = boto3.client('ec2', region_name=settings.AWS_REGION)
    instances = client.describe_instances()
    ec2_data = []
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance['Tags']:
                if tag["Key"] == 'Name':
                    instancename = tag["Value"]
            ec2_data.append({                  
                'name': instancename,          
                'id': instance['InstanceId'],
                'state': instance['State']['Name'],
                'type': instance['InstanceType'],
                'region': instance['Placement']['AvailabilityZone'],                
            })
    return render(request, 'ec2_list.html', {'instances': ec2_data})

@login_required
def ec2_action(request):
    if request.method == 'POST':
        instance_id = request.POST.get('instance_id')
        action = request.POST.get('action')

        client = boto3.client('ec2', region_name=settings.AWS_REGION)

        try:
            if action == 'start':
                client.start_instances(InstanceIds=[instance_id])
                messages.success(request, f"Instance {instance_id} is starting.")
            elif action == 'stop':
                client.stop_instances(InstanceIds=[instance_id])
                messages.success(request, f"Instance {instance_id} is stopping.")            
            else:
                messages.error(request, "Invalid action.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

        return redirect('list_ec2')
    
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list_ec2')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from backend.models import Device, Measurement

# Create your views here.
@login_required
def main(request):
    return render(request, 'index.html')

#Device
@login_required
def device_list(request):
    #if super user, show everything, otherwise filter by logged in user.
    if request.user.is_superuser:
        devices = Device.objects.all()
    else:
        devices = Device.objects.filter(user=request.user)
    return render(request, 'crud-device.html', {'devices': devices})

@login_required
def device_create(request):
    if request.method == 'POST':
        Device.objects.create(
            device_id=request.POST['device_id'],
            type=request.POST['type'],
            custom_name=request.POST.get('custom_name') or None,
            user=request.user,
        )
        return redirect('device_list')
    return render(request, 'device-form.html')

@login_required
def device_edit(request, pk):
    if request.user.is_superuser:
        device = get_object_or_404(Device, pk=pk)
    else:
        device = get_object_or_404(Device, pk=pk, user=request.user)
    if request.method == 'POST':
        device.device_id = request.POST['device_id']
        device.device_type = request.POST['device_type']
        device.custom_name = request.POST.get('custom_name') or None
        device.save()
        return redirect('device_list')
    return render(request, 'device-form.html', {'device': device})

@login_required
def device_delete(request, pk):
    if request.user.is_superuser:
        device = get_object_or_404(Device, pk=pk)
    else:
        device = get_object_or_404(Device, pk=pk, user=request.user)
    if request.method == 'POST':
        device.delete()
        return redirect('device_list')
    return render(request, 'device-confirm-delete.html', {'device': device})

#Measurement
@login_required
def measurement_list(request):
    #if super user, show everything, otherwise filter by logged in user.
    if request.user.is_superuser:
        measurements = Measurement.objects.all().select_related('device')
    else:
        measurements = Measurement.objects.filter(device__user=request.user).select_related('device')
    return render(request, 'crud-data.html', {'measurements': measurements})

@login_required
def measurement_create(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            device = get_object_or_404(Device, pk=request.POST['device_id'])
        else:
            device = get_object_or_404(Device, pk=request.POST['device_id'], user=request.user)
        Measurement.objects.create(
            device=device,
            value=request.POST['value'],
            timestamp=request.POST['timestamp'],
        )
        return redirect('measurement_list')
    #if super user, show everything, otherwise filter by logged in user.
    if request.user.is_superuser:
        devices = Device.objects.all()
    else:
        devices = Device.objects.filter(user=request.user)
    return render(request, 'measurement-form.html', {'devices': devices})

@login_required
def measurement_edit(request, pk):
    if request.user.is_superuser:
        measurement = get_object_or_404(Measurement, pk=pk)
    else:
        measurement = get_object_or_404(Measurement, pk=pk, device__user=request.user)
    if request.method == 'POST':
        if request.user.is_superuser:
            measurement.device = get_object_or_404(Device, pk=request.POST['device_id'])
        else:
            measurement.device = get_object_or_404(Device, pk=request.POST['device_id'], user=request.user)
        measurement.value = request.POST['value']
        measurement.timestamp = request.POST['timestamp']
        measurement.save()
        return redirect('measurement_list')
    #if super user, show everything, otherwise filter by logged in user.
    if request.user.is_superuser:
        devices = Device.objects.all()
    else:
        devices = Device.objects.filter(user=request.user)
    return render(request, 'measurement-form.html', {'measurement': measurement, 'devices': devices})

@login_required
def measurement_delete(request, pk):
    if request.user.is_superuser:
        measurement = get_object_or_404(Measurement, pk=pk)
    else:
        measurement = get_object_or_404(Measurement, pk=pk, device__user=request.user)
    if request.method == 'POST':
        measurement.delete()
        return redirect('measurement_list')
    return render(request, 'measurement-confirm-delete.html', {'measurement': measurement})
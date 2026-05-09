from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from apps.accounts.forms import CustomerProfileEditForm
from apps.accounts.models import CustomerProfile, User


@login_required
def role_redirect(request):
    if request.user.role == User.Roles.ADMIN:
        return redirect('dashboard:admin_dashboard')
    if request.user.role == User.Roles.COOK:
        return redirect('dashboard:cook_dashboard')
    return redirect('dashboard:customer_dashboard')


@login_required
def customer_dashboard(request):
    if request.user.role != User.Roles.CUSTOMER:
        raise PermissionDenied
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    return render(request, 'dashboard/customer_dashboard.html', {'profile': profile})


@login_required
def customer_profile_edit(request):
    if request.user.role != User.Roles.CUSTOMER:
        raise PermissionDenied
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CustomerProfileEditForm(request.POST, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard:customer_dashboard')
    else:
        form = CustomerProfileEditForm(instance=profile, user=request.user)
    return render(request, 'dashboard/customer_profile_edit.html', {'form': form})


@login_required
def cook_dashboard(request):
    if request.user.role != User.Roles.COOK:
        raise PermissionDenied
    return render(request, 'dashboard/cook_dashboard.html')


@login_required
def admin_dashboard(request):
    if request.user.role != User.Roles.ADMIN:
        raise PermissionDenied
    return render(request, 'dashboard/admin_dashboard.html')

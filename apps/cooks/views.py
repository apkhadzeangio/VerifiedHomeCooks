from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.accounts.models import CookProfile, CookVerification, User

from .forms import CookApplicationForm


@login_required
def cook_apply_view(request):
    if request.user.role == User.Roles.ADMIN:
        return redirect('dashboard:admin_dashboard')

    if hasattr(request.user, 'cook_profile'):
        return redirect('cooks:cook_application_status')

    if request.method == 'POST':
        form = CookApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            return redirect('cooks:cook_application_status')
    else:
        form = CookApplicationForm()

    return render(request, 'cooks/apply.html', {'form': form})


@login_required
def cook_application_status_view(request):
    cook_profile = getattr(request.user, 'cook_profile', None)
    if not cook_profile:
        return redirect('cooks:cook_apply')

    verification = getattr(cook_profile, 'verification', None)
    status = verification.status if verification else cook_profile.verification_status
    admin_comment = verification.admin_comment if verification else ''

    message_map = {
        CookVerification.Status.PENDING: 'Your application is pending review.',
        CookVerification.Status.APPROVED: 'You are approved as a cook. You can now access your cook dashboard.',
        CookVerification.Status.REJECTED: 'Your application was rejected. Please review admin comments.',
        CookVerification.Status.SUSPENDED: 'Your cook account is suspended. Please contact support.',
    }

    return render(
        request,
        'cooks/application_status.html',
        {
            'status': status,
            'admin_comment': admin_comment,
            'status_message': message_map.get(status, 'Status unavailable.'),
        },
    )

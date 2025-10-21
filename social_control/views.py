from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import SocialAccount, SocialSession
@login_required
def dashboard(request):
    accounts = SocialAccount.objects.filter(user=request.user)
    return render(request, 'social_control/dashboard.html', {'accounts': accounts})

@login_required
def add_account(request):
    if request.method == 'POST':
        platform = request.POST['platform']
        limit = int(request.POST['limit'])
        SocialAccount.objects.create(user=request.user, platform=platform, daily_limit_minutes=limit)
        return redirect('social_dashboard')
    return render(request, 'social_control/add_account.html')

@login_required
def update_usage(request, account_id):
    account = SocialAccount.objects.get(id=account_id, user=request.user)
    if request.method == 'POST':
        minutes = int(request.POST['minutes'])
        account.time_spent_today += minutes
        account.save()

        # Check limit
        if account.is_over_limit():
            send_mail(
                subject=f"⏰ Your {account.platform} limit reached!",
                message=f"Hey {request.user.username}, you've hit your daily {account.platform} limit ({account.daily_limit_minutes} mins). Time to refocus 💪",
                from_email='noreply@selfgrowth.com',
                recipient_list=[request.user.email],
            )
        return redirect('social_dashboard')
    return render(request, 'social_control/update_usage.html', {'account': account})



def start_session(request, account_id):
    account = get_object_or_404(SocialAccount, id=account_id, user=request.user)
    session = SocialSession.objects.create(account=account)
    return JsonResponse({'message': f'Started {account.platform} session', 'session_id': session.id})

def end_session(request, session_id):
    session = get_object_or_404(SocialSession, id=session_id)
    session.end_time = timezone.now()
    session.save()

    # update total time spent today
    duration = session.get_duration_minutes()
    account = session.account
    account.time_spent_today += duration
    account.save()

    # check for limit
    if account.time_spent_today >= account.daily_limit_minutes:
        send_mail(
            f'Your {account.platform} daily limit is reached',
            f'Hey {account.user.username}, you’ve used {account.time_spent_today} minutes on {account.platform}, exceeding your daily limit of {account.daily_limit_minutes} minutes.',
            'filebarag@gmail.com',
            [account.user.email],
            fail_silently=True,
        )

    return JsonResponse({'message': 'Session ended', 'duration_minutes': duration})

from __future__ import absolute_import

from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings

from .models import Invite


# need_three_warning.apply_async([],countdown=5)

"""
@shared_task
def you_need_three_warning(pak):
    picks = pak.get_picks(week is required here)
    if len(picks) < 3:
        # check to see if pak in contest.  Only send this after contest exists

        msg = "We noticed that you removed a 3pak pick, but didn't add a replacement player. "
        msg += "You must have three picks to score points for the week. Please make a replacement pick before Sunday at noon or you will not receive any points this week."

        send_mail('Alert: Make your third 3pak pick', msg, 'no-reply@3pak-testing.com',
                  [pak.user.email, ],
                  fail_silently=False)
"""


@shared_task
def invite_user(invitation_id):
    invite = Invite.objects.get(id=invitation_id)
    subject = "You've been challenged"
    # msg = "{} has challenged you on 3pak. Visit http://app.3pak.com to respond to that challenege.\n".format(
    #         invite.user.username
    # )
    user_company = invite.user.profile.company_name
    context = {
        'user': invite.user.username,
        'site': "{0}?play={1}".format(settings.PAK_SITE_ADDRESS, user_company)
    }
    t = get_template('invite_user.txt')
    txt = t.render(context)

    t2 = get_template('invite_user.html')
    htmltxt = t2.render(context)

    send_mail(subject, txt, 'no-reply@3pak-testing.com',
              [invite.address, ],
              html_message=htmltxt,
              fail_silently=False)

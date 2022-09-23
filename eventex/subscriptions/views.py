from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from eventex.subscriptions.forms import SubscriptionForm
from django.core import mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from eventex.subscriptions.models import Subscription


def subscribe(request):
    if request.method == 'POST':
        return create(request)
    else:
        return new(request)

def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render (request, 'subscriptions/subscription_form.html',
                      {'form': form})
     
    sub = Subscription.objects.create(**form.cleaned_data) 

    _send_mail('Confirmação de Inscrição',
                settings.DEFAULT_FROM_EMAIL,
                sub.email,
                'subscriptions/subscription_email.txt',
                {'sub':sub})  
              

    return HttpResponseRedirect('/inscricao/{}/'.format(sub.pk))
  
def new(request):
    return render(request, 'subscriptions/subscription_form.html', 
                 {'form': SubscriptionForm()})

def detail(request, pk):
    try:
        sub = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    return render(request, 'subscriptions/subscription_detail.html', {'subscription': sub})

def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail


@login_required
def contact(request):
    title = 'Contact Us'
    form = ContactForm(request.POST or None)
    confirm_message = '''Feel free to let us know what you think about SONIC and do well to add 
                        suggestions to make SONIC better. Thank You!!!'''

    if form.is_valid():
        name = form.cleaned_data['name']
        comment = form.cleaned_data['comment']
        subject = "Message from SONIC"
        message = '%s \n %s' %(comment, name)
        emailFrom = form.cleaned_data['email']
        emailTo = [settings.EMAIL_HOST_USER]
        send_mail(subject, message, emailFrom, emailTo, fail_silently=True)
        title = 'Thanks!'
        confirm_message = 'Thanks for the message. We will get right back to you'
        form = None

    context = {'title': title, 'form': form, 'confirm_message': confirm_message}
    return render(request, 'contact/contact.html', context)

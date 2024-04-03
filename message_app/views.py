from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from pretty_html_table import build_table

# Create your views here.
from message_app.models import Document
from message_app.forms import DocumentForm

from message_app.task import send_email_fun
from devtest import settings

import pandas as pd

def send_email(request, message,html_message):
    send_email_fun.delay("Python Assignment - Shubham Birmi", message, settings.EMAIL_HOST_USER, "shubhambirmi@hotmail.com",html_message)
    return HttpResponse("Sent Email Successfully...Check your mail please")

def query_view(request):
    # Handle file upload
    newdoc =None
    # Load documents for the list page
    documents = Document.objects.all()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES['docfile'].name.endswith('.xlsx'):
                newdoc = pd.read_excel(request.FILES['docfile'])
            elif request.FILES['docfile'].name.endswith('.csv'):
                newdoc = pd.read_csv(request.FILES['docfile'])
            # newdoc.save()
            # print(newdoc)
            for col in newdoc.columns:
                if col.lower()=="dpd":
                    # print(newdoc.groupby(['Cust State', 'DPD']).count())
                    # print(newdoc.groupby(['Cust State','DPD'])['ACCNO'].count())
                    # print(newdoc.groupby(['Cust State','DPD'])["ACCNO"].count().reset_index(name="count"))
                    newdoc = newdoc.groupby(['Cust State','DPD'])["ACCNO"].count().reset_index(name="count")
                    # output = build_table(newdoc, 'blue_light')
                    output = newdoc.to_html()
                    send_email(request,message="", html_message=output)
                else:
                    pass
            # Redirect to the document list after POST
            return render(
                request,
                'main.html',
                {'df': newdoc,'documents': documents, 'form': form,"len":len(newdoc.columns)}
            )
    else:
        form = DocumentForm() # A empty, unbound form



    context = {'documents': documents, 'form': form}

    # Render list page with the documents and the form
    return render(
        request,
        'main.html',
        context,
    )

    # return render(request, 'main.html')
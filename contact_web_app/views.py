from django.shortcuts import render
from django.http import HttpResponse
from models import Contact, Provider


def contacts_home(request):
    return render(request, "contact_web_app/index.html")


def add_contact_form(request):
    return render(request, "contact_web_app/add_contact.html")


def add_contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone_no = request.POST['phone_no']
        email = request.POST['email']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        pin_code = request.POST['pin_code']
        try:
            Contact.objects.get(phone_no=phone_no)
        except Contact.DoesNotExist:
            contact = Contact(name=name, phone_no=phone_no, email=email, street=street, city=city, state=state,
                              pin_code=pin_code)
            contact.save()
            message = 'Contact successfully added!'
            return HttpResponse(message)
        else:
            message = 'Contact already exist!'
            return HttpResponse(message)


def modify_contact_form(request):
    name = request.POST['name']
    phone_no = request.POST['phone_no']
    email = request.POST['email']
    street = request.POST['street']
    city = request.POST['city']
    state = request.POST['state']
    pin_code = request.POST['pin_code']
    return render(request, "contact_web_app/modify_contact.html", {'name': name, 'phone_no': phone_no, 'email': email,
                                                                   'street': street, 'city': city, 'state': state,
                                                                   'pin_code': pin_code})


def modify_contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone_no = request.POST['phone_no']
        email = request.POST['email']
        street = request.POST['street']
        city = request.POST['city']
        state = request.POST['state']
        pin_code = request.POST['pin_code']
        try:
            contact = Contact.objects.get(phone_no=phone_no)
            contact.name = name
            contact.email = email
            contact.street = street
            contact.city = city
            contact.state = state
            contact.pin_code = pin_code
            contact.save()
            message = 'Contact successfully modified!'
            return HttpResponse(message)
        except Contact.DoesNotExist:
            message = 'There is no contact with this phone number!'
            return HttpResponse(message)


def delete_contact_form(request):
    return render(request, "contact_web_app/delete_contact.html")


def delete_contact(request):
    if request.method == 'POST':
        phone_no = request.POST['phone_no']
        try:
            contact = Contact.objects.get(phone_no=phone_no)
            contact.delete()
            message = 'Contact deleted successfully!'
            return HttpResponse(message)
        except Contact.DoesNotExist:
            message = 'There is no contact with this phone number!'
            return HttpResponse(message)


def get_contact_form(request):
    message = ''
    return render(request, "contact_web_app/get_contact.html", {'message': message})


def get_contact(request):
    if request.method == 'POST':
        phone_no = request.POST['phone_no']
        try:
            contact = Contact.objects.get(phone_no=phone_no)
            return render(request, "contact_web_app/view_contact.html", {'contact': contact})
        except Contact.DoesNotExist:
            message = 'There is no contact with this phone number!'
            return render(request, "contact_web_app/get_contact.html", {'message': message})


def get_provider_form(request):
    return render(request, "contact_web_app/get_provider.html")


def get_provider(request):
    if request.method == 'POST':
        phone_no = request.POST['phone_no']
        providers = Provider.objects.all()
        for provider in providers:
            if phone_no[0:4] in provider.series_list:
                return HttpResponse(provider.provider_name)
        return HttpResponse('Other')


def get_contacts_by_provider_form(request):
    message = ''
    return render(request, "contact_web_app/get_contacts_by_provider.html", {'message': message})


def get_contacts_by_provider(request):
    if request.method == 'POST':
        provider_name = request.POST['provider']
        provider = Provider.objects.get(provider_name=provider_name)
        li = []
        contacts = Contact.objects.all()
        for contact in contacts:
            if contact.phone_no[0:4] in provider.series_list:
                li.append(contact)
        if li:
            return render(request, "contact_web_app/view_contacts.html", {'contacts': li})
        else:
            message = 'There are no contacts with this provider!'
            return render(request, "contact_web_app/get_contacts_by_provider.html", {'message': message})


def get_contacts_by_field_form(request):
    message = ''
    return render(request, "contact_web_app/get_contacts_by_field.html", {'message': message})


def get_contacts_by_field(request):
    if request.method == 'POST':
        string = request.POST['string']
        field = request.POST['field']
        if field == 'name':
            subset = Contact.objects.filter(name__contains=string)
        elif field == 'phone_no':
            subset = Contact.objects.filter(phone_no__contains=string)
        elif field == 'email':
            subset = Contact.objects.filter(email__contains=string)
        elif field == 'street':
            subset = Contact.objects.filter(street__contains=string)
        elif field == 'city':
            subset = Contact.objects.filter(city__contains=string)
        elif field == 'state':
            subset = Contact.objects.filter(state__contains=string)
        else:
            subset = Contact.objects.filter(pin_code__contains=string)
        if subset:
            return render(request, 'contact_web_app/view_contacts.html', {'contacts': subset})
        else:
            message = 'There are no matching contacts!'
            return render(request, "contact_web_app/get_contacts_by_field.html", {'message': message})

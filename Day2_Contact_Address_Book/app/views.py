from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Contact
from .forms import ContactForm

class ContactListView(ListView):
    model = Contact
    template_name = 'app/contact_list.html'
    context_object_name = 'contacts'

class ContactDetailView(DetailView):
    model = Contact
    template_name = 'app/contact_detail.html'

class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'app/contact_form.html'  # Changed to contact_form.html
    success_url = reverse_lazy('contact_list')

class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'app/contact_form.html'  # Changed to contact_form.html
    success_url = reverse_lazy('contact_list')

class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'app/contact_confirm_delete.html'
    success_url = reverse_lazy('contact_list')

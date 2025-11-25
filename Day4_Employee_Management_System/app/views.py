from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Employee
from .forms import EmployeeForm

class EmployeeListView(ListView):
    model = Employee
    template_name = 'app/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10  # Optional: pagination

class EmployeeDetailView(DetailView):
    model = Employee
    template_name = 'app/employee_detail.html'
    context_object_name = 'employee'

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'app/employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeUpdateView(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'app/employee_form.html'
    success_url = reverse_lazy('employee_list')

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'app/employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

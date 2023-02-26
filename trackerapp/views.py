from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum



def index(request):
    if request.method == 'POST':
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()
    
    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))
    expense_form = ExpenseForm()
    return render(request,'trackerapp/index.html',{'expense_form':expense_form,'expenses':expenses,'total_expenses':total_expenses})


def edit(request,id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    
    if request.method == 'POST':
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid:
            form.save()
            return redirect('index')
  
    return render(request,'trackerapp/edit.html',{'expense_form':expense_form})


class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = reverse_lazy("index")

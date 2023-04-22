import datetime
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
    
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))
    
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expense.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))
    
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = Expense.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))
    
    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    
    categorical_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    
    expense_form = ExpenseForm()
    
    return render(request,'trackerapp/index.html',
                  {'expense_form':expense_form,
                    'expenses':expenses,
                    'total_expenses':total_expenses,
                    'yearly_sum':yearly_sum,
                    'monthly_sum':monthly_sum,
                    'weekly_sum':weekly_sum,
                    'daily_sums':daily_sums,
                    'categorical_sums': categorical_sums
                    })


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

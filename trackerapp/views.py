from django.shortcuts import render
from .forms import ExpenseForm


def index(request):
    if request.method == 'POST':
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()
    expense_form = ExpenseForm()
    return render(request,'trackerapp/index.html',{'expense_form':expense_form})

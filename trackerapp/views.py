from django.shortcuts import render
from .forms import ExpenseForm


def index(request):
    expense_form = ExpenseForm()
    return render(request,'trackerapp/index.html',{'expense_form':expense_form})

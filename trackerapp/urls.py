from django.urls import path
from .views import index,edit,ExpenseDeleteView

urlpatterns = [
    path("",index,name='index'),
    path("edit/<int:id>/",edit,name="edit"),
    path("delete/<int:pk>/",ExpenseDeleteView.as_view(template_name='trackerapp/expense_delete.html'),name='expense_delete'),
]
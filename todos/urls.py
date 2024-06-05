from django.urls import path
from .views import TodoListCreateView, TodoCreateView, RegisterView, LoginView, LogoutView, YearlySummaryView, MonthlySummaryView, WeeklySummaryView, TestAuthView

urlpatterns = [
    path('todolists/', TodoListCreateView.as_view(), name='todolist-create'),
    path('todolists/<int:list_id>/todos/', TodoCreateView.as_view(), name='todo-create'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('summary/yearly/', YearlySummaryView.as_view(), name='yearly-summary'),
    path('summary/monthly/', MonthlySummaryView.as_view(), name='monthly-summary'),
    path('summary/weekly/', WeeklySummaryView.as_view(), name='weekly-summary'),
    path('test-auth/', TestAuthView.as_view(), name='test-auth'),
]

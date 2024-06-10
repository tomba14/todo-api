from django.urls import path
from .views import DefaultView, IsLoggedInView, TodoListMonthlyView, TodoListCreateView, TodoCreateView, RegisterView, LoginView, LogoutView, YearlySummaryView, MonthlySummaryView, WeeklySummaryView, TestAuthView

urlpatterns = [
    path('', DefaultView.as_view(), name='default'),
    path('/isLoggedIn', IsLoggedInView.as_view(), name='is-logged-in'),  # This is the default route, so it should be the first one
    path('/todolists/', TodoListCreateView.as_view(), name='todolist-create'),
    path('/todolists/monthly/', TodoListMonthlyView.as_view(), name='todolist-monthly'),
    path('/todolists/todos/', TodoCreateView.as_view(), name='todo-create'),
    path('/register/', RegisterView.as_view(), name='register'),
    path('/login/', LoginView.as_view(), name='login'),
    path('/logout/', LogoutView.as_view(), name='logout'),
    path('/summary/yearly/', YearlySummaryView.as_view(), name='yearly-summary'),
    path('/summary/monthly/', MonthlySummaryView.as_view(), name='monthly-summary'),
    path('/summary/weekly/', WeeklySummaryView.as_view(), name='weekly-summary'),
    path('test-auth/', TestAuthView.as_view(), name='test-auth'),
]

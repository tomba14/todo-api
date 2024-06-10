from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from .models import TodoList, Todo
from .serializers import TodoListSerializer, TodoSerializer

class DefaultView(APIView):
    def get(self, request):
        return Response({"message": "Todo API"})

class IsLoggedInView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(
                {"message": "OK", "user_id": request.user.id},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "OKerror"},
                status=status.HTTP_403_FORBIDDEN
            )

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(LoginView, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class TodoListCreateView(generics.ListCreateAPIView):
    serializer_class = TodoListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TodoList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        now = timezone.now()
        current_month = now.month
        current_year = now.year

        # Verificar si ya existe una lista de tareas para el usuario en el mes actual
        if TodoList.objects.filter(user=user, created_at__year=current_year, created_at__month=current_month).exists():
            raise serializers.ValidationError("Ya existe una lista de tareas para este mes.")
        
        # Si no existe, se crea una nueva lista de tareas
        serializer.save(user=user)
class TodoListMonthlyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        now = timezone.now()
        current_month = now.month
        current_year = now.year

        # Filtrar las listas de tareas por usuario, año y mes actuales
        todo_lists = TodoList.objects.filter(user=user, created_at__year=current_year, created_at__month=current_month)
        serializer = TodoListSerializer(todo_lists, many=True)
        return Response(serializer.data)
class TodoCreateView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(todo_list__user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        now = timezone.now()
        current_month = now.month
        current_year = now.year

        # Intentar obtener el TodoList del mes actual para el usuario
        todo_list, created = TodoList.objects.get_or_create(
            user=user,
            created_at
            defaults={'user': user}
        )

        # Guardar el nuevo Todo con el todo_list asociado
        serializer.save(todo_list=todo_list)


class TodoUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(todo_list__user=self.request.user)

class TodoDeleteView(generics.DestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(todo_list__user=self.request.user)

class YearlySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = timezone.now().year
        todos = Todo.objects.filter(todo_list__user=request.user, is_completed=True, todo_list__month__year=year)
        count = todos.count()
        return Response({'year': year, 'completed_tasks': count})

class MonthlySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = timezone.now().month
        year = timezone.now().year
        todos = Todo.objects.filter(todo_list__user=request.user, is_completed=True, todo_list__month__year=year, todo_list__month__month=month)
        count = todos.count()
        return Response({'year': year, 'month': month, 'completed_tasks': count})

class WeeklySummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        todos = Todo.objects.filter(todo_list__user=request.user, is_completed=True, todo_list__month__range=[start_of_week, end_of_week])
        count = todos.count()
        return Response({'start_of_week': start_of_week, 'end_of_week': end_of_week, 'completed_tasks': count})
        
class TestAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated"})


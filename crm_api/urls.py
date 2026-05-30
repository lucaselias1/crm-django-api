from django.contrib import admin
from django.urls import path
from clientes.views import ClienteListView, ClienteCreateView, NotaCreateView, NotaListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Tela de Administração do Django
    path('admin/', admin.site.urls),
    
    # --- ROTAS DA API DE CLIENTES ---
    # Rota para Listar Clientes (GET /api/clientes/)
    path('api/clientes/', ClienteListView.as_view(), name='cliente-list'),
    
    # Rota para Criar Cliente (POST /api/clientes/novo/)
    path('api/clientes/novo/', ClienteCreateView.as_view(), name='cliente-create'),
    
    # --- ROTAS DE AUTENTICAÇÃO JWT ---
    # Rota para Gerar o Token (POST /api/token/)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Rota para Renovar o Token (POST /api/token/refresh/)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # --- ROTAS DA API DE NOTAS ---
    # Rota para Criar Nota (POST /api/notas/novo/)
    path('api/notas/novo/', NotaCreateView.as_view(), name='nota-create'),
    path('api/clientes/<int:cliente_id>/notas/', NotaListView.as_view(), name='cliente-nota-list'),
]
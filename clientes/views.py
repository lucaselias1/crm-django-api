from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from .models import Cliente, Nota
from .serializers import ClienteSerializer, ClienteCreateSerializer, NotaSerializer
from .permissions import IsAdminOrVendedorOwner 
from django.db.models import Q

# 1. LISTAR CLIENTES (Com regra de Ownership)
class ClienteListView(generics.ListAPIView):
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated, IsAdminOrVendedorOwner]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nome', 'email', 'telefone']

    def get_queryset(self):
        user = self.request.user
        # Se for admin, vê TODOS os clientes do banco
        if user.is_staff or user.groups.filter(name='administrador').exists():
            return Cliente.objects.all()
        # Se for vendedor, vê APENAS os seus próprios clientes
        return Cliente.objects.filter(usuario_responsavel=user)

# 2. CADASTRAR CLIENTE (Vincula o dono automaticamente)
class ClienteCreateView(generics.CreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminOrVendedorOwner]

    def perform_create(self, serializer):
        # Salva o cliente vinculando o usuário que está enviando o POST
        serializer.save(usuario_responsavel=self.request.user)

# 3. LISTAR NOTAS (Com regra de Ownership)
class NotaListView(generics.ListAPIView):
    serializer_class = NotaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrVendedorOwner]

    def get_queryset(self):
        user = self.request.user
        cliente_id = self.kwargs['cliente_id']
        
        # Se for admin, pode ver as notas de qualquer cliente
        if user.is_staff or user.groups.filter(name='administrador').exists():
            return Nota.objects.filter(cliente_id=cliente_id)
            
        # Se for vendedor, só vê se for o dono daquele cliente específico
        return Nota.objects.filter(cliente_id=cliente_id, cliente__usuario_responsavel=user)

# 4. CRIAR NOTA
class NotaCreateView(generics.CreateAPIView):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrVendedorOwner]
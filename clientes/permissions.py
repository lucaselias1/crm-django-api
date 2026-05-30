from rest_framework import permissions


class IsAdminOrVendedorOwner(permissions.BasePermission):
    """
    Permissão customizada:
    - Admins têm acesso total.
    - Vendedores só acessam se forem os donos do registro.
    """
    def has_permission(self, request, view):
        # Qualquer usuário autenticado pode tentar acessar as listagens/criações
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Se for administrador do sistema, o acesso é totalmente liberado
        if request.user.is_staff or request.user.groups.filter(name='administrador').exists():
            return True
            
        # Se o objeto testado for um Cliente, verifica se o usuário é o responsável
        if hasattr(obj, 'usuario_responsavel'):
            return obj.usuario_responsavel == request.user
            
        # Se o objeto testado for uma Nota, verifica se ele é dono do cliente daquela nota
        if hasattr(obj, 'cliente'):
            return obj.cliente.usuario_responsavel == request.user
            
        return False
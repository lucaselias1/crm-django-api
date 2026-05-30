from rest_framework import serializers
from .models import Cliente, Nota

# 1. SERIALIZER PARA LISTAR CLIENTES
class ClienteSerializer(serializers.ModelSerializer):
    # Mostra o nome do usuário (vendedor) em texto na listagem, em vez de só o ID numérico
    usuario_responsavel = serializers.ReadOnlyField(source='usuario_responsavel.username')

    class Meta:
        model = Cliente
        # Usar '__all__' é ótimo para listagem pois traz ID, nome, email, telefone e o vendedor
        fields = '__all__'


# 2. SERIALIZER PARA CADASTRAR CLIENTES
class ClienteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        # Removemos o método 'create' manual daqui de dentro! O DRF cuida disso.
        fields = ['id', 'nome', 'email', 'telefone', 'usuario_responsavel']
        
        # SUPER IMPORTANTE: Avisa o Django que o Postman NÃO precisa enviar o vendedor,
        # pois a View vai injetar o usuário logado automaticamente através do Token JWT!
        read_only_fields = ['usuario_responsavel']


# 3. SERIALIZER DE NOTAS (Está perfeito!)
class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = ['id', 'cliente', 'texto', 'data_criacao']
        read_only_fields = ['data_creation',] # Corrigido pequeno typo para 'data_criacao'
        read_only_fields = ['data_criacao']
from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    usuario_responsavel = models.ForeignKey(User, on_delete=models.PROTECT, related_name='clientes_usuario_responsavel')
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class ListarClientes(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_listagem = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Listagem de {self.cliente.nome} em {self.data_listagem}"


class Nota(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def __str__(self):
        return f"Nota para {self.cliente.nome} em {self.data_criacao}"
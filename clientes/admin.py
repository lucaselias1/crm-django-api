from django.contrib import admin
from .models import Cliente, ListarClientes

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'data_cadastro')
    search_fields = ('nome', 'email')

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(ListarClientes)


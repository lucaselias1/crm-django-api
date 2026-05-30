from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Cliente, Nota

class CRMCompletoTestCase(APITestCase):

    def setUp(self):
        # 1. Configuração de Perfis e Usuários
        self.grupo_admin = Group.objects.create(name='administrador')
        self.grupo_vendedor = Group.objects.create(name='vendedor')

        self.admin_user = User.objects.create_superuser(username='admin', password='password123')
        self.vendedor_1 = User.objects.create_user(username='vendedor1', password='password123')
        self.vendedor_2 = User.objects.create_user(username='vendedor2', password='password123')

        self.vendedor_1.groups.add(self.grupo_vendedor)
        self.vendedor_2.groups.add(self.grupo_vendedor)

        # 2. Criação de Dados Iniciais para os Testes
        self.cliente_vendedor_1 = Cliente.objects.create(
            nome="Lucas Ribeiro", email="lucas@crm.com", telefone="11999999999", usuario_responsavel=self.vendedor_1
        )
        self.cliente_vendedor_2 = Cliente.objects.create(
            nome="Amanda Costa", email="amanda@crm.com", telefone="21988888888", usuario_responsavel=self.vendedor_2
        )

        # 3. Rotas da API
        self.url_token = reverse('token_obtain_pair')
        self.url_clientes_list = reverse('cliente-list')
        self.url_clientes_create = reverse('cliente-create')
        self.url_notas_create = reverse('nota-create')

    # ==========================================
    # FLUXO 1: AUTENTICAÇÃO E ROTAS PROTEGIDAS
    # ==========================================
    def test_login_com_dados_validos_gera_token(self):
        """Valida que o login correto devolve os tokens access e refresh"""
        data = {"username": "vendedor1", "password": "password123"}
        response = self.client.post(self.url_token, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_com_dados_invalidos(self):
        """Valida que dados de login incorretos são rejeitados"""
        data = {"username": "vendedor1", "password": "senha_errada"}
        response = self.client.post(self.url_token, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_acesso_a_rota_protegida_sem_token(self):
        """Garante que usuários não autenticados são barrados nas rotas de clientes"""
        response = self.client.get(self.url_clientes_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ==========================================
    # FLUXO 2: CADASTRO DE CLIENTES (VÁLIDO/INVÁLIDO)
    # ==========================================
    def test_cadastro_cliente_com_dados_validos(self):
        """Vendedor consegue cadastrar cliente com sucesso e vira o dono dele"""
        self.client.force_authenticate(user=self.vendedor_1)
        data = {"nome": "Novo Cliente", "email": "novo@email.com", "telefone": "123456"}
        response = self.client.post(self.url_clientes_create, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cliente.objects.filter(nome="Novo Cliente").count(), 1)
        # Verifica se o dono salvo foi o vendedor logado
        cliente_salvo = Cliente.objects.get(nome="Novo Cliente")
        self.assertEqual(cliente_salvo.usuario_responsavel, self.vendedor_1)

    def test_cadastro_cliente_com_dados_invalidos(self):
        """Valida que o serializer rejeita campos em branco ou incorretos"""
        self.client.force_authenticate(user=self.vendedor_1)
        data = {"nome": "", "email": "email_invalido", "telefone": ""}
        response = self.client.post(self.url_clientes_create, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ==========================================
    # FLUXO 3: CRIAÇÃO E CONSULTA DE NOTAS
    # ==========================================
    def test_criar_e_listar_notas_associadas_ao_cliente(self):
        """Cria uma nota para o cliente e valida que ela é listada na rota correta"""
        self.client.force_authenticate(user=self.vendedor_1)
        
        # Criar Nota via POST
        data = {"cliente": self.cliente_vendedor_1.id, "texto": "Anotação de reunião pedagógica."}
        response = self.client.post(self.url_notas_create, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Listar Nota via GET
        url_listar_notas = reverse('cliente-nota-list', kwargs={'cliente_id': self.cliente_vendedor_1.id})
        response = self.client.get(url_listar_notas)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['texto'], "Anotação de reunião pedagógica.")

    # ==========================================
    # FLUXO 4: PERMISSÕES DE ACESSO (OWNERSHIP)
    # ==========================================
    def test_vendedor_nao_acessa_clientes_de_outro_vendedor(self):
        """Vendedor 1 não pode ver a Amanda (cliente do Vendedor 2)"""
        self.client.force_authenticate(user=self.vendedor_1)
        response = self.client.get(self.url_clientes_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], "Lucas Ribeiro") # Só vê o dele

    def test_admin_acessa_todos_os_clientes(self):
        """Administrador tem passe livre para ver a lista inteira de clientes"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.url_clientes_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # Vê os 2 clientes cadastrados

    # ==========================================
    # FLUXO 5: FILTROS DE LISTAGEM (CASE-INSENSITIVE / PARCIAL)
    # ==========================================
    def test_filtro_de_busca_por_nome_case_insensitive(self):
        """Testa o parâmetro ?search= com texto parcial e maiúsculo/minúsculo"""
        self.client.force_authenticate(user=self.vendedor_1)
        
        # Buscando por 'LUCAS' (caixa alta) deve achar 'Lucas Ribeiro'
        response = self.client.get(f"{self.url_clientes_list}?search=LUCAS")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], "Lucas Ribeiro")
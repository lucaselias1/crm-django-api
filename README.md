# 🚀 CRM API - Sistema de Gestão de Clientes e Interações

Este é um ecossistema de API robusto para gerenciamento de clientes e registro de interações (notas), desenvolvido com **Django Rest Framework (DRF)**. O projeto conta com autenticação segura, controle de acesso baseado em perfis (RBAC), banco de dados relacional de produção, conteinerização completa e esteira de integração contínua (CI).

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python 3.12 / Django 5.x / Django REST Framework
* **Autenticação:** JWT (JSON Web Tokens) via `django-rest-framework-simplejwt`
* **Banco de Dados:** PostgreSQL (Produção) / SQLite (Testes Locais)
* **Containers:** Docker / Docker Compose
* **Qualidade de Código:** Coverage.py (Mapeamento de testes)
* **CI/CD:** GitHub Actions (Pipeline automatizado)

---

## 🔒 Arquitetura de Segurança e Permissões

O sistema implementa **RBAC (Role-Based Access Control)** combinado com regras rígidas de **Ownership** (Dono do Registro):

* **Perfil Administrador (`is_staff` ou Grupo `administrador`):** Possui acesso total e irrestrito ao sistema, podendo listar, criar, editar e visualizar clientes ou notas de qualquer usuário.
* **Perfil Vendedor (Grupo `vendedor`):** Acesso estritamente controlado. Um vendedor só possui visibilidade e permissão de edição sobre os clientes e notas que ele mesmo cadastrou (**Ownership**). Ele é impedido de acessar dados de outros vendedores.

---

## 📦 Como Rodar o Projeto com Docker (Recomendado)

O projeto está totalmente configurado para subir o ambiente de desenvolvimento e o banco de dados PostgreSQL com **apenas um comando**.

### Pré-requisitos
* Possuir o [Docker](https://www.docker.com/) e o Docker Compose instalados.

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git)
   cd NOME_DO_REPOSITORIO

2.  Suba os containers da aplicação:
    Bash

    docker compose up --build

    Este comando irá baixar a imagem do PostgreSQL, construir o container da API Django, rodar as migrações do banco de dados automaticamente e expor a aplicação.

3.  A API estará disponível no endereço: http://localhost:8000/

🧪 Testes Automatizados e Cobertura

O projeto possui uma base sólida de testes cobrindo fluxos felizes e cenários de erro (dados inválidos, invasão de rotas, e-mails duplicados e filtros parciais).

Para rodar os testes localmente e verificar o relatório de cobertura de código (coverage):

1.  Ative seu ambiente virtual e execute:
    Bash

    coverage run --source='.' manage.py test clientes

2.  Para ver o relatório no terminal:
    Bash

    coverage report

    Atualmente o projeto conta com 100% de cobertura nos módulos críticos de segurança (views, permissions e serializers).

🤖 Integração Contínua (GitHub Actions)

A cada git push ou pull_request realizado nas branches principais, um workflow automatizado é disparado no GitHub Actions para garantir a saúde do sistema. O pipeline executa:

1.  Instalação limpa das dependências.

2.  Execução de toda a suíte de testes.

3.  Validação do relatório de cobertura (Coverage).

4.  Validação do Build da imagem Docker para checar se a receita (Dockerfile) continua íntegra.

## 🛣️ Principais Endpoints da API

| Método | Endpoint | Descrição | Acesso |
| :--- | :--- | :--- | :--- |
| **POST** | `/api/token/` | Gera os tokens JWT (Access e Refresh) | Público |
| **POST** | `/api/token/refresh/` | Renova o Token de Acesso expirado | Público |
| **GET** | `/api/clientes/` | Lista os clientes (Filtro por `?search=`) | Autenticado (Vê apenas os seus / Admin vê tudo) |
| **POST** | `/api/clientes/novo/` | Cadastra um novo cliente | Autenticado (Vincula o dono automaticamente) |
| **POST** | `/api/notas/novo/` | Cria uma nota para um cliente específico | Autenticado (Dono do cliente ou Admin) |
| **GET** | `/api/clientes/<id>/notas/` | Lista as notas de um cliente específico | Autenticado (Dono do cliente ou Admin) |

## 🤝 Como Contribuir

1. Faça um **Fork** do projeto.
2. Crie uma nova branch com sua modificação: `git checkout -b minha-nova-feature`.
3. Salve suas alterações e faça um commit: `git commit -m "Adiciona nova feature X"`.
4. Envie para a sua branch: `git push origin minha-nova-feature`.
5. Abra um **Pull Request** detalhando as alterações.

---

## ✒️ Desenvolvedor

* **Lucas Elias** - *Desenvolvimento Backend, Testes e DevOps* - [Meu GitHub](https://github.com/lucaselias1)

---

Este projeto foi desenvolvido como um marco técnico de boas práticas em APIs REST, segurança e automação. Sinta-se à vontade para usá-lo ou dar feedbacks!

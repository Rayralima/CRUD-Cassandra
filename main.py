from astrapy import DataAPIClient
import uuid

# Conectando ao AstraDB via REST API
client = DataAPIClient("SUA_SENHA_ASTRADB")
db = client.get_database_by_api_endpoint("https://e8961dbc-c149-44ca-8c01-3ead80708cce-us-east1.apps.astra.datastax.com")

usuarios = db["usuarios"]
posts = db["posts"]

# Função adicionar ususuário
def adicionar_usuario():
    nome = input("Nome: ")
    email = input("Email: ")
    user_id = str(uuid.uuid4())
    usuarios.insert_one({
        "_id": user_id,
        "nome": nome,
        "email": email
    })
    print("Usuário adicionado com sucesso!")

# Função listar usuários
def listar_usuarios():
    print("\nUsuários cadastrados:")
    for user in usuarios.find():
        print(f"- {user['nome']} ({user['_id']})")

# Função adicionar post
def adicionar_post():
    user_id = input("ID do usuário: ")
    titulo = input("Título do post: ")
    conteudo = input("Conteúdo: ")
    post_id = str(uuid.uuid4())
    posts.insert_one({
        "_id": post_id,
        "usuario_id": user_id,
        "titulo": titulo,
        "conteudo": conteudo
    })
    print("Post adicionado com sucesso!")

# Função listar posts de um usuário
def listar_posts_usuario():
    user_id = input("ID do usuário: ")
    print(f"\nPosts do usuário {user_id}:")
    for post in posts.find({"usuario_id": user_id}):
        print(f"- {post['titulo']} ({post['_id']})\n  {post['conteudo']}")

# Função atualizar post
def atualizar_post():
    post_id = input("ID do post a atualizar: ")
    novo_titulo = input("Novo título: ")
    novo_conteudo = input("Novo conteúdo: ")

    try:
        result = posts.update_one(
            {"_id": post_id},
            {"$set": {"titulo": novo_titulo, "conteudo": novo_conteudo}}
        )

        updated = result.update_info.get("nModified", 0)
        encontrados = result.update_info.get("n", 0)

        if encontrados == 0:
            print("Nenhum post encontrado com esse ID.")
        elif updated > 0:
            print("Post atualizado com sucesso!")
        else:
            print("Post encontrado, mas nenhum campo foi alterado (mesmos valores).")

    except Exception as e:
        print(f"Erro inesperado: {e}")

# Função excluir post
def excluir_post():
    post_id = input("ID do post a excluir: ")
    result = posts.delete_one({"_id": post_id})
    if result.deleted_count:
        print("Post excluído com sucesso!")
    else:
        print("Post não encontrado.")

# Função menu
def menu():
    while True:
        print("\n--- MENU CRUD ---")
        print("1. Adicionar Usuário")
        print("2. Listar Usuários")
        print("3. Adicionar Post")
        print("4. Listar Posts de um Usuário")
        print("5. Atualizar Post")
        print("6. Excluir Post")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_usuario()
        elif opcao == '2':
            listar_usuarios()
        elif opcao == '3':
            adicionar_post()
        elif opcao == '4':
            listar_posts_usuario()
        elif opcao == '5':
            atualizar_post()
        elif opcao == '6':
            excluir_post()
        elif opcao == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Menu iniciar
menu()

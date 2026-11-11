from typing import List, Optional
from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# 1. Configuração do Banco de Dados
# Criamos um banco SQLite em memória para este exemplo
engine = create_engine("sqlite:///:memory:", echo=True)
SessionLocal = sessionmaker(bind=engine)


# 2. Definição do Modelo (Tabela)
class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)

    def __repr__(self) -> str:
        return f"Usuario(id={self.id}, nome='{self.nome}', email='{self.email}')"


# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)


# ==========================================
# FUNÇÕES DO CRUD
# ==========================================


# C - CREATE (Criar) # Você cria o objeto para adicioná-lo ao banco de dados
def criar_usuario(nome: str, email: str) -> Usuario:
    with SessionLocal() as session:
        novo_usuario = Usuario(nome=nome, email=email)
        session.add(novo_usuario)
        session.commit()  # Salva no banco
        session.refresh(novo_usuario)  # Atualiza o objeto com o ID gerado
        print(f"\n[CREATE] Usuário criado: {novo_usuario}")
        return novo_usuario


# R - READ (Ler/Buscar) # Você faz pesquisas utilizando a sessão do SQLAlchemy para buscar dados no banco de dados, transformando os resultados em objetos Python
def listar_usuarios() -> List[Usuario]:
    with SessionLocal() as session:
        # No SQLAlchemy 2.0, usamos session.scalars() com select()
        from sqlalchemy import select

        usuarios = session.scalars(select(Usuario)).all()
        print(f"\n[READ] Todos os usuários: {usuarios}")
        return list(usuarios)


def buscar_usuario_por_id(usuario_id: int) -> Optional[Usuario]:
    with SessionLocal() as session:
        usuario = session.get(Usuario, usuario_id)
        print(f"\n[READ] Busca por ID ({usuario_id}): {usuario}")
        return usuario


# U - UPDATE (Atualizar) # Você pega o objeto do banco de dados, altera o valor do atributo e salva fazendo o commit
def atualizar_email_usuario(usuario_id: int, novo_email: str) -> Optional[Usuario]:
    with SessionLocal() as session:
        usuario = session.get(Usuario, usuario_id)
        if usuario:
            usuario.email = novo_email
            session.commit()
            session.refresh(usuario)
            print(f"\n[UPDATE] Usuário ID {usuario_id} atualizado: {usuario}")
            return usuario
        print(f"\n[UPDATE] Usuário ID {usuario_id} não encontrado.")
        return None


# D - DELETE (Excluir) # Você pega o objeto e o deleta usando a sessão
def deletar_usuario(usuario_id: int) -> bool:
    with SessionLocal() as session:
        usuario = session.get(Usuario, usuario_id)
        if usuario:
            session.delete(usuario)
            session.commit()
            print(f"\n[DELETE] Usuário ID {usuario_id} excluído com sucesso.")
            return True
        print(f"\n[DELETE] Usuário ID {usuario_id} não encontrado.")
        return False


# ==========================================
# EXECUÇÃO DO FLUXO CRUD
# ==========================================
if __name__ == "__main__":
    print("\n--- INICIANDO TESTES DO CRUD ---")

    # 1. Testando o CREATE
    user1 = criar_usuario("Alice Silva", "alice@email.com")
    user2 = criar_usuario("Bob Souza", "bob@email.com")

    # 2. Testando o READ
    listar_usuarios()
    buscar_usuario_por_id(1)

    # 3. Testando o UPDATE
    atualizar_email_usuario(1, "alice.nova@email.com")
    buscar_usuario_por_id(1)

    # 4. Testando o DELETE
    deletar_usuario(2)
    listar_usuarios()

    print("\n--- TESTES CONCLUÍDOS ---")

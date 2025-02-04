from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from faker import Faker
import random
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.models import Base, Regiao, Loja, Produto, Categoria, Cliente, Vendedor, Venda, ProdutosVenda  # Supondo que as classes estão no arquivo models.py
from database.database import SessionLocal, engine  # Importando a sessão do seu arquivo de banco

# Inicializa o Faker
fake = Faker(['pt_BR'])

# Função para criar as categorias no banco
def criar_categorias(db: Session):
    categorias = ["Eletrônicos", "Roupas", "Alimentos", "Móveis", "Brinquedos", "Ferramentas", "Livros", "Jogos", "Esportes", "Beleza"]
    categoria_data = [Categoria(nome=categoria) for categoria in categorias]
    db.add_all(categoria_data)
    db.commit()

# Função para criar lojas no banco
def criar_lojas(db: Session):
    lojas = []
    for i in range(10):
        loja = Loja(
            nome=fake.company(),
            regiao_id=random.randint(1, 5),
            created_at=fake.date_this_decade()
        )
        lojas.append(loja)
    db.add_all(lojas)
    db.commit()

# Função para criar produtos no banco
def criar_produtos(db: Session):
    produtos = []
    caminho = r"faker/produtos.csv"
    df_produtos = pd.read_csv(caminho)
    
    # Cache de categorias
    categorias_cache = {categoria.nome: categoria.id for categoria in db.query(Categoria).all()}

    for _, row in df_produtos.iterrows():
        nome_produto = row["nome"]
        categoria = row["categoria"]
        
        # Encontrar a categoria_id correspondente no cache
        categoria_id = categorias_cache.get(categoria)

        if not categoria_id:
            # Caso a categoria não exista no cache, verificamos no banco
            categoria_db = db.query(Categoria).filter(Categoria.nome == categoria).first()
            
            if not categoria_db:
                # Caso a categoria não exista no banco, criamos uma nova
                categoria_db = Categoria(nome=categoria)
                db.add(categoria_db)
                db.commit()  # Persistir a nova categoria para obter o id
                categorias_cache[categoria] = categoria_db.id  # Atualizar o cache
            else:
                # Caso a categoria exista no banco, adicionamos ao cache
                categorias_cache[categoria] = categoria_db.id
            
            categoria_id = categorias_cache[categoria]  # Garantir que temos o id da categoria
        
        # Criar o produto
        produto = Produto (
            nome=nome_produto,
            categoria_id=categoria_id,
            preco=round(random.uniform(10.0, 500.0), 2),  # Gerar um preço aleatório
            created_at=fake.date_this_decade()
        )
        produtos.append(produto)

    # Adicionar os produtos ao banco
    db.add_all(produtos)
    db.commit()

# Função para criar as regiões no banco
def criar_regioes(db: Session):
    regioes = ["Norte", "Sul", "Leste", "Oeste", "Centro-Oeste"]
    regiao_data = [Regiao(nome=regiao) for regiao in regioes]
    db.add_all(regiao_data)
    db.commit()
# Função para criar clientes, vendedores e vendas no banco
def criar_vendas_clientes_vendedores(db: Session):
    clientes = []
    vendedores = []
    vendas = []
    produtos_venda = []
    for loja_id in range(1, 11):  # Para cada loja
        
        
        for day in range(365):  # Durante 365 dias
            data_venda = datetime.today() - timedelta(days=day)
            
            num_vendas = random.randint(50, 100)  # Número de vendas por dia
            print(f"Gerando dados para a loja {loja_id} no dia {data_venda} com {num_vendas} vendas")
            for _ in range(num_vendas):
                cliente_id = random.randint(1, 1000)
                vendedor_id = random.randint(1, 100)
                produto_ids = random.sample(range(1, 1001), 3)  # Seleciona 3 produtos aleatórios
                total = 0
            
                # Gerar cliente se necessário
                if cliente_id not in [c.id for c in clientes]:
                    cliente = Cliente(
                        id=cliente_id,
                        nome=fake.name(),
                        email=fake.email(),
                        telefone=fake.phone_number(),
                        created_at=fake.date_this_decade()
                    )
                    #db.add(cliente) # Adiciona o cliente ao banco
                    clientes.append(cliente)

                # Gerar vendedor se necessário
                if vendedor_id not in [v.id for v in vendedores]:
                    vendedor = Vendedor(
                        id=vendedor_id,
                        nome=fake.name(),
                        loja_id=loja_id,
                        created_at=fake.date_this_decade()
                    )
                    #db.add(vendedor) # Adiciona o vendedor ao banco
                    vendedores.append(vendedor)
                # Vendas
                venda = Venda(
                    cliente_id=cliente_id,
                    vendedor_id=vendedor_id,
                    loja_id=loja_id,
                    total=total,
                    data_venda=data_venda
                )

                vendas.append(venda)
                # Inserir os produtos vendidos
                for produto_id in produto_ids:
                    preco_unitario = round(random.uniform(10.0, 500.0), 2)
                    quantidade = random.randint(1, 5)  # Quantidade do produto na venda

                    produto_venda = ProdutosVenda(
                        venda=venda,
                        produto_id=produto_id,
                        quantidade=quantidade,
                        preco_unitario=preco_unitario
                    )
                    total += quantidade * preco_unitario  # Atualiza o total da venda
                    produtos_venda.append(produto_venda)

                venda.total = total  # Atualiza o valor total da venda

    # Inserir dados de clientes, vendedores, vendas e produtos_venda no banco
    db.add_all(clientes)
    db.add_all(vendedores)
    db.commit()  # Commit para persistir os clientes e vendedores antes das vendas
    print("Clientes e vendedores inseridos com sucesso!")
    db.add_all(vendas)
    db.add_all(produtos_venda)

    # Commit para salvar as alterações
    db.commit()

# Função principal para rodar as inserções
def main():
    db = SessionLocal()
    try:
        # Criar as tabelas no banco de dados (caso não existam)
        Base.metadata.create_all(bind=engine)
        # Criar categorias, lojas, produtos, clientes, vendedores e vendas no banco
        #criar_categorias(db)
        #criar_regioes(db)
        #criar_lojas(db)
        #criar_produtos(db)
        criar_vendas_clientes_vendedores(db)
        print("Dados inseridos com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from models.models import Cliente, Produto, Venda, Loja, Vendedor, ProdutosVenda, Categoria
from database.database import SessionLocal

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para exibir clientes
def exibir_clientes(db: Session):
    clientes = db.query(Cliente).all()
    clientes_data = [{"ID": cliente.id, "Nome": cliente.nome, "Email": cliente.email, "Telefone": cliente.telefone} for cliente in clientes]
    df_clientes = pd.DataFrame(clientes_data)
    st.dataframe(df_clientes)

# Função para exibir produtos
def exibir_produtos(db: Session):
    produtos = db.query(Produto).all()
    produtos_data = [{"ID": produto.id, "Nome": produto.nome, "Preço": produto.preco, "Categoria ID": produto.categoria_id} for produto in produtos]
    df_produtos = pd.DataFrame(produtos_data)
    st.dataframe(df_produtos)

# Função para exibir as vendas e seus detalhes
def exibir_vendas(db: Session):
    vendas_query = (
        db.query(
            Venda.id.label("Venda_ID"),
            Cliente.nome.label("Cliente"),
            Vendedor.nome.label("Vendedor"),
            Loja.nome.label("Loja"),
            Venda.total.label("Total"),
            Venda.data_venda.label("Data_da_Venda"),
        )
        .join(Cliente, Venda.cliente_id == Cliente.id)
        .join(Vendedor, Venda.vendedor_id == Vendedor.id)
        .join(Loja, Venda.loja_id == Loja.id)
    )

    # Paginação
    itens_por_pagina = 100
    total_vendas = vendas_query.count()
    total_paginas = max((total_vendas // itens_por_pagina) + (1 if total_vendas % itens_por_pagina > 0 else 0), 1)

    if "pagina_vendas" not in st.session_state:
        st.session_state.pagina_vendas = 1

    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.session_state.pagina_vendas > 1:
            if st.button("⬅️ Página Anterior"):
                st.session_state.pagina_vendas -= 1
                st.rerun()

    with col3:
        if st.session_state.pagina_vendas < total_paginas:
            if st.button("➡️ Próxima Página"):
                st.session_state.pagina_vendas += 1
                st.rerun()

    offset = (st.session_state.pagina_vendas - 1) * itens_por_pagina

    vendas_data = vendas_query.limit(itens_por_pagina).offset(offset).all()

    # Criar DataFrame com detalhes adicionais
    df_vendas = []
    for venda in vendas_data:
        # Adiciona a linha principal da venda
        df_vendas.append({
            "Venda ID": venda.Venda_ID,
            "Cliente": venda.Cliente,
            "Vendedor": venda.Vendedor,
            "Loja": venda.Loja,
            "Total": f"R$ {venda.Total:.2f}",
            "Data da Venda": venda.Data_da_Venda.strftime("%d/%m/%Y"),
        })
        
        # Detalhes dos produtos vendidos
        produtos = db.query(ProdutosVenda).filter(ProdutosVenda.venda_id == venda.Venda_ID).all()
        for produto in produtos:
            df_vendas.append({
                "Venda ID": f"Produto {produto.produto_id}",
                "Produto": f"ID: {produto.produto_id}",
                "Quantidade": produto.quantidade,
                "Preço Unitário": f"R$ {produto.preco_unitario:.2f}",
                "Total": f"R$ {produto.quantidade * produto.preco_unitario:.2f}",
                "Data da Venda": "Detalhes"
            })
        
        # Inserir uma linha em branco para separar os detalhes
        df_vendas.append({
            "Venda ID": "",
            "Cliente": "",
            "Vendedor": "",
            "Loja": "",
            "Total": "",
            "Data da Venda": ""
        })

    # Converter para DataFrame
    df = pd.DataFrame(df_vendas)

    # Exibir a tabela com os detalhes diretamente
    st.write(f"Página {st.session_state.pagina_vendas} de {total_paginas}")
    st.dataframe(df, use_container_width=True)


def exibir_detalhes_venda(db: Session, venda_id: int):
    st.subheader(f"Detalhes da Venda #{venda_id}")

    detalhes_venda_query = (
        db.query(
            Venda.id.label("Venda_ID"),
            Cliente.nome.label("Cliente"),
            Vendedor.nome.label("Vendedor"),
            Loja.nome.label("Loja"),
            Venda.total.label("Total"),
            Venda.data_venda.label("Data_da_Venda"),
            Produto.nome.label("Produto"),
            ProdutosVenda.quantidade.label("Quantidade"),
            ProdutosVenda.preco_unitario.label("Preço_Unitário"),
        )
        .join(Cliente, Venda.cliente_id == Cliente.id)
        .join(Vendedor, Venda.vendedor_id == Vendedor.id)
        .join(Loja, Venda.loja_id == Loja.id)
        .join(ProdutosVenda, ProdutosVenda.venda_id == Venda.id)
        .join(Produto, ProdutosVenda.produto_id == Produto.id)
        .filter(Venda.id == venda_id)
    )

    detalhes_venda = detalhes_venda_query.all()

    if not detalhes_venda:
        st.error("Venda não encontrada.")
        return

    # Exibir os detalhes da venda
    info_venda = detalhes_venda[0]
    st.write(f"**Cliente:** {info_venda.Cliente}")
    st.write(f"**Vendedor:** {info_venda.Vendedor}")
    st.write(f"**Loja:** {info_venda.Loja}")
    st.write(f"**Total:** R$ {info_venda.Total:.2f}")
    st.write(f"**Data da Venda:** {info_venda.Data_da_Venda.strftime('%d/%m/%Y')}")

    # Criar tabela de produtos da venda
    produtos_venda_df = pd.DataFrame([
        {
            "Produto": item.Produto,
            "Quantidade": item.Quantidade,
            "Preço Unitário": f"R$ {item.Preço_Unitário:.2f}",
            "Subtotal": f"R$ {item.Quantidade * item.Preço_Unitário:.2f}",
        }
        for item in detalhes_venda
    ])

    st.write("### Produtos Vendidos")
    st.dataframe(produtos_venda_df, use_container_width=True)


# Função para exibir lojas
def exibir_lojas(db: Session):
    lojas = db.query(Loja).all()
    lojas_data = [{"ID": loja.id, "Nome": loja.nome, "Região ID": loja.regiao_id} for loja in lojas]
    df_lojas = pd.DataFrame(lojas_data)
    st.dataframe(df_lojas)

# Título do aplicativo
st.title('Dashboard de Lojas de Varejo')

# Menu de navegação na barra lateral
opcao = st.sidebar.selectbox(
    "Selecione uma opção",
    ("Clientes", "Produtos", "Vendas", "Lojas")
)

# Obter sessão do banco de dados
db = next(get_db())

# Exibir os dados com base na opção selecionada
if opcao == "Clientes":
    st.header("Clientes")
    exibir_clientes(db)

elif opcao == "Produtos":
    st.header("Produtos")
    exibir_produtos(db)

elif opcao == "Vendas":
    st.header("Vendas")
    exibir_vendas(db)

elif opcao == "Lojas":
    st.header("Lojas")
    exibir_lojas(db)

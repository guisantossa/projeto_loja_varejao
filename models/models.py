# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Loja(Base):
    __tablename__ = "lojas"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    regiao_id = Column(Integer, ForeignKey("regioes.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    preco = Column(Float)
    created_at = Column(DateTime(timezone=True), default=func.now())

    # Relacionamento com produtos_venda
    vendas = relationship("ProdutosVenda", back_populates="produto")

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nome = Column(String)

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    telefone = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

class Vendedor(Base):
    __tablename__ = "vendedores"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    loja_id = Column(Integer, ForeignKey("lojas.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    vendedor_id = Column(Integer, ForeignKey("vendedores.id"))
    loja_id = Column(Integer, ForeignKey("lojas.id"))
    data_venda = Column(DateTime, default=func.now())
    total = Column(Float)

    # Relacionamento com produtos_venda
    produtos = relationship("ProdutosVenda", back_populates="venda")

class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(Integer, primary_key=True)
    loja_id = Column(Integer, ForeignKey("lojas.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer)

class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True)
    venda_id = Column(Integer, ForeignKey("vendas.id"))
    metodo = Column(String)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())

class Regiao(Base):
    __tablename__ = "regioes"

    id = Column(Integer, primary_key=True)
    nome = Column(String)

class Promocao(Base):
    __tablename__ = "promocoes"

    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    desconto = Column(Float)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)

class ProdutosVenda(Base):
    __tablename__ = "produtos_venda"

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey("vendas.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer)
    preco_unitario = Column(Float)

    venda = relationship("Venda", back_populates="produtos")
    produto = relationship("Produto", back_populates="vendas")


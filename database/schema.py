from pydantic import BaseModel, PositiveFloat, EmailStr, validator, Field
from datetime import datetime
from typing import Optional, List

# Produto
class ProdutoBase(BaseModel):
    nome: str
    preco: PositiveFloat
    categoria_id: int  # Referência à categoria
    descricao: Optional[str] = None  # Se necessário, adicione descrição

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[PositiveFloat] = None
    categoria_id: Optional[int] = None
    descricao: Optional[str] = None

# Loja
class LojaBase(BaseModel):
    nome: str
    regiao_id: int

class LojaCreate(LojaBase):
    pass

class LojaResponse(LojaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class LojaUpdate(BaseModel):
    nome: Optional[str] = None
    regiao_id: Optional[int] = None

# Categoria
class CategoriaBase(BaseModel):
    nome: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None

# Cliente
class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None

# Vendedor
class VendedorBase(BaseModel):
    nome: str
    loja_id: int

class VendedorCreate(VendedorBase):
    pass

class VendedorResponse(VendedorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class VendedorUpdate(BaseModel):
    nome: Optional[str] = None
    loja_id: Optional[int] = None

# Venda
class VendaBase(BaseModel):
    cliente_id: int
    vendedor_id: int
    loja_id: int
    total: PositiveFloat

class VendaCreate(VendaBase):
    pass

class VendaResponse(VendaBase):
    id: int
    data_venda: datetime

    class Config:
        from_attributes = True

class VendaUpdate(BaseModel):
    cliente_id: Optional[int] = None
    vendedor_id: Optional[int] = None
    loja_id: Optional[int] = None
    total: Optional[PositiveFloat] = None

# Pagamento
class PagamentoBase(BaseModel):
    venda_id: int
    metodo: str
    status: str

class PagamentoCreate(PagamentoBase):
    pass

class PagamentoResponse(PagamentoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PagamentoUpdate(BaseModel):
    metodo: Optional[str] = None
    status: Optional[str] = None

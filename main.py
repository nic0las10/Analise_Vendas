from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import InMemoryDatabase

app = FastAPI()

# Inicializa o banco de dados em memória para vendas
db = InMemoryDatabase()

# Modelo para validação de dados
class Venda(BaseModel):
    produto: str
    quantidade: int
    valor_total: float

# Endpoint raiz
@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de análise de vendas!"}

# Endpoint para listar todas as vendas
@app.get("/vendas")
def get_sales():
    vendas = db.list_sales()
    if not vendas:
        return {"message": "Nenhuma venda encontrada."}
    return vendas

# Endpoint para adicionar uma nova venda
@app.post("/vendas")
def create_sale(venda: Venda):
    try:
        nova_venda = db.create_sale(venda.produto, venda.quantidade, venda.valor_total)
        return {"message": "Venda criada com sucesso!", "venda": nova_venda}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar venda: {str(e)}")

# Endpoint para atualizar uma venda existente
@app.put("/vendas/{id}")
def update_sale(id: int, venda: Venda):
    updated_sale = db.update_sale(id, venda.produto, venda.quantidade, venda.valor_total)
    if not updated_sale:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return {"message": "Venda atualizada com sucesso!", "venda": updated_sale}

# Endpoint para deletar uma venda existente
@app.delete("/vendas/{id}")
def delete_sale(id: int):
    try:
        if not db.delete_sale(id):
            raise HTTPException(status_code=404, detail="Venda não encontrada")
        return {"message": f"Venda com ID {id} deletada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar venda: {str(e)}")

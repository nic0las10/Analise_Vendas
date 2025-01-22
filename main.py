from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Lista fictícia de vendas
vendas = [
    {"id": 1, "produto": "Camisa", "quantidade": 5, "valor_total": 100.0},
    {"id": 2, "produto": "Jaqueta", "quantidade": 2, "valor_total": 300.0},
]

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
    return vendas

# Endpoint para adicionar uma nova venda
@app.post("/vendas")
def create_sale(venda: Venda):
    # Criar um ID único para a nova venda
    novo_id = len(vendas) + 1
    nova_venda = venda.dict()
    nova_venda["id"] = novo_id

    # Adicionar à lista de vendas
    vendas.append(nova_venda)
    return nova_venda

# Endpoint para atualizar uma venda existente
@app.put("/vendas/{id}")
def update_sale(id: int, venda: Venda):
    for i, v in enumerate(vendas):
        if v["id"] == id:
            # Atualizar os dados da venda existente
            vendas[i] = {"id": id, **venda.dict()}
            return vendas[i]

    # Levantar uma exceção se o ID não for encontrado
    raise HTTPException(status_code=404, detail="Venda não encontrada")

# Endpoint para deletar uma venda existente
@app.delete("/vendas/{id}")
def delete_sale(id: int):
    for i, v in enumerate(vendas):
        if v["id"] == id:
            # Remover a venda da lista
            vendas.pop(i)
            return {"message": f"Venda com ID {id} deletada com sucesso!"}

    # Levantar uma exceção se o ID não for encontrado
    raise HTTPException(status_code=404, detail="Venda não encontrada")

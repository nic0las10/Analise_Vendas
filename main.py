from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import InMemoryDatabase
from script import gerar_dados_simulados  # Certifique-se de criar o script para gerar dados simulados
import csv
from fastapi.responses import FileResponse

app = FastAPI()

# Inicializa o banco de dados em memória para vendas
db = InMemoryDatabase()

# Gera dados simulados ao iniciar a aplicação
gerar_dados_simulados(db, quantidade=100)

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
    nova_venda = db.create_sale(venda.produto, venda.quantidade, venda.valor_total)
    return {"message": "Venda criada com sucesso!", "venda": nova_venda}

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
    if not db.delete_sale(id):
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return {"message": f"Venda com ID {id} deletada com sucesso!"}

# Endpoint para exportar dados para CSV
import csv
from fastapi.responses import FileResponse

@app.get("/exportar-csv")
def exportar_csv():
    arquivo_csv = "vendas.csv"
    with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Produto", "Quantidade", "Valor Total"])
        for venda in db.list_sales():
            writer.writerow([venda["id"], venda["produto"], venda["quantidade"], venda["valor_total"]])
    return FileResponse(arquivo_csv, media_type="text/csv", filename="vendas.csv")


app.get("/exportar-csv")
def exportar_csv():
    """
    Exporta as vendas cadastradas para um arquivo CSV.
    Retorna o arquivo para download.
    """
    arquivo_csv = "vendas.csv"
    try:
        # Cria o arquivo CSV
        with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Escreve o cabeçalho
            writer.writerow(["ID", "Produto", "Quantidade", "Valor Total"])
            # Escreve os dados das vendas
            for venda in db.list_sales():
                writer.writerow([venda["id"], venda["produto"], venda["quantidade"], venda["valor_total"]])
        
        # Retorna o arquivo para download
        return FileResponse(arquivo_csv, media_type="text/csv", filename="vendas.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exportar vendas: {str(e)}")
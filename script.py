import random

def gerar_dados_simulados(db, quantidade=50):
    produtos = ["Camisa", "Jaqueta", "Capacete", "Luvas", "Mochila"]
    for _ in range(quantidade):
        produto = random.choice(produtos)
        qtd = random.randint(1, 20)
        valor_total = qtd * random.uniform(50, 500)  # Preço entre R$50 e R$500
        db.create_sale(produto, qtd, round(valor_total, 2))

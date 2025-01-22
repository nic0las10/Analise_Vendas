class InMemoryDatabase:
    def __init__(self):
        # Inicializa o banco de dados com uma lista vazia para armazenar vendas
        self.sales = []
        # Variável para manter o controle do próximo ID a ser usado
        self.next_id = 1

    def create_sale(self, produto, quantidade, valor_total):
        # Cria uma nova venda
        sale = {
            "id": self.next_id,             # Atribui um ID único à venda
            "produto": produto,             # Adiciona o produto fornecido
            "quantidade": quantidade,       # Adiciona a quantidade fornecida
            "valor_total": valor_total      # Adiciona o valor total fornecido
        }
        self.sales.append(sale)             # Adiciona a venda à lista de vendas
        self.next_id += 1                   # Incrementa o ID para a próxima venda
        return sale                         # Retorna a venda criada

    def list_sales(self):
        # Retorna a lista de todas as vendas
        return self.sales

    def update_sale(self, sale_id, produto, quantidade, valor_total):
        # Atualiza uma venda com base no ID fornecido
        for sale in self.sales:
            if sale["id"] == sale_id:
                # Atualiza os campos da venda com os novos valores
                sale.update({
                    "produto": produto,
                    "quantidade": quantidade,
                    "valor_total": valor_total
                })
                return sale                 # Retorna a venda atualizada
        return None                         # Retorna None se o ID não for encontrado

    def delete_sale(self, sale_id):
        # Remove a venda da lista com base no ID fornecido
        for sale in self.sales:
            if sale["id"] == sale_id:
                self.sales.remove(sale)     # Remove a venda da lista
                return True                 # Retorna True se a venda foi removida
        return False                        # Retorna False se o ID não foi encontrado

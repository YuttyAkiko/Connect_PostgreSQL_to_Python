import psycopg2

# classe de funcionarios
class FuncionarioDB:
    def __init__(self, host, database, user, password):
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()
        self._criar_tabela()

    # criar tabela caso nao exista
    def _criar_tabela(self):
        try:
            create_table_query = """
                CREATE TABLE IF NOT EXISTS cad_funcionarios (
                    user_id serial PRIMARY KEY,
                    nome VARCHAR(50) UNIQUE NOT NULL,
                    data_contratação TIMESTAMP NOT NULL,
                    idade INTEGER CHECK (idade >= 18),
                    salario INTEGER NOT NULL
                );
            """
            self.cursor.execute(create_table_query)
            self.connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            # printa o erro caso o banco de dados já exista
            print(error)

    # inserir novos dados
    def _inserir_dados(self, dados_para_inserir):
        insert_data_query = """
            INSERT INTO cad_funcionarios (user_id, nome, data_contratação, idade, salario)
            VALUES (%s, %s, %s, %s, %s);
        """
        self.cursor.execute(insert_data_query, dados_para_inserir)
        self.connection.commit()

    # consultando dados 
    def _consultar_dados(self):
        consulta_query = "SELECT * FROM cad_funcionarios;"
        self.cursor.execute(consulta_query)
        dados = self.cursor.fetchall()
        return dados

    # Atualizar dados
    def _atualizar_dados(self, novo_user_id, novo_salario):
        atualizacao_query = "UPDATE cad_funcionarios SET salario = %s WHERE user_id = %s;"
        self.cursor.execute(atualizacao_query, (novo_salario, novo_user_id))
        self.connection.commit()

    # Excluir dados
    def _excluir_dados(self, user_id_para_excluir):
        exclusao_query = "DELETE FROM cad_funcionarios WHERE user_id = %s;"
        self.cursor.execute(exclusao_query, (user_id_para_excluir,))
        self.connection.commit()

    # fechar conexao
    def _fechar_conexao(self):
        self.cursor.close()
        self.connection.close()
        print('Conexão fechada com sucesso.')



if __name__ == "__main__":

    # Exemplo de utilização da classe
    funcionario_db = FuncionarioDB(
        host='localhost',
        database='clinicavision',
        user='postgres',
        password='12345'
    )
    # ----  CHAMANDO AS FUNÇÕES DA CLASSE FUNCIONARIOS ----

    # # inserir dados
    # dados_para_inserir = [
    #     # (123457, 'Yutty', '2023-10-02', 30, 1850),
    #     # (123458, 'Lucas', '2023-11-05', 27, 1550),
    #     (123458, 'Fernando', '2023-11-09', 18, 1500),
    #     # Adicione mais tuplas de dados conforme necessário
    # ]
    # funcionario_db._inserir_dados(dados_para_inserir[0])

    # # Consultar dados
    # dados_consultados = funcionario_db._consultar_dados()
    # print("Dados na tabela:")
    # for dado in dados_consultados:
    #     print(dado)

    # # Atualizar dados
    # novo_user_id = 123456
    # novo_salario = 1850
    # funcionario_db._atualizar_dados(novo_user_id, novo_salario)

    # # Consultar dados após atualização
    # dados_atualizados = funcionario_db._consultar_dados()
    # print("\nDados após a atualização:")
    # for dado in dados_atualizados:
    #     print(dado)

    # # Excluir dados
    # user_id_para_excluir = 123458
    # funcionario_db._excluir_dados(user_id_para_excluir)

    # # Consultar dados após exclusão
    # dados_apos_exclusao = funcionario_db._consultar_dados()
    # print("\n Dados após a exclusão:")
    # for dado in dados_apos_exclusao:
    #     print(dado)

    funcionario_db._fechar_conexao()

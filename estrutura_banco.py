import psycopg2


#Classe para fazer a conexão com  banco de dados
class Conexao:
    
    #Construtor para já se conectar com o banco
    def __init__(self):
        try:
            #Se conecta com o banco de dados com as configurações estabelecidas
            self.conexao = psycopg2.connect(host="localhost",database="desafio", user="postgres", password="")
            
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)


    #Criação de tabelas no banco de dados do postgres 
    def criar_tabelas(self):
        tabelas =   (
            """Create table sistema_operacional(
                id serial Primary Key,
                nome varchar(200) NOT NULL
            )""",
            """Create table pais(
                id serial Primary Key,
                nome varchar(200) NOT NULL
            )""",
            """Create table empresa(
                id serial Primary Key,
                nome varchar(200) NOT NULL
            )""",
            """Create table ferramenta_comunic(
                id serial Primary Key,
                nome varchar(300) NOT NULL
            )""",
            """Create table linguagem_programacao(
                id serial Primary Key,
                nome varchar(200) NOT NULL
            )""",
            """Create table respondente(
                id serial Primary Key,
                nome varchar(200) NOT NULL,
                contrib_open_source integer NOT NULL,
                programa_hobby integer NOT NULL,
                salario float NOT NULL,
                sistema_operacional_id integer,
                pais_id integer,
                empresa_id integer,
                Foreign Key (sistema_operacional_id) 
                    References sistema_operacional(id)
                    On Update Cascade On Delete Cascade,
                Foreign Key (pais_id) 
                    References pais(id)
                    On Update Cascade On Delete Cascade,
                Foreign Key (empresa_id) 
                    References empresa(id)
                    On Update Cascade On Delete Cascade
            )""",
            """Create table resp_usa_linguagem(
                respondente_id integer,
                linguagem_programacao_id integer,
                momento integer,
                Foreign Key (respondente_id) 
                    References respondente(id)
                    On Update Cascade On Delete Cascade,
                Foreign Key (linguagem_programacao_id) 
                    References linguagem_programacao(id)
                    On Update Cascade On Delete Cascade
            )""",
            """Create table resp_usa_ferramenta(
                ferramenta_comunic_id integer,
                respondente_id integer,
                momento integer,
                Foreign Key (ferramenta_comunic_id) 
                    References ferramenta_comunic(id)
                    On Update Cascade On Delete Cascade,
                Foreign Key (respondente_id) 
                    References respondente(id)
                    On Update Cascade On Delete Cascade
            )"""         
            )
        try:
            cursor = self.conexao.cursor()
            for tabela in tabelas:
                cursor.execute(tabela)
            cursor.close()
            
            self.conexao.commit()
            print("Tabelas criadas com sucesso.")
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        pass
        
            
    #Procedimento para deletar as tabelas se caso elas existirem
    def deletarTabelas(self):
        
        tabelas = ("""DROP TABLE IF EXISTS resp_usa_ferramenta""",
                """DROP TABLE IF EXISTS resp_usa_linguagem""",
                """DROP TABLE IF EXISTS respondente""",
                """DROP TABLE IF EXISTS linguagem_programacao""",
                """DROP TABLE IF EXISTS ferramenta_comunic""",
                """DROP TABLE IF EXISTS empresa""",
                """DROP TABLE IF EXISTS pais""",
                """DROP TABLE IF EXISTS sistema_operacional"""
                )
        try:
            cursor = self.conexao.cursor()
            for tabela in tabelas:
                cursor.execute(tabela)
            cursor.close()
            
            self.conexao.commit()
            print("Tabelas deletadas com sucesso.")
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        pass
        
        
        
    #Função que insere os dados na tabela e retorna o id da linha inserida
    def inserir_dados_id(self,dados):
        id = 0
        try:
            cursor = self.conexao.cursor()
            cursor.execute(dados)
            id = cursor.fetchone()[0]
            cursor.close()
            self.conexao.commit()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        return(id)
        pass
    
    #Procedimento que insere os dados na tabela
    def inserir_dados(self,dados):
        try:
            cursor = self.conexao.cursor()
            cursor.execute(dados)
            cursor.close()
            self.conexao.commit()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        pass
        
    #Função que verifica se um registro já fora cadastrado e caso já tenha sido cadastrado irá retornar o seu id
    def verificar_registro(self,dados):
        quantidade = 0
        identificador = 0
        try:
            cursor = self.conexao.cursor()
            cursor.execute(dados)
            quantidade = cursor.rowcount
            if(quantidade > 0):
                row = cursor.fetchone()
                identificador = row[0]
            cursor.close()
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            
        return(identificador,quantidade)
        pass
            
    #Função para realizar buscas sql dentro do banco de dados e retornar os resultados encontrados
    def selecionar_dados(self,dados):
        resp = []
        try:
            cursor = self.conexao.cursor()
            cursor.execute(dados)
            linha = cursor.fetchone()
            
            while linha is not None:
                resp.append(linha)
                linha = cursor.fetchone()
            
            cursor.close()
            
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            
        return(resp)
        pass

    #Procedimento que encerra a conexao com o banco de dados
    def encerrar_conexao(self):
        self.conexao.close()
        pass


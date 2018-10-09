import psycopg2

conexao = psycopg2.connect(host="localhost",database="desafio", user="postgres", password="")


def criar_tabelas():
    # Criação de tabelas no banco de dados do postgres 
    
    tabelas =   (
         """Create table sistema_operacional(
            id integer Primary Key,
            nome varchar(200) NOT NULL
         )""",
         """Create table pais(
            id integer Primary Key,
            nome varchar(200) NOT NULL
         )""",
         """Create table empresa(
            id integer Primary Key,
            nome varchar(200) NOT NULL
         )""",
         """Create table ferramenta_comunic(
            id integer Primary Key,
            nome varchar(200) NOT NULL
         )""",
        """Create table linguagem_programacao(
            id integer Primary Key,
            nome varchar(200) NOT NULL
         )""",
        """Create table respondente(
            id integer Primary Key,
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
        cursor = conexao.cursor()
        for tabela in tabelas:
            print(tabela)
            cursor.execute(tabela)
        cursor.close()
        
        conexao.commit()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        conexao.close()
    
criar_tabelas()
conexao.close()

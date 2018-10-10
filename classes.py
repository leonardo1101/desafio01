from estrutura_banco import *


# Classe para a tabela de sistemas operacionais, utilizando os seus atributos para realizar a inserção
class SistemaOperacional:
    
    def __init__(self, name):
        self.name = name
        self.id = 1
        pass
    
    def inserir(self):
        #Caso o nome seja vazio não será adicionado no banco de dados
        if(self.name !=  ""):
            cnx = Conexao()
            sql = """select id from sistema_operacional where nome = '"""+self.name+"""' ;"""
            self.id , quantidade = cnx.verificar_registro(sql)
            
            #Caso já esteja cadastrado não será adicionado no banco
            if(quantidade == 0):
                sql = """Insert into sistema_operacional values (default,'"""+ self.name+ """') RETURNING id;"""
                self.id = cnx.inserir_dados_id(sql)
            cnx.encerrar_conexao()    
        pass

# Classe para a tabela pais, utilizando os seus atributos para realizar a inserção
class Pais:    
        
    def __init__(self, name):
        self.name = name
        self.id = 1
        pass
    
    def inserir(self):
        #Caso o nome seja vazio não será adicionado no banco de dados
        if(self.name !=  ""):
            cnx = Conexao()
            sql = """select id from pais where nome = '"""+self.name+"""' ;"""
            self.id , quantidade  = cnx.verificar_registro(sql)

            #Caso já esteja cadastrado não será adicionado no banco
            if(quantidade == 0):
                sql = """Insert into pais values (default,'"""+ self.name+ """') RETURNING id;"""
                self.id = cnx.inserir_dados_id(sql)
                
            cnx.encerrar_conexao()    
        pass
      
# Classe para a tabela empresa, utilizando os seus atributos para realizar a inserção
class Empresa:
    
    def __init__(self, name):
        self.name = name
        self.id = 1
        pass
    
    def inserir(self):
        #Caso o nome seja vazio não será adicionado no banco de dados
        if(self.name !=  ""):
            cnx = Conexao()
            sql = """select id from empresa where nome = '"""+self.name+"""' ;"""
            self.id , quantidade  = cnx.verificar_registro(sql)
            
            #Caso já esteja cadastrado não será adicionado no banco
            if(quantidade == 0):
                sql = """Insert into empresa values (default,'"""+ self.name+ """') RETURNING id;"""
                self.id = cnx.inserir_dados_id(sql)

            cnx.encerrar_conexao()    
        pass
        
# Classe para a tabela ferramenta_comunic, utilizando os seus atributos para realizar a inserção
class FerramentaComunic:
    
    def __init__(self, name):
        self.name = name
        self.id = 1
        pass
    
    def inserir(self):
        #Caso o nome seja vazio não será adicionado no banco de dados
        if(self.name !=  ""):
            cnx = Conexao()
            sql = """select id from ferramenta_comunic where nome = '"""+self.name+"""' ;"""
            self.id , quantidade  = cnx.verificar_registro(sql)
            
            #Caso já esteja cadastrado não será adicionado no banco
            if(quantidade == 0):
                sql = """Insert into ferramenta_comunic values (default,'"""+ self.name+ """') RETURNING id;"""
                self.id = cnx.inserir_dados_id(sql)

            cnx.encerrar_conexao()    
        pass

# Classe para a tabela linguagem_programacao, utilizando os seus atributos para realizar a inserção
class LinguagemProgramacao:
    
    def __init__(self, name):
        self.name = name
        self.id = 1
        pass
    
    def inserir(self):
        #Caso o nome seja vazio não será adicionado no banco de dados
        if(self.name !=  ""):
            cnx = Conexao()
            sql = """select id from linguagem_programacao where nome = '"""+self.name+"""' ;"""
            self.id , quantidade  = cnx.verificar_registro(sql)

            #Caso já esteja cadastrado não será adicionado no banco
            if(quantidade == 0):
                sql = """Insert into linguagem_programacao values (default,'"""+ self.name+ """') RETURNING id;"""
                self.id = cnx.inserir_dados_id(sql)

            cnx.encerrar_conexao()    
        pass

# Classe para a tabela respondente, utilizando os seus atributos para realizar a inserção
class Respondente:
    
    def __init__(self, name):
        self.name = name
        self.contrib_open_source = 0
        self.programa_hobby = 0
        self.salario = 0
        self.sistema_operacional_id = 0
        self.pais_id = 0
        self.empresa_id = 0
        self.id = 0
        pass
    
    def set_programa_hobby(self, programa_hobby):
        #Como as respostas tem apenas duas opções, realizou-se uma mudança para poupar espaço no banco
        if(programa_hobby == "Yes"):
            self.programa_hobby = 1
        else:
            self.programa_hobby = 0
        pass
    
    def set_salario(self, salario):
        #Regra de negócio estabelecida para salário
        try:
            self.salario = float(salario)
            self.salario = (self.salario/12) * 3.81
        except:
            self.salario = 0.0
        pass
    
    def set_sistema_operacional_id(self, sistema_operacional_id):
        #Caso o campo do sistema operaciona seja vazio não será associado nenhuma chave estrangeira
        if(sistema_operacional_id != 0):
            self.sistema_operacional_id = sistema_operacional_id
        else:
            self.sistema_operacional_id = ""
        pass
    
    def set_contrib_open_source(self, contrib_open_source):
        #Como as respostas tem apenas duas opções, realizou-se uma mudança para poupar espaço no banco
        if(contrib_open_source == "Yes"):
            self.contrib_open_source = 1
        else:
            self.contrib_open_source = 0
        pass
    
    def set_pais_id(self, pais_id):
        #Caso o campo do pais seja vazio não será associado nenhuma chave estrangeira
        if(pais_id != 0):
            self.pais_id = pais_id
        else:
            self.pais_id = ""
        pass
    
    def set_empresa_id(self, empresa_id):
        #Caso o campo do empresa seja vazio não será associado nenhuma chave estrangeira
        if(empresa_id != 0):
            self.empresa_id = empresa_id
        else:
            self.empresa_id = ""
        pass
    
    def inserir(self):
        cnx = Conexao()
        sql = """Insert into respondente values (default,'"""+ self.name +"""',"""+ str(self.contrib_open_source) +""", """+ str(self.programa_hobby) +""", """+ str(self.salario) +""","""+ str(self.sistema_operacional_id) +""", """+ str(self.pais_id) +""", """+ str(self.empresa_id) +""") RETURNING id;"""
        self.id = cnx.inserir_dados_id(sql)
        cnx.encerrar_conexao()    
        pass
    
# Classe para a tabela resp_usa_ferramenta, utilizando os seus atributos para realizar a inserção
class RespUsaFerramenta:

    def __init__(self, momento):
        self.momento = momento
        self.ferramenta_comunic_id = 0
        self.respondente_id = 0
        pass
    
    def set_respondente_id(self,num):
        self.respondente_id = num
    
    def set_ferramenta_comunic_id(self,num):
        if(num != 0):
            self.ferramenta_comunic_id = num
        else:
            self.ferramenta_comunic_id = ""
    def inserir(self):
        cnx = Conexao()
        sql = """Insert into resp_usa_ferramenta values ('"""+ str(self.ferramenta_comunic_id) +"""',"""+ str(self.respondente_id) +""", """+ str(self.momento) +""") """
        cnx.inserir_dados(sql)
        cnx.encerrar_conexao()
        pass
    
# Classe para a tabela resp_usa_linguagem, utilizando os seus atributos para realizar a inserção
class RespUsaLinguagem:

    def __init__(self, momento):
        self.momento = momento
        self.linguagem_programacao_id = 0
        self.respondente_id = 0
        pass
    
    def set_respondente_id(self,num):
        self.respondente_id = num
        
    def set_linguagem_programacao_id(self,num):
        if(num != 0):
            self.linguagem_programacao_id = num
        else:
            self.linguagem_programacao_id = ""
    def inserir(self):
        cnx = Conexao()
        sql = """Insert into resp_usa_linguagem values ('"""+ str(self.respondente_id) +"""',"""+ str(self.linguagem_programacao_id) +""", """+ str(self.momento) +""")"""
        cnx.inserir_dados(sql)
        cnx.encerrar_conexao()
        pass
        


    
        

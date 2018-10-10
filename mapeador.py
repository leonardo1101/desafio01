import csv
from classes import *
from estrutura_banco import *


#Procedimento para mapear os dados contidos na planilha para o banco de dados
def mapeador():
    #Caminho da planilha
    pwd_bc = "base_de_respostas_10k_amostra.csv"

    #Cria uma conexão com o banco de dados, deletando as tabelas existentes relacionadas ao desafio e criando novas tabelas
    cnx = Conexao()
    cnx.deletarTabelas()
    cnx.criar_tabelas()

    #Listas utilizadas para armazenar um objeto da tabela correspondente ou os dados quando houver mais de uma informação em cada linha (LanguageWorkedWith/CommunicationTools)
    respondente = []
    ferram_com = []
    lgm_prog = []
    sistemas_operacionais = []
    empresa =[]
    pais = []

    #Inteiro utilizados para armazenar o numero da coluna de cada campo da planilha, para que possa ser extraido a informação necessária
    col_os = 0
    col_hb = 0
    col_cs = 0
    col_ct = 0
    col_lww = 0
    col_so = 0
    col_csz = 0
    col_c = 0

    with open(pwd_bc, 'rt') as base_conhecimento:
        spamreader = csv.reader(base_conhecimento, delimiter=',')
        i = 0
        obj = ""
        #Pega a primeira linha, contendo o nome da coluna
        colunas = next(spamreader)
        
        #Mapeia o nome da coluna com o seu numero
        col_os = colunas.index("OpenSource")
        col_hb = colunas.index("Hobby")
        col_cs = colunas.index("ConvertedSalary")
        col_ct = colunas.index("CommunicationTools")
        col_lww = colunas.index("LanguageWorkedWith")
        col_so = colunas.index("OperatingSystem")
        col_csz = colunas.index("CompanySize")
        col_c = colunas.index("Country")
        
        #Percorre linha por linha, pegando as colunas que temos interesse
        for row in spamreader:
            #Pega o nome do pais e insere no banco
            pais = Pais(row[col_c])
            pais.inserir()
            
            #Pega o nome o tamanho da empresa e insere no banco de dados
            empresa = Empresa(row[col_csz])
            empresa.inserir()
            
            #Pega o nome do sistema operacional e insere no banco de dados
            sistem_operacional = SistemaOperacional(row[col_so])
            sistem_operacional.inserir()
            
            #Pega o campo de linguagens, separa as linguagens e insere cada uma no banco de dados 
            linguagensObj = []
            linguagens = row[col_lww].split(";")
            for j in range(len(linguagens)):
                obj = LinguagemProgramacao(linguagens[j])
                obj.inserir()
                linguagensObj.append(obj)
            
            #Pega o campo de feramentas, separa as feramentas e insere cada uma no banco de dados 
            ferramObj = []
            ferramentas = row[col_ct].split(";")
            for j in range(len(ferramentas)):
                obj = FerramentaComunic(ferramentas[j])
                obj.inserir()
                ferramObj.append(obj)
                
            
            #Cria um objeto respondente, inserindo seus atributos de acordo com as colunas e for fim insere no banco de dados
            resp = Respondente("respondente_" + str(i))
            i = i + 1
            resp.set_contrib_open_source(row[col_os])
            resp.set_programa_hobby(row[col_hb])
            resp.set_salario(row[col_cs])
            resp.set_sistema_operacional_id(sistem_operacional.id)
            resp.set_pais_id(pais.id)
            resp.set_empresa_id(empresa.id)
            resp.inserir()
            
            #Percorre cada ferramenta contida nessa linha e insere a sua relação com o respondente
            for obj in ferramObj:
                if(obj.id !=0):
                    rsf = RespUsaFerramenta(i)
                    rsf.set_respondente_id(resp.id)
                    rsf.set_ferramenta_comunic_id(obj.id)
                    rsf.inserir()
            
            #Percorre cada linguagem contida nessa linha e insere a sua relação com o respondente
            for obj in linguagensObj:
                if(obj.id !=0):
                    rul = RespUsaLinguagem(i)
                    rul.set_respondente_id(resp.id)
                    rul.set_linguagem_programacao_id(obj.id)
                    rul.inserir()
                    
            print("Linha ",i," inserida com sucesso no banco de dados.")
            
            

    cnx.encerrar_conexao() 
            
#Procedimento para responder a pergunta 1
def quant_resp_pais():
    cnx = Conexao()
    print("\nQuantidade de respondente de cada país:\n")
    sql = """ Select Count(*),P.nome from respondente R, pais P where R.pais_id = P.id GROUP BY P.nome ORDER BY count ;"""
    resultado = cnx.selecionar_dados(sql)
    for linha in resultado:
        print("País: ",linha[1],"\nQuantidade: ",linha[0],"\n")
    cnx.encerrar_conexao()

#Procedimento para responder a pergunta 2
def quant_resp_windows_usa():
    cnx = Conexao()
    sql = """ Select Count(*) from respondente R, pais P, sistema_operacional S where R.pais_id = P.id and R.sistema_operacional_id = S.id and S.nome = 'Windows' and P.nome = 'United States' ;"""
    resultado = cnx.selecionar_dados(sql)
    print("Quantidade de usuários que usam Windows e moram em United States:",resultado[0][0])
    cnx.encerrar_conexao()

#Procedimento para responder a pergunta 3
def quant_resp_salario():
    cnx = Conexao()
    sql = """ Select avg(R.salario) from respondente R, pais P, sistema_operacional S where R.pais_id = P.id and R.sistema_operacional_id = S.id and S.nome = 'Linux-based' and P.nome = 'Israel' ;"""
    resultado = cnx.selecionar_dados(sql)
    print("Media do salário de usuários que usam Linux-based e moram em Israel: {:.2f}".format(resultado[0][0]))
    cnx.encerrar_conexao()

#Procedimento para responder a pergunta 4    
def media_salario_desvio():
    cnx = Conexao()
    print("\nMédia e o desvio padrão do salário dos usuários que usam Slack para cada tamanho de empresa disponível: \n")
    sql = """ Select E.nome,avg(R.salario),stddev(R.salario) from respondente R, empresa E, resp_usa_ferramenta RF, ferramenta_comunic FC where R.empresa_id = E.id  and FC.nome = 'Slack'and FC.id = RF.ferramenta_comunic_id and RF.respondente_id = R.id GROUP BY E.nome  ;"""
    resultado = cnx.selecionar_dados(sql)
    for linha in resultado:
        print("Tamanho:",linha[0],"\nMedia do salário: {:.2f}".format(linha[1]),"\nDesvio padrão: {:.2f} \n".format(linha[2]))
    cnx.encerrar_conexao()

#Procedimento para responder a pergunta 5
def media_salario_sistema_operacional():
    cnx = Conexao()
    print("\nDiferença entre a média de salário dos respondentes do Brasil que acham que criar código é um hobby e a média de todos de salário de todos os respondentes brasileiros agrupado por cada sistema operacional que eles usam:\n")
    sql = """ Select S.nome,SBH.media_brasil_hobby,avg(R.salario),abs(avg(R.salario) - SBH.media_brasil_hobby) from (Select avg(R.salario) as media_brasil_hobby from respondente R, pais P where R.programa_hobby = 1 and P.id = R.pais_id and P.nome = 'Brazil') as SBH ,respondente R, sistema_operacional S, pais P where R.sistema_operacional_id = S.id and R.pais_id = P.id and P.nome = 'Brazil' GROUP BY S.nome,SBH.media_brasil_hobby ;"""
    resultado = cnx.selecionar_dados(sql)
    for linha in resultado:
        print("SO: ",linha[0],"\nMédia hobby: {:.2f}".format(linha[1]),"\nMedia geral: {:.2f}".format(linha[2]),"\nDiferença Media: {:.2f} \n".format(linha[3]))
    cnx.encerrar_conexao()

#Procedimento para responder a pergunta 6
def tres_maiores_tecnologias():
    cnx = Conexao()
    print("\nTop 3 tecnologias mais usadas pelos desenvolvedores:\n")
    sql = """ Select LP.nome,Count(*) from respondente R, resp_usa_linguagem RL, linguagem_programacao LP where RL.linguagem_programacao_id = LP.id and RL.respondente_id = R.id  GROUP BY LP.nome Order by count desc limit 3;"""
    resultado = cnx.selecionar_dados(sql)
    for linha in resultado:
        print("Tecnologia:",linha[0], "\nQuantidade de usuários:",linha[1],"\n")
        
    cnx.encerrar_conexao()

#Procedimento para responder a pergunta 7
def top_cinco_salario_pais():
    cnx = Conexao()
    print("\nTop 5 países em questão de salário:\n")
    sql = """ Select P.nome,MAX(R.salario) from respondente R,pais P where R.pais_id = P.id  GROUP BY P.nome Order by max desc limit 5;"""
    resultado = cnx.selecionar_dados(sql)
    for linha in resultado:
        print("Pais:",linha[0],"\nSalário:",linha[1],"\n")
    cnx.encerrar_conexao()

#Procedimento para responder a pergunta 8
def quant_usuario_maior_salario_minimo():
    cnx = Conexao()
    print("\nQuantos usuários ganham mais de 5 salários mínimos em cada um desses paises:\n")
    paises_salario = []
    paises_salario.append(['United States',4787.9])
    paises_salario.append(['India',243.52])
    paises_salario.append(['United Kingdom',6925.63])
    paises_salario.append(['Germany',6664])
    paises_salario.append(['Canada',5567.68])
    
    for ps in paises_salario:
        sql = """ Select Count(*) from respondente R,pais P where R.pais_id = P.id and P.nome = '"""+ps[0]+"""' and R.salario > """+str(ps[1] * 5)+""";"""
        resultado = cnx.selecionar_dados(sql)
        for linha in resultado:
            print("País:",ps[0],"\nQuantidade de usuários:",linha[0],"\n")
        
    cnx.encerrar_conexao()


quant_usuario_maior_salario_minimo()       
                

def interpretador(codigo):
    # Quebra o código em linhas
    linhas = codigo.split("\n")
    
    # Um dicionário para armazenar as variáveis
    variaveis = {}
    
    for linha in linhas:
        linha = linha.strip()  # Remove espaços em branco desnecessários
        
        # Se for uma linha de "definir"
        if linha.startswith("definir"):
            partes = linha[8:].strip().split(" como ")  # Pega o nome da variável e o valor
            nome = partes[0].strip()
            valor = partes[1].strip().strip('"')  # Remove aspas se houver
            variaveis[nome] = valor  # Armazena a variável
            
        # Se for uma linha de "mostrar"
        elif linha.startswith("mostrar"):
            conteudo = linha[8:].strip().strip('"')
            print(conteudo)  # Exibe o conteúdo

        # Se for uma estrutura condicional "se"
        elif linha.startswith("se"):
            condicao = linha[3:].split(" então ")[0].strip()
            comando = linha.split(" então ")[1].strip()
            
            # Aqui podemos apenas checar se a condição é "verdadeira" ou "falsa"
            if condicao == "verdadeiro":
                interpretador(comando)  # Executa o comando dentro da condição
        
        # Se for um laço "enquanto"
        elif linha.startswith("enquanto"):
            condicao = linha[8:].split(" faça ")[0].strip()
            comando = linha.split(" faça ")[1].strip()
            
            # Verifica a condição do laço (por enquanto, consideramos "verdadeiro" ou "falso")
            while condicao == "verdadeiro":
                interpretador(comando)  # Executa o comando dentro do laço
                break  # Evitar loops infinitos para esse exemplo
        else:
            print(f"Comando não reconhecido: {linha}")

# Exemplo de código na nossa linguagem
codigo = """
definir nome como "lalala"
mostrar "O nome é " + nome
se verdadeiro então mostrar "Isso é verdadeiro"
enquanto verdadeiro faça mostrar "Dentro do laço"
"""

# Executa o código
interpretador(codigo)

# Função para criar um carro com marca e modelo
def criar_carro(marca, modelo):
    return {"marca": marca, "modelo": modelo}

# Função para acelerar o carro
def acelerar(carro):
    print(f"O {carro['marca']} {carro['modelo']} está acelerando!")

# Função para parar o carro
def parar(carro):
    print(f"O {carro['marca']} {carro['modelo']} parou.")

# Função para criar um carro com cor adicional
def criar_carro_com_cor(marca, modelo, cor):
    carro = criar_carro(marca, modelo)  # Criamos um carro básico
    carro["cor"] = cor  # Adicionamos a cor
    return carro

# Função para exibir a cor do carro
def exibir_cor(carro):
    print(f"O carro é da cor {carro['cor']}.")

# Criando os carros:
carro1 = criar_carro("Fusca", "1984")  # Criando o carro Fusca
carro2 = criar_carro("Gol", "2019")  # Criando o carro Gol

# Acelerando e parando os carros:
print(carro1["marca"])  # Acessando a marca
print(carro1["modelo"])  # Acessando o modelo
acelerar(carro1)  # Acelerando o carro Fusca
parar(carro1)  # Parando o carro Fusca

print(carro2["marca"])  # Acessando a marca
print(carro2["modelo"])  # Acessando o modelo
acelerar(carro2)  # Acelerando o carro Gol
parar(carro2)  # Parando o carro Gol

# Criando o carro com cor:
carro3 = criar_carro_com_cor("Civic", "2022", "azul")  # Criando o carro Civic com cor azul
print(carro3["marca"])  # Acessando a marca
print(carro3["modelo"])  # Acessando o modelo
print(carro3["cor"])  # Acessando a cor
exibir_cor(carro3)  # Exibindo a cor do carro Civic

# Acelerando e parando o carro com cor:
acelerar(carro3)  # Acelerando o Civic
parar(carro3)  # Parando o Civic

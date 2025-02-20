# Vamos começar criando uma classe chamada "Carro"
# Uma classe é um molde ou planta que define como os objetos dessa classe serão.
# Ela define o que um objeto pode fazer (os métodos) e o que ele tem (os atributos).

class Carro:
    # A classe "Carro" tem dois atributos: "marca" e "modelo", e um método que vai fazer o carro "acelerar"
    
    # O método especial __init__ é o que chama quando criamos um novo objeto da classe.
    # Ele serve para inicializar os atributos do objeto (marcar a marca e o modelo).
    def __init__(self, marca, modelo):
        # Os atributos do objeto são definidos dentro de "__init__".
        # O "self" refere-se ao próprio objeto que está sendo criado.
        self.marca = marca  # Atributo que armazena a marca do carro
        self.modelo = modelo  # Atributo que armazena o modelo do carro
    
    # Esse é um método que define o comportamento do objeto. Aqui, estamos dizendo o que o carro faz.
    def acelerar(self):
        print(f"O {self.marca} {self.modelo} está acelerando!")
    
    # Vamos também adicionar outro método para o carro "parar"
    def parar(self):
        print(f"O {self.marca} {self.modelo} parou.")

# Vamos criar um objeto da classe Carro, ou seja, instanciar um carro.
# A instância será um objeto com os atributos e comportamentos definidos na classe.

carro1 = Carro("Fusca", "1984")  # Criando um carro do tipo "Fusca", modelo "1984"

# Agora, podemos acessar os atributos e métodos desse objeto:
print(carro1.marca)  # Aqui estamos acessando o atributo "marca" do carro1. Deve imprimir "Fusca"
print(carro1.modelo)  # Aqui estamos acessando o atributo "modelo" do carro1. Deve imprimir "1984"

# Chamando o método "acelerar" do carro1
carro1.acelerar()  # Isso vai chamar o método que imprime a mensagem de aceleração

# Chamando o método "parar" do carro1
carro1.parar()  # Isso vai chamar o método que imprime a mensagem de parada

# Agora, vamos criar outro carro, para ver como funciona com múltiplos objetos:

carro2 = Carro("Gol", "2019")  # Criando outro carro do tipo "Gol", modelo "2019"

# Acessando atributos do carro2:
print(carro2.marca)  # Deve imprimir "Gol"
print(carro2.modelo)  # Deve imprimir "2019"

# Chamando os métodos do carro2
carro2.acelerar()  # O Gol vai acelerar
carro2.parar()  # O Gol vai parar

# Criando outro exemplo de carro com uma característica adicional, como a cor:
class CarroComCor(Carro):  # A classe CarroComCor herda da classe Carro
    def __init__(self, marca, modelo, cor):  # Agora temos um novo atributo "cor"
        super().__init__(marca, modelo)  # Chamamos o __init__ da classe pai para manter os atributos de marca e modelo
        self.cor = cor  # Agora o carro tem um atributo adicional chamado "cor"
    
    def exibir_cor(self):  # Método para exibir a cor do carro
        print(f"O carro é da cor {self.cor}.")

# Criando um carro com cor:
carro3 = CarroComCor("Civic", "2022", "azul")  # Criamos um carro "Civic", modelo "2022", cor "azul"

# Exibindo as informações do carro3
print(carro3.marca)  # Marca do carro, deve imprimir "Civic"
print(carro3.modelo)  # Modelo do carro, deve imprimir "2022"
print(carro3.cor)  # Cor do carro, deve imprimir "azul"
carro3.exibir_cor()  # O carro3 vai exibir a sua cor

# Como o CarroComCor também herda de Carro, ele tem todos os métodos da classe Carro.
carro3.acelerar()  # O Civic vai acelerar
carro3.parar()  # O Civic vai parar

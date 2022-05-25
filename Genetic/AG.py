import random
import operator
import time 

random.seed(14)

#Listas
x = []
y = []
lista_cidades = []
nome_dos_pontos = []

#Variáveis
numero_de_pontos = 30
tamanho_da_pop_inicial = 50
tamanho_do_elitismo = 2
taxa_de_mutacao = 0.05
numero_de_geracoes = 30

inicio = time.time()

# Criando uma classe fitness
class Fitness:
    def __init__(self, rota):

        self.rota = rota
        self.distancia = 0
        self.fitness = 0.0

    def rota_distancia(self):
        if self.distancia == 0:
            distancia_da_rota = 0
            for i in range(0, len(self.rota)):
                cidade_inicial = self.rota[i]
                prox_cidade = None
                if i + 1 < len(self.rota):
                    prox_cidade = self.rota[i + 1]
                else:
                    prox_cidade = self.rota[0]
                distancia_da_rota += cidade_inicial.distancia(prox_cidade)
            self.distancia = distancia_da_rota
        return self.distancia

    def rota_fitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.rota_distancia())
        return self.fitness

# Classe de cidade para guardar pontos de entrega
class Cidade:
    def __init__(self, nome, x, y):
        self.nome = nome
        self.x = x
        self.y = y

    def distancia(self, Cidade):
        xDis = abs(self.x - Cidade.x)
        yDis = abs(self.y - Cidade.y)
        distancia = xDis+yDis
        return distancia

    def __repr__(self):
        return f'({str(self.nome)})'

# Gerando a Primeira População inicial
def popu_inicial(tam_popu_inicial, lista_cidades):
    populacao = []

    for i in range(0, tam_popu_inicial):
        populacao.append(criar_rota(lista_cidades))
    return populacao

# Gerando a população inicial e possiveis rotas
def criar_rota(lista_cidades):
    rota = random.sample(lista_cidades, len(lista_cidades))
    return rota

# Ordenando as rotas da população inicial de acordo com o seu fitness do maior pro menor
def ordenando_rotas(populacao):
    fitness_resultados = {}
    for i in range(0, len(populacao)):
        fitness_resultados[i] = Fitness(populacao[i]).rota_fitness()
    rotas_ordenadas = sorted(fitness_resultados.items(), key=operator.itemgetter(1), reverse=True)
    return rotas_ordenadas

# Calculando a média das distâncias em cada geração
def media_distancia_rotas(rotas_ordenadas):
    soma = 0
    for i in range(0,len(rotas_ordenadas)):
        soma += Fitness(rotas_ordenadas[i]).rota_distancia()
    return soma/len(rotas_ordenadas)

# Torneio
def torneio(popu_ordenada, tam_elitismo):
    resultado_selecao = []
    a = popu_ordenada[random.randint(0, len(popu_ordenada) - 1)]
    b = popu_ordenada[random.randint(0, len(popu_ordenada) - 1)]

    for i in range(0, tam_elitismo):
        resultado_selecao.append(popu_ordenada[i][0])
        
    for i in range(0, len(popu_ordenada) - tam_elitismo):
        a = popu_ordenada[random.randint(0, len(popu_ordenada) - 1)][0]
        b = popu_ordenada[random.randint(0, len(popu_ordenada) - 1)][0]
        while b == a:
            b = popu_ordenada[random.randint(0, len(popu_ordenada) - 1)][0]
        if a >= b:
            resultado_selecao.append(a)
        else:
            resultado_selecao.append(b)
    return resultado_selecao

# Acasalamento
def matingPool(populacao, resultado_selecao):
    matingpool = []
    for i in range(0, len(resultado_selecao)):
        index = resultado_selecao[i]
        matingpool.append(populacao[index])
    return matingpool

# CrossOver Aleatório
def crossOver1(pai1, pai2):
    filho = []
    filhoP1 = []
    filhoP2 = []

    geneA = int(random.random() * len(pai1))
    geneB = int(random.random() * len(pai1))

    inicio = min(geneA, geneB)
    final = max(geneA, geneB)

    for i in range(inicio, final):
        filhoP1.append(pai1[i])

    filhoP2 = [item for item in pai2 if item not in filhoP1]
    filho = filhoP1 + filhoP2
    return filho

# one-point CrossOver
def crossOver2(pai1, pai2):
    filho = []
    filhoP1 = []
    filhoP2 = []
    meio = len(pai1)//2
    for i in range(0, meio):
        filhoP1.append(pai1[i])
    filhoP2 = [item for item in pai2 if item not in filhoP1]
    filho = filhoP1 + filhoP2
    return filho

# Cross-Over em toda a população
def cross_over_popu(matingpool, tam_elitismo):
    filhos = []
    tamanho = len(matingpool) - tam_elitismo
    amostra = random.sample(matingpool, len(matingpool))

    for i in range(0, tam_elitismo):
        filhos.append(matingpool[i])

    for i in range(0, tamanho):
        filho = crossOver1(amostra[i], amostra[len(matingpool) - i - 1])
        filhos.append(filho)
    return filhos

# Função mutação em apenas um gene de uma unica rota
def mutar(individuo, taxa_mutacao):
    for trocado in range(len(individuo)):
        if (random.random() < taxa_mutacao):
            trocar_com = int(random.random() * len(individuo))

            Cidade1 = individuo[trocado]
            Cidade2 = individuo[trocar_com]

            individuo[trocado] = Cidade2
            individuo[trocar_com] = Cidade1
    return individuo

# Aplicando a mutação em toda a população
def mutar_popu(populacao, taxa_mutacao):
    popu_mutada = []

    for ind in range(0, len(populacao)):
        mutar_ind = mutar(populacao[ind], taxa_mutacao)
        popu_mutada.append(mutar_ind)
    return popu_mutada

# Moldando próxima geração juntando os passos
def prox_geracao(gene_atual, tam_elitismo, taxa_mutacao):
    popu_ordenada = ordenando_rotas(gene_atual)
    resultado_selecao = torneio(popu_ordenada, tam_elitismo)
    matingpool = matingPool(gene_atual, resultado_selecao)
    filhos = cross_over_popu(matingpool, tam_elitismo)
    prox_geracao = mutar_popu(filhos, taxa_mutacao)
    return prox_geracao

def algoritmo_genetico(populacao, tam_popu_inicial, tam_elitismo, taxa_mutacao, num_geracao):
    pop = popu_inicial(tam_popu_inicial, populacao)
    distancia_melhor_rota = [1 / ordenando_rotas(pop)[0][1]]
    media = [media_distancia_rotas(pop)]
    print(f'População inicial, Distância Inicial: {str(distancia_melhor_rota[0])}, Média: {float(media[0])}')

    for i in range(1, num_geracao + 1):
        #Exibindo gerações
        pop = prox_geracao(pop, tam_elitismo, taxa_mutacao)
        media.append(media_distancia_rotas(pop))
        distancia_melhor_rota.append(1 / ordenando_rotas(pop)[0][1])
        print(f'Geração {str(i)}, Distância: {distancia_melhor_rota[i]}, Media: {media[i]}')

    best_rota_index = ordenando_rotas(pop)[0][0]
    best_rota = pop[best_rota_index]

    return best_rota

for i in range(0, numero_de_pontos):
    cidade = input().split()
    nome_dos_pontos.append(str(cidade[0]))
    lista_cidades.append(Cidade(str(cidade[0]), int(cidade[1]), int(cidade[2])))

best_rota = algoritmo_genetico(
populacao = lista_cidades, 
tam_popu_inicial=tamanho_da_pop_inicial, 
tam_elitismo=tamanho_do_elitismo, 
taxa_mutacao=taxa_de_mutacao, 
num_geracao=numero_de_geracoes
)

print('Está é a melhor rota {}'.format(best_rota))

for i in best_rota:
    x.append(i.x)
    y.append(i.y)
x.append(best_rota[0].x)
y.append(best_rota[0].y)

fim = time.time()
print("O tempo de execução:", (fim-inicio))


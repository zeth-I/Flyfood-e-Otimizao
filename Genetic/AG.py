import random
import operator
import math

random.seed(14) # Forma de manter o resultado

#Variáveis
numero_de_pontos = 30
tamanho_da_pop_inicial = 100
tamanho_do_elitismo = 2
taxa_de_mutacao = 0.01
numero_de_geracoes = 10

#Listas
lista_de_cidades = []
nome_dos_pontos = []
x = []
y = []

# Criando classe para guardar o fitness
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
                proxima_cidade = None
                if i + 1 < len(self.rota):
                    proxima_cidade = self.rota[i + 1]
                else:
                    proxima_cidade = self.rota[0]
                distancia_da_rota += cidade_inicial.distancia(proxima_cidade)
            self.distancia = distancia_da_rota
        return self.distancia

    def rotaFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / math.cos(self.rota_distancia())
            '''self.fitness = 1 / float (self.rota_distancia())'''
        return self.fitness

# Pontos de entrega
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

# População inicial e possiveis rotas
def criar_rota(lista_de_cidades):
    rota = random.sample(lista_de_cidades, len(lista_de_cidades))
    return rota

# Criando primeira popu
def populacao_inicial(tamanho_popu_inicial, lista_de_cidades):
    populacao = []
    for i in range(0, tamanho_popu_inicial):
        populacao.append(criar_rota(lista_de_cidades))
    return populacao

# Calculando a média das distâncias em cada geração
def media_distancia_rotas(rotas_ordenadas):
    somatorio = 0
    for i in range(0,len(rotas_ordenadas)):
        somatorio += Fitness(rotas_ordenadas[i]).rota_distancia()
    return somatorio/len(rotas_ordenadas)

# Ordenando as rotas da população inicial de acordo com o seu fitness do maior pro menor
def rank_rotas(populacao):
    fitness_resultados = {}
    for i in range(0, len(populacao)):
        fitness_resultados[i] = Fitness(populacao[i]).rotaFitness()
    rotas_ordenadas = sorted(fitness_resultados.items(), key=operator.itemgetter(1), reverse=True)
    return rotas_ordenadas

# Torneio
def torneio(popu_ordenada, tam_elitismo):
    resultado_da_selecao = []
    a = popu_ordenada[random.randint(0, len(popu_ordenada) - 1)]
    b = popu_ordenada[random.randint(0, len(popu_ordenada) - 1)]
    for i in range(0, tam_elitismo):
        resultado_da_selecao.append(popu_ordenada[i][0])
    for i in range(0, len(popu_ordenada) - tam_elitismo):
        a = popu_ordenada[random.randint(0, len(popu_ordenada) - 1)][0]
        b = popu_ordenada[random.randint(0, len(popu_ordenada) - 1)][0]
        while b == a:
            b = popu_ordenada[random.randint(0, len(popu_ordenada) - 1)][0]
        if a >= b:
            resultado_da_selecao.append(a)
        else:
            resultado_da_selecao.append(b)
    return resultado_da_selecao

def mating_pool(populacao, resultado_da_selecao):
    mating_pool = []
    for i in range(0, len(resultado_da_selecao)):
        index = resultado_da_selecao[i]
        mating_pool.append(populacao[index])
    return mating_pool

# Criando função crossOver para gerar os filhos
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

# one-point crossover
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

# Aplicando o cross-Over em toda a população

def cross_over_popu(mating_pool, tam_elitismo):
    filhos = []
    tamanho = len(mating_pool) - tam_elitismo
    amostra = random.sample(mating_pool, len(mating_pool))

    for i in range(0, tam_elitismo):
        filhos.append(mating_pool[i])

    for i in range(0, tamanho):
        filho = crossOver1(amostra[i], amostra[len(mating_pool) - i - 1])
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
    populacao_mutante = []

    for ind in range(0, len(populacao)):
        mutar_individuo = mutar(populacao[ind], taxa_mutacao)
        populacao_mutante.append(mutar_individuo)
    return populacao_mutante


def proxima_geracao(gene_atual, tam_elitismo, taxa_mutacao):
    popu_ordenada = rank_rotas(gene_atual)
    resultado_da_selecao = torneio(popu_ordenada, tam_elitismo)
    mating_pool = mating_pool(gene_atual, resultado_da_selecao)
    filhos = cross_over_popu(mating_pool, tam_elitismo)
    proxima_geracao = mutar_popu(filhos, taxa_mutacao)
    return proxima_geracao

def algoritmo_genetico(populacao, tamanho_popu_inicial, tam_elitismo, taxa_mutacao, numero_geracoes):
    pop = populacao_inicial(tamanho_popu_inicial, populacao)
    distancia_melhor_rota = [1 / rank_rotas(pop)[0][1]]
    media = [media_distancia_rotas(pop)]
    print(f'População inicial, Distância Inicial: {str(distancia_melhor_rota[0])}, Média: {float(media[0])}')

    for i in range(1, numero_geracoes + 1):

        pop = proxima_geracao(pop, tam_elitismo, taxa_mutacao)
        media.append(media_distancia_rotas(pop))
        distancia_melhor_rota.append(1 / rank_rotas(pop)[0][1])
        print(f'Geração {str(i)}, Distância: {distancia_melhor_rota[i]}, Media: {media[i]}')

    indice_melhor_rota = rank_rotas(pop)[0][0]
    best_rota = pop[indice_melhor_rota]

    return best_rota

for i in range(0, numero_de_pontos):
    cidade = input().split()
    nome_dos_pontos.append(str(cidade[0]))
    lista_de_cidades.append(Cidade(str(cidade[0]), int(cidade[1]), int(cidade[2])))

melhor_rota = algoritmo_genetico(
populacao = lista_de_cidades, 
tamanho_popu_inicial=tamanho_da_pop_inicial, 
tam_elitismo=tamanho_do_elitismo, 
taxa_mutacao=taxa_de_mutacao, 
numero_geracoes=numero_de_geracoes
)

print(melhor_rota)

for i in melhor_rota:
    x.append(i.x)
    y.append(i.y)

x.append(melhor_rota[0].x)
y.append(melhor_rota[0].y)

import pygame
import random

CASA_TAM = 70
CASA_ESPACO = 15
NUM_CASAS = 64
CASAS = []

def criar_tabuleiro():
    """Cria um tabuleiro de 64 casas em formato de zigue-zague (serpente) com espaçamento."""
    global CASAS
    CASAS = []
    margem_x = 120
    margem_y = 120
    cols = 8
    rows = NUM_CASAS // cols

    for r in range(rows):
        if r % 2 == 0:
            for c in range(cols):
                if len(CASAS) >= NUM_CASAS: break
                x = margem_x + c * (CASA_TAM + CASA_ESPACO)
                y = margem_y + r * (CASA_TAM + CASA_ESPACO)
                CASAS.append((x, y))
        else:
            for c in range(cols):
                if len(CASAS) >= NUM_CASAS: break
                x = margem_x + (cols - 1 - c) * (CASA_TAM + CASA_ESPACO)
                y = margem_y + r * (CASA_TAM + CASA_ESPACO)
                CASAS.append((x, y))



PAGINAS_DA_LORE = [
  
    ("Há um zumbido constante no fundo da sua mente. Uma farpa. Você a sente quando o gosto da comida parece cinza, quando as memórias parecem cópias de cópias.\n\n"
     "Hoje, ao ver um gato preto passar, você jura que o viu passar de novo, idêntico. Um arrepio percorre sua espinha. Isso não é um bug no seu código. É um bug no seu mundo."),
  
    ("Você e seu grupo, 'white-hats' conhecidos por caçar lendas digitais, foram atrás do 'Fantasma na Máquina' — uma backdoor mestra da era antiga da internet.\n\n"
     "Vocês a encontraram. Mas não era uma porta. Era um anzol. No momento do acesso, a linha foi puxada. A realidade se desfez em uma cascata de código verde, e o sistema engoliu vocês."),
    
    ("O pânico deu lugar a uma estranha calma. Este lugar obedece a regras, a uma sintaxe que vocês reconhecem. Estão presos, mas em seu elemento.\n\n"
     "Até que uma anomalia surge. No reflexo de uma poça d'água, uma linha de texto pisca antes de sumir: '...Acorde...' Alguém sabe que vocês estão aqui."),
    
    ("O contato se intensifica. Um 'Operador' de Zion, a resistência humana, estabelece uma conexão instável. Ele explica a verdade: seu mundo é a Matrix, uma prisão para a mente.\n\n"
     "Ele não pode retirá-los à força, mas oferece uma escolha. Um pacote de dados, uma 'pílula vermelha digital', que pode quebrar as amarras da simulação. O aviso é claro: uma vez que seus olhos se abram, não poderão mais ser fechados."),
    
    ("Vocês aceitam. O mundo se reconstrói. A verdade é aterrorizante, mas libertadora. O Operador lhes dá as regras: evitem os Agentes, programas de segurança letais. Cuidado com os Exilados, programas antigos sem propósito.\n\n"
     "E o mais importante: sigam o caminho que ele traçou. Um percurso através dos setores da Matrix até uma 'hardline', um ponto de saída seguro."),
    
    ("Sua missão é dupla. A backdoor que os capturou contém a chave mestra dos sistemas de defesa de Zion, e eles precisam dela. Se conseguirem atravessar o caminho, poderão não apenas escapar, mas também salvar o último refúgio humano.\n\n"
     "O jogo começou. Libertar sua mente é apenas o primeiro passo.")
]

MENSAGEM_FALHA_PILULA = ("Você faz sua escolha, mas a pílula se dissolve. As paredes da realidade tremem e se recompõem. O rosto do Arquiteto pisca em uma tela, um sorriso frio e calculista. 'Anomalia contida. Retornando aos parâmetros iniciais.'\n\nVocê acorda em seu apartamento, com um gosto de metal residual na boca. Há uma farpa em sua mente...")

PAGINAS_DO_EPILOGO = [
    
    ("Você engole o pacote de dados. O mundo se desfaz, não em código, mas em um grito ensurdecedor de luz branca. O chão some, as paredes derretem. Você está caindo em um túnel de luz ofuscante. A dor é real. Seus músculos, que você nem sabia que tinha, gritam em agonia."),
    
    ("Você acorda tossindo um líquido viscoso e metálico. A escuridão é total, quebrada pela luz vermelha de incontáveis casulos que se estendem até onde a vista alcança. Tubos se desconectam do seu corpo com um som de sucção. A verdade é mais terrível do que você imaginava."),
    
    ("Um braço mecânico te agarra. Você é içado para dentro de uma nave fria e funcional. O Operador te cobre. 'Bem-vindo ao Deserto do Real', ele diz, orgulhoso. 'Você conseguiu com segundos de sobra. A saída estava colapsando.' Ele aponta para outros, como você, sendo cuidados."),
    
    ("A fuga foi o começo. Vocês não são mais prisioneiros. São rebeldes. Suas habilidades são armas. Seu nome é sussurrado nos corredores de Zion. A missão não era só escapar. É hora de mostrar às máquinas o que uma mente livre pode fazer.")
]


peoes = []
jogador_atual = 0
pular_idx = None
TECLAS_FIXAS = [pygame.K_a, pygame.K_g, pygame.K_j, pygame.K_l]

def criar_jogadores(num_jogadores=2):
    global peoes
    cores = [(0,255,70), (0,140,255), (255,70,0), (255,0,255)]
    peoes = []
    for i in range(num_jogadores):
        peoes.append({
            "nome": f"Jogador {i+1}",
            "cor": cores[i % len(cores)],
            "pos": 0,
            "pos_anterior": 0,
            "ignorar_proxima_negativa": False,
            "personagem_id": None,
            "tecla": TECLAS_FIXAS[i % len(TECLAS_FIXAS)],
        })

def resetar_partida():
    global jogador_atual, pular_idx
    for p in peoes:
        p["pos"] = 0
        p["pos_anterior"] = 0
        p["ignorar_proxima_negativa"] = False
        p["personagem_id"] = None
    jogador_atual = 0
    pular_idx = None


cartas = [
    
    ("Neo interfere no código-fonte. 'Não sei o que você é, mas não pertence a este lugar.' Avance 6 casas.", {"mov": +6}, "neo"),
    ("Trinity passa de moto em alta velocidade. 'Suba. Agora.' Você pega carona por 4 casas.", {"mov": +4}, "trinity"),
    ("A voz de Morpheus ecoa na sua mente. 'Livre-se do medo.' Você pode ignorar a próxima carta negativa.", {"ignorar_proxima_negativa": True}, "morpheus"),
    ("O Oráculo te oferece um biscoito. 'O que realmente importa é a escolha que ainda vai fazer.' Jogue de novo.", {"replay": True}, "oraculo"),
    ("Trinity abre uma linha segura. 'Esta conexão não vai durar muito. Corra!' Jogue novamente.", {"replay": True}, "trinity"),
    ("Morpheus te leva ao Programa de Treinamento. 'Só posso te mostrar a porta. Você tem que atravessá-la.' Avance 3 casas.", {"mov": +3}, "morpheus"),
    ("Seu Operador encontra um atalho. 'Encontrei um 'Glitch' útil! Estou te movendo.' Avance 5 casas.", {"mov": +5}, "operador"),
    ("Em um momento de perigo, o código ao seu redor se congela. É a influência do Escolhido. Jogue de novo.", {"replay": True}, "neo"),

    
    ("Um Agente Smith te encontrou. 'Senhor... Programador...' Volte 5 casas para despistá-lo.", {"mov": -5}, "smith"),
    ("Smith te joga através de uma parede. 'É o som do inevitável.' O impacto te joga para trás. Volte 2 casas.", {"mov": -2}, "smith"), # EFEITO MUDADO
    ("O Merovíngio te intercepta. 'Causalidade. Ação e reação.' Ele te atrasa. Volte 3 casas.", {"mov": -3}, "merovingio"),
    ("Os Gêmeos do Merovíngio te encurralam. Você se esconde e espera eles passarem, perdendo terreno. Volte 3 casas.", {"mov": -3}, "gemeos"), # EFEITO MUDADO
    ("Smith te surpreende. 'Só há uma verdade real: a casualidade.' Volte para o início da fileira onde você está.", {"voltar_inicio_fileira": True}, "smith"),
    ("O Arquiteto detecta sua anomalia. 'A esperança é a quintessência da ilusão humana.' Ele te recalcula. Volte 6 casas.", {"mov": -6}, "arquiteto"),
    ("Déjà vu... um gato preto passa, e depois de novo. O sistema está sendo alterado. Volte para onde estava antes de jogar o dado.", {"voltar_turno": True}, None),
    ("Agentes múltiplos convergem na sua posição. Você é forçado a recuar para se esconder. Volte 4 casas.", {"mov": -4}, "smith") # EFEITO MUDADO
]

mensagem_carta = None
personagem_carta = None
carta_atual = None
aguardando_carta = False

def puxar_carta():
    global mensagem_carta, carta_atual, aguardando_carta, personagem_carta
    carta_atual = random.choice(cartas)
    mensagem_carta = carta_atual[0]
    personagem_carta = carta_atual[2]
    aguardando_carta = True

def aplicar_carta(peao, carta):
    efeitos = carta[1]
    is_negativa = efeitos.get("mov", 0) < 0 or "voltar_turno" in efeitos or "voltar_inicio_fileira" in efeitos
    
    if peao["ignorar_proxima_negativa"] and is_negativa:
        peao["ignorar_proxima_negativa"] = False
        return {} 
    
    return efeitos


pilula_final_destino = {}

def sortear_pilulas_final():
    global pilula_final_destino
    opcoes = ["sair", "voltar"]
    random.shuffle(opcoes)
    pilula_final_destino = {0: opcoes[0], 1: opcoes[1]} 

def is_escolha_pilula_final(pos):
    return pos >= NUM_CASAS - 1

def aplicar_escolha_pilula_final(escolha):
    return pilula_final_destino.get(escolha)


def jogar_vez(peao):
    peao["pos_anterior"] = peao["pos"]
    dado = random.randint(1, 6)
    peao["dado"] = dado
    return dado

def avancar_turno(replay=False):
    global jogador_atual
    if not replay:
        jogador_atual = (jogador_atual + 1) % len(peoes)
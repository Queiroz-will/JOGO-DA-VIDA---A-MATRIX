# main.py (Atualizado com "Buff do Neo" e Animação "Sem Teleporte")
# ## MUDANÇA: Corrigido Lag do Loading + Adicionado Nomes nos Peões
# ## MUDANÇA: Corrigida Música tocando sobre a Cutscene

import pygame
import sys
import os
import random 
from utils import (
    desenhar_texto, desenhar_botao, desenhar_janela_central, MatrixRain,
    BRANCO, PRETO, VERDE, VERMELHO, AZUL, AMARELO, CINZA,
    VERDE_MATRIX, PRETO_MATRIX, desenhar_texto_formatado
)
import jogo

pygame.init()
pygame.mixer.init() 

# ----------------------------
# Configurações da tela (Iniciais)
# ----------------------------
LARGURA, ALTURA = 1440, 900
TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Jogo da Vida - A Matrix (Carregando...)")

# =====================================================================================
# ## <<< NOVO: TELA DE LOADING
# =====================================================================================

# Carrega APENAS as fontes necessárias para o loading
try:
    fonte_loading_titulo = pygame.font.SysFont("arialblack", 40)
    fonte_loading_rain = pygame.font.SysFont("consolas", 20)
except:
    fonte_loading_titulo = pygame.font.SysFont(None, 50) # Fallback
    fonte_loading_rain = pygame.font.SysFont(None, 22)  # Fallback

# Classe de chuva de 0s e 1s (versão simplificada para o loading)
class LoadingRain:
    def __init__(self, largura, altura, fonte):
        self.largura = largura
        self.altura = altura
        self.fonte = fonte
        self.tam_fonte_w = fonte.size("0")[0]
        self.tam_fonte_h = fonte.get_height()
        self.colunas = max(1, largura // self.tam_fonte_w)
        self.y_pos = [random.randint(-200, 0) for _ in range(self.colunas)]
        self.vel = [random.randint(2, 6) for _ in range(self.colunas)]
        self.caracteres = ['0', '1']

    # Removido o "fade" que causava lag
    def desenhar(self, tela):
        cor_verde = (0, 255, 70)
        
        for i in range(self.colunas):
            char = random.choice(self.caracteres)
            try:
                surf = self.fonte.render(char, True, cor_verde)
            except:
                surf = pygame.font.SysFont(None, 22).render(char, True, cor_verde)
                
            x = i * self.tam_fonte_w
            y = self.y_pos[i]
            
            if 0 <= y <= self.altura:
                tela.blit(surf, (x, y))
                
            self.y_pos[i] = self.y_pos[i] + self.vel[i]
            
            if self.y_pos[i] > self.altura:
                self.y_pos[i] = random.randint(-100, 0)

# Função de loading agora limpa a tela (rápido)
def desenhar_tela_loading(progresso, total, rain_effect):
    # 1. Limpa a tela
    TELA.fill(PRETO_MATRIX)
    
    # 2. Desenha a chuva de 0s e 1s
    rain_effect.desenhar(TELA)
    
    # 3. Desenha o texto central
    texto_surf = fonte_loading_titulo.render("ENTRANDO NA MATRIX, PREPARE-SE", True, BRANCO)
    texto_rect = texto_surf.get_rect(center=(LARGURA // 2, ALTURA // 2))
    TELA.blit(texto_surf, texto_rect)

    # 4. Desenha a barra de progresso
    bar_w = LARGURA * 0.6
    bar_h = 30
    bar_x = LARGURA // 2 - bar_w // 2
    bar_y = ALTURA * 0.75
    
    percent = progresso / total
    current_w = max(0, bar_w * percent)
    
    # Fundo da barra
    pygame.draw.rect(TELA, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=5)
    # Barra de progresso
    pygame.draw.rect(TELA, VERDE_MATRIX, (bar_x, bar_y, current_w, bar_h), border_radius=5)
    # Contorno
    pygame.draw.rect(TELA, BRANCO, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=5)
    
    pygame.display.flip()

# Todas as variáveis de assets são pré-declaradas
# Fontes
fonte = None
fonte_titulo = None
fonte_subtitulo = None
fonte_botao = None
fonte_mono = None
fonte_prologo = None
fonte_peao_nome = None 
# Sons
VOLUME_GERAL = 1.0  
VOLUME_MUSICA = 0.5 
VOLUME_EFEITOS = 0.5 
click_sound = None
move_sound = None
dice_roll_sound = None
falha_sound = None
splash_sound = None
cutscene_sound = None
# Sprites
personagem_sprites = {}
selecao_sprites = {}
peao_sprites = {}
splash_frames = []
cutscene_frames = [] 
regras_bg_sprite = None 
personagens_nomes_cartas = ["neo", "trinity", "morpheus", "oraculo", "operador", "smith", "merovingio", "gemeos", "arquiteto"]
DADO_TAMANHO = (180, 180)
dice_roll_sprites = []
dice_result_sprites = {}

# Função "Generator" para carregar tudo
def carregar_assets():
    global fonte, fonte_titulo, fonte_subtitulo, fonte_botao, fonte_mono, fonte_prologo, fonte_peao_nome
    global click_sound, move_sound, dice_roll_sound, falha_sound, splash_sound, cutscene_sound
    global personagem_sprites, selecao_sprites, peao_sprites, splash_frames, cutscene_frames, regras_bg_sprite
    global dice_roll_sprites, dice_result_sprites

    # Contagem total de assets para a barra de progresso
    total_assets = 7 + 7 + len(personagens_nomes_cartas) + (4*2) + 1 + (6*2) + 188 + 171 
    progresso = 0

    # ----------------------------
    # 1. Fontes
    # ----------------------------
    fonte = pygame.font.SysFont("arial", 28)
    progresso += 1; yield progresso, total_assets
    fonte_titulo = pygame.font.SysFont("arialblack", 70)
    progresso += 1; yield progresso, total_assets
    fonte_subtitulo = pygame.font.SysFont("arialblack", 40)
    progresso += 1; yield progresso, total_assets
    fonte_botao = pygame.font.SysFont("arialblack", 30)
    progresso += 1; yield progresso, total_assets
    fonte_mono = pygame.font.SysFont("consolas", 22)
    progresso += 1; yield progresso, total_assets
    fonte_prologo = pygame.font.SysFont("arialblack", 36)
    progresso += 1; yield progresso, total_assets
    fonte_peao_nome = pygame.font.SysFont("arial", 18, bold=True) 
    progresso += 1; yield progresso, total_assets

    # ----------------------------
    # 2. Sons
    # ----------------------------
    pygame.mixer.music.set_volume(VOLUME_GERAL * VOLUME_MUSICA)
    try:
        pygame.mixer.music.load(os.path.join("assets", "musica_menu.mp3"))
    except Exception as e: print(f"⚠️ Música de menu não encontrada: {e}")
    progresso += 1; yield progresso, total_assets

    try:
        click_sound = pygame.mixer.Sound(os.path.join("assets", "click.wav"))
        click_sound.set_volume(VOLUME_GERAL * VOLUME_EFEITOS)
    except Exception as e: print(f"⚠️ Som de clique não encontrado: {e}")
    progresso += 1; yield progresso, total_assets

    try:
        move_sound = pygame.mixer.Sound(os.path.join("assets", "move.wav"))
        move_sound.set_volume(VOLUME_GERAL * VOLUME_EFEITOS)
    except: move_sound = None
    progresso += 1; yield progresso, total_assets

    try:
        dice_roll_sound = pygame.mixer.Sound(os.path.join("assets", "dados.mp3"))
        dice_roll_sound.set_volume(VOLUME_GERAL * VOLUME_EFEITOS)
    except Exception as e: print(f"⚠️ Som 'dados.mp3' não encontrado: {e}")
    progresso += 1; yield progresso, total_assets

    try:
        falha_sound = pygame.mixer.Sound(os.path.join("assets", "falha.mp3"))
        falha_sound.set_volume(VOLUME_GERAL * VOLUME_EFEITOS)
    except Exception as e: print(f"⚠️ Som 'falha.mp3' não encontrado: {e}")
    progresso += 1; yield progresso, total_assets

    try:
        splash_sound = pygame.mixer.Sound(os.path.join("assets", "splash.mp3"))
        splash_sound.set_volume(VOLUME_GERAL * VOLUME_EFEITOS)
    except Exception as e: print(f"⚠️ Som 'splash.mp3' não encontrado: {e}")
    progresso += 1; yield progresso, total_assets

    try:
        cutscene_sound = pygame.mixer.Sound(os.path.join("assets", "cutcine.mp3"))
        cutscene_sound.set_volume(VOLUME_GERAL * VOLUME_EFEITOS)
    except Exception as e: print(f"⚠️ Som 'cutcine.mp3' não encontrado: {e}")
    progresso += 1; yield progresso, total_assets
    
    # ----------------------------
    # 3. Carregamento de Sprites
    # ----------------------------
    for nome in personagens_nomes_cartas:
        try:
            imagem = pygame.image.load(os.path.join("assets", "images", f"{nome}.png")).convert_alpha()
            personagem_sprites[nome] = pygame.transform.scale(imagem, (100, 100))
        except Exception as e: print(f"⚠️ Sprite de carta '{nome}' não encontrada: {e}")
        progresso += 1; yield progresso, total_assets

    for i in range(1, 5):
        try:
            img_selecao = pygame.image.load(os.path.join("assets", "images", f"programador_{i}.png")).convert_alpha()
            selecao_sprites[i] = pygame.transform.scale(img_selecao, (150, 150))
            progresso += 1; yield progresso, total_assets
            
            peao_sprites[i] = pygame.image.load(os.path.join("assets", "personagens", f"programador_{i}.png")).convert_alpha()
            progresso += 1; yield progresso, total_assets
        except Exception as e: print(f"⚠️ Sprite do programador {i} não encontrada: {e}")

    print("Carregando splash (188 frames)...")
    for i in range(1, 189): # De 0001.png até 0188.png
        try:
            img = pygame.image.load(os.path.join("assets", "frames_splash", f"{i:04d}.png")).convert_alpha()
            splash_frames.append(img)
        except Exception as e: print(f"⚠️ Frame do Splash '{i:04d}.png' não encontrado: {e}")
        
        if i % 5 == 0:
            progresso += 5
            yield progresso, total_assets
    progresso += 188 % 5 
    yield progresso, total_assets
    print("Splash carregado.")

    try:
        regras_bg_sprite = pygame.image.load(os.path.join("assets", "images", "regras_bg.png")).convert_alpha()
    except Exception as e: print(f"⚠️ Imagem 'regras_bg.png' não encontrada: {e}")
    progresso += 1; yield progresso, total_assets

    for i in range(1, 7): 
        try:
            img = pygame.image.load(os.path.join("assets", "dados", f"ROLL_{i:02d}.png")).convert_alpha()
            dice_roll_sprites.append(pygame.transform.scale(img, DADO_TAMANHO))
        except Exception as e: print(f"⚠️ Sprite de dado 'ROLL_{i:02d}.png' não encontrada: {e}")
        progresso += 1; yield progresso, total_assets

    for i in range(1, 7): 
        try:
            img = pygame.image.load(os.path.join("assets", "dados", f"DADO_{i}.png")).convert_alpha()
            dice_result_sprites[i] = pygame.transform.scale(img, DADO_TAMANHO)
        except Exception as e: print(f"⚠️ Sprite de dado 'DADO_{i}.png' não encontrada: {e}")
        progresso += 1; yield progresso, total_assets

    print("Carregando cutscene (171 frames)... Isso pode levar um momento.")
    for i in range(1, 172): # De 0001.png até 0171.png
        try:
            img = pygame.image.load(os.path.join("assets", "frames_cutscene", f"{i:04d}.png")).convert_alpha()
            cutscene_frames.append(img)
        except Exception as e: print(f"⚠️ Frame da Cutscene '{i:04d}.png' não encontrado: {e}")
        
        if i % 5 == 0:
            progresso += 5
            yield progresso, total_assets
    progresso += 171 % 5 
    yield progresso, total_assets
    print("Cutscene carregada.")

# =====================================================================================
# ## <<< NOVO: LOOP DE LOADING (LÓGICA)
# =====================================================================================

loading_rain_effect = LoadingRain(LARGURA, ALTURA, fonte_loading_rain)
asset_loader = carregar_assets() 
carregando = True
progresso_atual = 0
total_assets = 1 

TELA.fill(PRETO_MATRIX)
desenhar_tela_loading(0, 1, loading_rain_effect)

while carregando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    try:
        resultado = next(asset_loader)
        progresso_atual, total_assets = resultado
    except StopIteration:
        carregando = False
        progresso_atual = total_assets
    
    desenhar_tela_loading(progresso_atual, total_assets, loading_rain_effect)
    pygame.time.delay(1) 

# =====================================================================================
# ## <<< FIM DO LOADING: O JOGO COMEÇA AQUI
# =====================================================================================

# ----------------------------
# Inicialização do Jogo
# ----------------------------
pygame.display.set_caption("Jogo da Vida - A Matrix") 
jogo.criar_tabuleiro(LARGURA, ALTURA) 
jogo.criar_jogadores(num_jogadores=2) 
rain_effect = MatrixRain(LARGURA, ALTURA, fonte_mono) 

# ----------------------------
# Estados do Jogo
# ----------------------------
SPLASH_SCREEN = "splash_screen"
MENU = "menu"
OPCOES = "opcoes"
QTD_JOGADORES = "qtd_jogadores"
NOME = "nome"
SELECAO_PERSONAGEM = "selecao_personagem"
PROLOGO = "prologo"
CUTSCENE = "cutscene" 
REGRAS = "regras"
JOGO = "jogo"
PILULA_FINAL = "pilula_final"
PILULA_FALHA = "pilula_falha"
FIM = "fim"
PAUSA = "pausa" 
MOSTRAR_BUFF = "mostrar_buff" 
estado = SPLASH_SCREEN 

# Variáveis de controle
nomes = ["", "", "", ""]
foco_jogador = 0
cursor_on = True
cursor_timer = 0
num_jogadores = 2
jogador_selecionando = 0
personagens_escolhidos = []
estado_anterior_opcoes = None 
jogador_com_buff = None 
pilula_final_peao = None 

# Variáveis para o Prólogo "Star Wars"
prologo_scroll_y = ALTURA
PROLOGO_SCROLL_SPEED = 0.85 
PROLOGO_LINES = [] 

# Variáveis para o Epílogo "Star Wars"
epilogo_scroll_y = ALTURA
EPILOGO_SCROLL_SPEED = 0.85 
EPILOGO_LINES = []
fim_scroll_acabou = False 

# Variáveis para o sistema de animação
animacao_em_andamento = False
peao_animando = None
passos_restantes = 0
passos_direcao = 1 
o_que_fazer_depois_anim = None 
animacao_replay = False 
timer_animacao = 0
TEMPO_PASSO = 100 
frame_atual = 0 
timer_frame = 0 
TEMPO_FRAME = 200

# Variáveis de controle para Splash
splash_frame_atual = 0
splash_timer_frame = 0
TEMPO_FRAME_SPLASH = 1000 // 24 # 24fps
splash_anim_concluida = False
splash_som_iniciado = False

# Variáveis para a Cutscene
cutscene_frame_atual = 0
cutscene_timer_frame = 0
TEMPO_FRAME_CUTSCENE = 1000 // 24 # 24fps
cutscene_som_iniciado = False

# Variáveis de controle para Animação de Dado
estado_anim_dado = "nenhum" 
timer_anim_dado = 0
dado_frame_atual = 0 
dado_frame_timer = 0
dado_resultado_sorteado = 0
DURACAO_ANIM_DADO = 1000   
DURACAO_MOSTRAR_DADO = 1000 
TEMPO_FRAME_DADO = 50      

# Definição das áreas dos botões
rects_botoes_menu = {}
rects_botoes_opcoes = {}
rects_botoes_qtd = {}
rects_botoes_nome = {}
rects_botoes_selecao = {}
rects_botoes_pilula = {}
rects_botoes_pausa = {} 
rects_botoes_prologo = {} 
rects_botoes_regras = {}
rects_botoes_fim = {} 

# =====================================================================================
# FUNÇÕES DE DESENHO DE TELA
# =====================================================================================

def desenhar_splash_screen():
    TELA.fill(PRETO_MATRIX)
    
    if splash_frames and splash_frame_atual < len(splash_frames): 
        frame_original = splash_frames[splash_frame_atual]
        frame_esticado = pygame.transform.scale(frame_original, (LARGURA, ALTURA))
        TELA.blit(frame_esticado, (0, 0))
    
    elif not splash_frames: 
        desenhar_texto(TELA, "JOGO DA VIDA - A MATRIX", LARGURA//2, ALTURA//2 - 50, BRANCO, True, fonte_titulo)
        desenhar_texto(TELA, "APERTE QUALQUER TECLA PARA COMEÇAR", LARGURA//2, ALTURA - 100, BRANCO, True, fonte_botao)
    
    if splash_anim_concluida:
        desenhar_texto(TELA, "Jogo da Vida - A Matrix", LARGURA//2, ALTURA * 0.2, BRANCO, True, fonte_titulo)
        desenhar_texto(TELA, "APERTE QUALQUER TECLA PARA COMEÇAR", LARGURA//2, ALTURA - 100, BRANCO, True, fonte_botao)

def desenhar_menu():
    global rects_botoes_menu
    rects_botoes_menu = {} 
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_texto(TELA, "Jogo da Vida - A Matrix", LARGURA//2, ALTURA * 0.15, VERDE_MATRIX, True, fonte_titulo)
    btn_w, btn_h = 300, 70
    btn_x = LARGURA // 2 - btn_w // 2
    y_start = ALTURA * 0.4
    desenhar_botao(TELA, "Iniciar Jogo", btn_x, y_start, btn_w, btn_h, (10,40,10), (20,80,20), fonte_botao)
    rects_botoes_menu["iniciar"] = pygame.Rect(btn_x, y_start, btn_w, btn_h)
    desenhar_botao(TELA, "Opções", btn_x, y_start + btn_h + 30, btn_w, btn_h, (10,10,40), (20,20,80), fonte_botao)
    rects_botoes_menu["opcoes"] = pygame.Rect(btn_x, y_start + btn_h + 30, btn_w, btn_h)
    desenhar_botao(TELA, "Sair", btn_x, y_start + 2 * (btn_h + 30), btn_w, btn_h, (40,10,10), (80,20,20), fonte_botao)
    rects_botoes_menu["sair"] = pygame.Rect(btn_x, y_start + 2 * (btn_h + 30), btn_w, btn_h)

def desenhar_opcoes():
    global rects_botoes_opcoes
    rects_botoes_opcoes = {}
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_texto(TELA, "Opções", LARGURA//2, ALTURA * 0.1, VERDE_MATRIX, True, fonte_titulo)
    btn_vol_size = 50 
    y_start = ALTURA * 0.22
    desenhar_texto(TELA, "Volume Geral", LARGURA//2, y_start, BRANCO, True, fonte_botao)
    desenhar_botao(TELA, "-", LARGURA//2 - 120, y_start + 40, btn_vol_size, btn_vol_size, (40,40,40), (80,80,80), fonte_botao)
    rects_botoes_opcoes["geral-"] = pygame.Rect(LARGURA//2 - 120, y_start + 40, btn_vol_size, btn_vol_size)
    desenhar_texto(TELA, f"{int(VOLUME_GERAL*100)}%", LARGURA//2, y_start + 65, BRANCO, True, fonte_botao)
    desenhar_botao(TELA, "+", LARGURA//2 + 70, y_start + 40, btn_vol_size, btn_vol_size, (40,40,40), (80,80,80), fonte_botao)
    rects_botoes_opcoes["geral+"] = pygame.Rect(LARGURA//2 + 70, y_start + 40, btn_vol_size, btn_vol_size)
    y_start += 110 
    desenhar_texto(TELA, "Música", LARGURA//2, y_start, BRANCO, True, fonte_botao)
    desenhar_botao(TELA, "-", LARGURA//2 - 120, y_start + 40, btn_vol_size, btn_vol_size, (40,40,40), (80,80,80), fonte_botao)
    rects_botoes_opcoes["musica-"] = pygame.Rect(LARGURA//2 - 120, y_start + 40, btn_vol_size, btn_vol_size)
    desenhar_texto(TELA, f"{int(VOLUME_MUSICA*100)}%", LARGURA//2, y_start + 65, BRANCO, True, fonte_botao)
    desenhar_botao(TELA, "+", LARGURA//2 + 70, y_start + 40, btn_vol_size, btn_vol_size, (40,40,40), (80,80,80), fonte_botao)
    rects_botoes_opcoes["musica+"] = pygame.Rect(LARGURA//2 + 70, y_start + 40, btn_vol_size, btn_vol_size)
    y_start += 110 
    desenhar_texto(TELA, "Efeitos Sonoros", LARGURA//2, y_start, BRANCO, True, fonte_botao)
    desenhar_botao(TELA, "-", LARGURA//2 - 120, y_start + 40, btn_vol_size, btn_vol_size, (40,40,40), (80,80,80), fonte_botao)
    rects_botoes_opcoes["efeitos-"] = pygame.Rect(LARGURA//2 - 120, y_start + 40, btn_vol_size, btn_vol_size)
    desenhar_texto(TELA, f"{int(VOLUME_EFEITOS*100)}%", LARGURA//2, y_start + 65, BRANCO, True, fonte_botao)
    desenhar_botao(TELA, "+", LARGURA//2 + 70, y_start + 40, btn_vol_size, btn_vol_size, (40,40,40), (80,80,80), fonte_botao)
    rects_botoes_opcoes["efeitos+"] = pygame.Rect(LARGURA//2 + 70, y_start + 40, btn_vol_size, btn_vol_size)
    res_y_label = y_start + 110
    res_y_btn1 = res_y_label + 50
    btn_res_w, btn_res_h = 300, 50 
    btn_res_x = LARGURA // 2 - btn_res_w // 2
    desenhar_texto(TELA, "Resolução", LARGURA//2, res_y_label, BRANCO, True, fonte_botao)
    desenhar_botao(TELA, "1280 x 720", btn_res_x, res_y_btn1, btn_res_w, btn_res_h, (40,40,40), (80,80,80), fonte_botao)
    rects_botoes_opcoes["res1"] = pygame.Rect(btn_res_x, res_y_btn1, btn_res_w, btn_res_h)
    desenhar_botao(TELA, "1440 x 900", btn_res_x, res_y_btn1 + btn_res_h + 10, btn_res_w, btn_res_h, (40,40,40), (80,80,80), fonte_botao)
    rects_botoes_opcoes["res2"] = pygame.Rect(btn_res_x, res_y_btn1 + btn_res_h + 10, btn_res_w, btn_res_h)
    desenhar_botao(TELA, "Tela Cheia", btn_res_x, res_y_btn1 + 2*(btn_res_h + 10), btn_res_w, btn_res_h, (40,40,40), (80,80,80), fonte_botao)
    rects_botoes_opcoes["resFull"] = pygame.Rect(btn_res_x, res_y_btn1 + 2*(btn_res_h + 10), btn_res_w, btn_res_h)
    btn_voltar_w, btn_voltar_h = 400, 60 
    texto_voltar = "Voltar à Pausa" if estado_anterior_opcoes == PAUSA else "Voltar ao Menu"
    desenhar_botao(TELA, texto_voltar, LARGURA//2 - btn_voltar_w//2, ALTURA - 80, btn_voltar_w, btn_voltar_h, (40,10,10), (80,20,20), fonte_botao)
    rects_botoes_opcoes["voltar"] = pygame.Rect(LARGURA//2 - btn_voltar_w//2, ALTURA - 80, btn_voltar_w, btn_voltar_h)

def desenhar_qtd_jogadores():
    global num_jogadores, nomes, rects_botoes_qtd
    rects_botoes_qtd = {}
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_texto(TELA, "Quantidade de Programadores", LARGURA//2, ALTURA * 0.15, VERDE_MATRIX, True, fonte_titulo)
    btn_size = 100
    spacing = 20
    total_width = 3 * btn_size + 2 * spacing
    start_x = LARGURA//2 - total_width // 2
    y_pos = ALTURA * 0.4
    for i in range(2, 5):
        x_pos = start_x + (i - 2) * (btn_size + spacing)
        desenhar_botao(TELA, str(i), x_pos, y_pos, btn_size, btn_size, (10,40,10), (20,80,20), fonte_botao)
        rects_botoes_qtd[i] = pygame.Rect(x_pos, y_pos, btn_size, btn_size)

def desenhar_nome():
    global cursor_on, cursor_timer, foco_jogador, nomes, rects_botoes_nome
    rects_botoes_nome = {}
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_texto(TELA, "Identifiquem-se, Programadores", LARGURA//2, ALTURA * 0.15, VERDE_MATRIX, True, fonte_titulo)
    cursor_timer += 1
    if cursor_timer > 25: cursor_on = not cursor_on; cursor_timer = 0
    teclas_legenda = ["A", "G", "J", "L"]
    campo_w, campo_h = LARGURA * 0.4, 70 
    campos_y = ALTURA * 0.3
    for i in range(num_jogadores):
        x = LARGURA//2 - campo_w//2
        y = campos_y + i*(campo_h + 16)
        pygame.draw.rect(TELA, (5,25,5), (x, y, campo_w, campo_h), border_radius=8)
        pygame.draw.rect(TELA, VERDE_MATRIX, (x, y, campo_w, campo_h), 2, border_radius=8)
        texto = nomes[i] + ("_" if cursor_on and foco_jogador == i else "")
        desenhar_texto(TELA, f"Programador {i+1} (tecla: {teclas_legenda[i]}): {texto}", x+12, y + campo_h//2 - 14, VERDE_MATRIX, False, fonte_mono)
    btn_w, btn_h = 300, 70
    btn_y = campos_y + num_jogadores*(campo_h + 16) + 30
    desenhar_botao(TELA, "Confirmar Nomes", LARGURA//2 - btn_w//2, btn_y, btn_w, btn_h, (10,40,10), (20,80,20), fonte_botao)
    rects_botoes_nome["confirmar"] = pygame.Rect(LARGURA//2 - btn_w//2, btn_y, btn_w, btn_h)

def desenhar_selecao_personagem():
    global jogador_selecionando, personagens_escolhidos, rects_botoes_selecao
    rects_botoes_selecao = {}
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    nome_jogador = jogo.peoes[jogador_selecionando]['nome']
    desenhar_texto(TELA, f"{nome_jogador}, escolha seu avatar:", LARGURA//2, ALTURA * 0.15, VERDE_MATRIX, True, fonte_titulo)
    num_chars = len(selecao_sprites)
    sprite_w, sprite_h = 150, 150
    spacing = 30
    total_w = num_chars * sprite_w + (num_chars - 1) * spacing
    start_x = LARGURA//2 - total_w//2
    y_pos = ALTURA//2 - sprite_h//2
    for i in range(1, num_chars + 1):
        x = start_x + (i - 1) * (sprite_w + spacing)
        sprite = selecao_sprites[i]
        rect = sprite.get_rect(topleft=(x, y_pos))
        rects_botoes_selecao[i] = rect
        mouse_pos = pygame.mouse.get_pos()
        if i in personagens_escolhidos:
            surf = pygame.Surface(rect.size, pygame.SRCALPHA); surf.fill((50, 50, 50, 180)); TELA.blit(sprite, rect); TELA.blit(surf, rect)
            desenhar_texto(TELA, "Escolhido", rect.centerx, rect.bottom + 20, CINZA, True, fonte)
        else:
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(TELA, VERDE_MATRIX, (rect.x-5, rect.y-5, rect.w+10, rect.h+10), 3, border_radius=8)
            TELA.blit(sprite, rect)

def desenhar_prologo():
    global rects_botoes_prologo, prologo_scroll_y, PROLOGO_LINES
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    rects_botoes_prologo = {} 
    if not PROLOGO_LINES:
        prologo_scroll_y = ALTURA + 50 
        max_width = LARGURA * 0.8 
        for pagina in jogo.PAGINAS_DA_LORE:
            paragrafos = pagina.split('\n\n') 
            for paragrafo in paragrafos:
                palavras = paragrafo.replace('\n', ' ').split(' ')
                linha_atual = ""
                for palavra in palavras:
                    linha_teste = linha_atual + palavra + " "
                    if fonte_prologo.size(linha_teste)[0] < max_width:
                        linha_atual = linha_teste
                    else:
                        PROLOGO_LINES.append(linha_atual)
                        linha_atual = palavra + " "
                PROLOGO_LINES.append(linha_atual) 
                PROLOGO_LINES.append("") 
    line_height = fonte_prologo.get_linesize()
    for i, line in enumerate(PROLOGO_LINES):
        y_pos = prologo_scroll_y + (i * line_height)
        if y_pos < ALTURA and y_pos > -line_height:
            desenhar_texto(TELA, line, LARGURA // 2, y_pos, AMARELO, True, fonte_prologo)
    btn_w, btn_h = 150, 60
    btn_x, btn_y = LARGURA - btn_w - 20, ALTURA - btn_h - 20
    desenhar_botao(TELA, "Pular", btn_x, btn_y, btn_w, btn_h, (40,10,10), (80,20,20), fonte_botao)
    rects_botoes_prologo["pular"] = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
    posicao_final_texto = prologo_scroll_y + (len(PROLOGO_LINES) * line_height)
    return posicao_final_texto

def desenhar_cutscene():
    TELA.fill(PRETO_MATRIX) 
    if cutscene_frames and cutscene_frame_atual < len(cutscene_frames):
        frame_original = cutscene_frames[cutscene_frame_atual]
        frame_esticado = pygame.transform.scale(frame_original, (LARGURA, ALTURA))
        TELA.blit(frame_esticado, (0, 0))
    else:
        desenhar_texto(TELA, "Carregando...", LARGURA//2, ALTURA//2, BRANCO, True, fonte)

def desenhar_regras():
    global rects_botoes_regras
    rects_botoes_regras = {}
    if regras_bg_sprite:
        TELA.blit(pygame.transform.scale(regras_bg_sprite, (LARGURA, ALTURA)), (0, 0))
    else:
        TELA.fill(PRETO_MATRIX) 
        rain_effect.update_and_draw(TELA)
    regras = ("1. Use sua tecla (A, G, J, L) para jogar o dado na sua vez.\n\n"
              "2. O peão se moverá casa por casa. Após parar, a carta do local será revelada.\n\n"
              "3. Siga as instruções das cartas para avançar ou recuar.\n\n"
              "4. O objetivo é chegar à 'Saída' e fazer a escolha final correta para escapar da Matrix.")
    desenhar_janela_central(TELA, LARGURA * 0.8, ALTURA * 0.6, (10,25,10), VERDE_MATRIX, "REGRAS", regras, fonte_subtitulo, fonte)
    btn_w, btn_h = 400, 70
    btn_x = LARGURA // 2 - btn_w // 2
    btn_y = ALTURA - 100
    desenhar_botao(TELA, "Iniciar Fuga da Matrix", btn_x, btn_y, btn_w, btn_h, (10,40,10), (20,80,20), fonte_botao)
    rects_botoes_regras["iniciar"] = pygame.Rect(btn_x, btn_y, btn_w, btn_h)

def desenhar_tabuleiro():
    for idx, (x, y) in enumerate(jogo.CASAS):
        pygame.draw.rect(TELA, (0, 30, 0), (x, y, jogo.CASA_TAM, jogo.CASA_TAM), border_radius=4)
        pygame.draw.rect(TELA, (0, 80, 0), (x, y, jogo.CASA_TAM, jogo.CASA_TAM), 2, border_radius=4)
        if idx == 0: desenhar_texto(TELA, "Início", x + jogo.CASA_TAM//2, y + jogo.CASA_TAM//2, VERDE_MATRIX, True, fonte)
        elif idx == jogo.NUM_CASAS - 1: desenhar_texto(TELA, "Saída", x + jogo.CASA_TAM//2, y + jogo.CASA_TAM//2, VERDE_MATRIX, True, fonte)

def desenhar_linhas_tabuleiro():
    COR_LINHA = (0, 100, 0)
    for i in range(len(jogo.CASAS) - 1):
        x1, y1 = jogo.CASAS[i]
        x2, y2 = jogo.CASAS[i+1]
        centro1 = (x1 + jogo.CASA_TAM // 2, y1 + jogo.CASA_TAM // 2)
        centro2 = (x2 + jogo.CASA_TAM // 2, y2 + jogo.CASA_TAM // 2)
        pygame.draw.line(TELA, COR_LINHA, centro1, centro2, width=5)

def desenhar_hud():
    y0 = 20
    teclas_legenda = ["A", "G", "J", "L"]
    for i, p in enumerate(jogo.peoes):
        cor = AMARELO if i == jogo.jogador_atual else VERDE_MATRIX
        desenhar_texto(TELA, f"{p['nome']} [{teclas_legenda[i]}] - Casa: {p['pos']+1}", 30, y0 + i*30, cor, False, fonte_mono)
    jogador_da_vez = jogo.peoes[jogo.jogador_atual]
    desenhar_texto(TELA, f"Vez de: {jogador_da_vez['nome']}", LARGURA - 250, 20, AMARELO, True, fonte_mono)
    if "dado" in jogador_da_vez and jogador_da_vez['dado'] > 0 and estado_anim_dado == "nenhum":
        desenhar_texto(TELA, f"Dado rolado: {jogador_da_vez['dado']}", LARGURA - 250, 50, BRANCO, True, fonte_mono)

# Função de desenhar o jogo agora inclui os NOMES
def desenhar_jogo():
    global frame_atual, timer_frame
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_tabuleiro()
    desenhar_linhas_tabuleiro()
    
    # Animação dos sprites dos peões
    timer_frame += clock.get_time()
    if timer_frame > TEMPO_FRAME:
        timer_frame = 0; frame_atual = (frame_atual + 1) % 2
        
    # Desenha os peões e seus nomes
    for i, p in enumerate(jogo.peoes):
        char_id = p.get("personagem_id")
        idx = min(p["pos"], len(jogo.CASAS)-1)
        x, y = jogo.CASAS[idx]
        
        if char_id in peao_sprites:
            spritesheet = peao_sprites[char_id]
            frame_width = spritesheet.get_width() // 2
            frame_rect = pygame.Rect(frame_width * frame_atual, 0, frame_width, spritesheet.get_height())
            peao_img = spritesheet.subsurface(frame_rect)
            peao_img_redimensionada = pygame.transform.scale(peao_img, (65, 65))
            peao_rect = peao_img_redimensionada.get_rect(center=(x + jogo.CASA_TAM//2, y + jogo.CASA_TAM//2))
            
            TELA.blit(peao_img_redimensionada, peao_rect)
            
            # Desenha o nome do jogador acima do sprite
            nome_jogador = p['nome']
            nome_x = peao_rect.centerx
            nome_y = peao_rect.top - 10 # 10 pixels acima
            desenhar_texto(TELA, nome_jogador, nome_x, nome_y, BRANCO, True, fonte_peao_nome)
            
        else:
            # Fallback (círculo), também com nome
            offset = (i - (num_jogadores-1)/2) * 15
            circ_x = x + jogo.CASA_TAM//2 + offset
            circ_y = y + jogo.CASA_TAM//2
            pygame.draw.circle(TELA, p["cor"], (circ_x, circ_y), 20)
            
            # Desenha o nome do jogador acima do círculo
            nome_jogador = p['nome']
            nome_x = circ_x
            nome_y = circ_y - 30 # 10 pixels acima do raio de 20
            desenhar_texto(TELA, nome_jogador, nome_x, nome_y, BRANCO, True, fonte_peao_nome)

    desenhar_hud()
    
    # Desenha a janela da carta
    if jogo.mensagem_carta:
        w, h = LARGURA * 0.7, 350
        cx, cy = LARGURA // 2, ALTURA // 2
        ret_fundo = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
        pygame.draw.rect(TELA, (10, 25, 10), ret_fundo, border_radius=8)
        pygame.draw.rect(TELA, VERDE_MATRIX, ret_fundo, 3, border_radius=8)
        titulo = ">>> TRANSMISSÃO RECEBIDA <<<"
        desenhar_texto(TELA, titulo, cx, ret_fundo.top + 30, VERDE_MATRIX, True, fonte_subtitulo)
        y_pos_sprite = ret_fundo.top + 80
        if jogo.personagem_carta and jogo.personagem_carta in personagem_sprites:
            sprite = personagem_sprites[jogo.personagem_carta]
            sprite_rect = sprite.get_rect(center=(cx, y_pos_sprite + sprite.get_height()//2 - 20))
            TELA.blit(sprite, sprite_rect); y_pos_texto = sprite_rect.bottom + 10
        else: y_pos_texto = y_pos_sprite
        padding = 40; ret_texto = pygame.Rect(ret_fundo.left + padding, y_pos_texto, w - padding*2, h - (y_pos_texto - ret_fundo.top) - 60)
        desenhar_texto_formatado(TELA, jogo.mensagem_carta, BRANCO, ret_texto, fonte)
        if jogo.aguardando_carta:
            tecla_str = pygame.key.name(jogo.peoes[jogo.jogador_atual]['tecla']).upper()
            desenhar_texto(TELA, f"Pressione sua tecla ({tecla_str}) para continuar!", cx, ret_fundo.bottom - 30, AMARELO, True, fonte)
            
    # Desenha a animação do dado
    if estado_anim_dado == "rolando":
        if dice_roll_sprites: 
            frame = dice_roll_sprites[dado_frame_atual] 
            rect = frame.get_rect(center=(LARGURA // 2, ALTURA // 2))
            TELA.blit(frame, rect)
    elif estado_anim_dado == "resultado":
        if dado_resultado_sorteado in dice_result_sprites: 
            frame = dice_result_sprites[dado_resultado_sorteado]
            rect = frame.get_rect(center=(LARGURA // 2, ALTURA // 2))
            TELA.blit(frame, rect)

def desenhar_falha_pilula():
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_tabuleiro()
    desenhar_hud()
    desenhar_janela_central(TELA, LARGURA * 0.7, 400, (25, 10, 10), VERMELHO, "FALHA NA CONEXÃO", jogo.MENSAGEM_FALHA_PILULA, fonte_subtitulo, fonte)
    desenhar_texto(TELA, "Pressione qualquer tecla para reiniciar o loop...", LARGURA//2, ALTURA - 100, BRANCO, True, fonte)

def desenhar_fim():
    global rects_botoes_fim, epilogo_scroll_y, EPILOGO_LINES, fim_scroll_acabou
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    rects_botoes_fim = {} 
    if not EPILOGO_LINES:
        epilogo_scroll_y = ALTURA + 50
        max_width = LARGURA * 0.8
        for pagina in jogo.PAGINAS_DO_EPILOGO:
            paragrafos = pagina.split('\n\n')
            for paragrafo in paragrafos:
                palavras = paragrafo.replace('\n', ' ').split(' ')
                linha_atual = ""
                for palavra in palavras:
                    linha_teste = linha_atual + palavra + " "
                    if fonte_prologo.size(linha_teste)[0] < max_width:
                        linha_atual = linha_teste
                    else:
                        EPILOGO_LINES.append(linha_atual)
                        linha_atual = palavra + " "
                EPILOGO_LINES.append(linha_atual)
                EPILOGO_LINES.append("")
    line_height = fonte_prologo.get_linesize()
    posicao_final_texto = epilogo_scroll_y + (len(EPILOGO_LINES) * line_height)
    if not fim_scroll_acabou:
        for i, line in enumerate(EPILOGO_LINES):
            y_pos = epilogo_scroll_y + (i * line_height)
            if y_pos < ALTURA and y_pos > -line_height:
                desenhar_texto(TELA, line, LARGURA // 2, y_pos, AMARELO, True, fonte_prologo)
        if posicao_final_texto < 0: 
            fim_scroll_acabou = True
    else:
        vencedor = None
        for p in jogo.peoes:
            if p["pos"] >= jogo.NUM_CASAS - 1: vencedor = p; break
        if not vencedor: vencedor = {"nome": "Ninguém"}
        desenhar_texto(TELA, f"Parabéns, {vencedor['nome']}!", LARGURA//2, ALTURA//2 - 100, AMARELO, True, fonte_titulo)
        btn_w, btn_h = 300, 70
        btn_x = LARGURA // 2 - btn_w // 2
        desenhar_botao(TELA, "Reiniciar", btn_x, ALTURA//2 + 50, btn_w, btn_h, (10,40,10), (20,80,20), fonte_botao)
        rects_botoes_fim["reiniciar"] = pygame.Rect(btn_x, ALTURA//2 + 50, btn_w, btn_h)
        desenhar_botao(TELA, "Menu", btn_x, ALTURA//2 + 50 + btn_h + 20, btn_w, btn_h, (40,10,10), (80,20,20), fonte_botao)
        rects_botoes_fim["menu"] = pygame.Rect(btn_x, ALTURA//2 + 50 + btn_h + 20, btn_w, btn_h)
    return posicao_final_texto 

def desenhar_pausa():
    global rects_botoes_pausa
    rects_botoes_pausa = {} 
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA) 
    overlay.fill((0, 0, 0, 180)) 
    TELA.blit(overlay, (0, 0))
    desenhar_texto(TELA, "PAUSA", LARGURA // 2, ALTURA * 0.25, VERDE_MATRIX, True, fonte_titulo)
    btn_w, btn_h = 400, 70
    btn_x = LARGURA // 2 - btn_w // 2
    y_start = ALTURA * 0.40
    desenhar_botao(TELA, "Continuar", btn_x, y_start, btn_w, btn_h, (10, 40, 10), (20, 80, 20), fonte_botao)
    rects_botoes_pausa["continuar"] = pygame.Rect(btn_x, y_start, btn_w, btn_h)
    desenhar_botao(TELA, "Opções", btn_x, y_start + btn_h + 20, btn_w, btn_h, (10, 10, 40), (20, 20, 80), fonte_botao)
    rects_botoes_pausa["opcoes"] = pygame.Rect(btn_x, y_start + btn_h + 20, btn_w, btn_h)
    desenhar_botao(TELA, "Voltar ao Menu", btn_x, y_start + 2 * (btn_h + 20), btn_w, btn_h, (40, 10, 10), (80, 20, 20), fonte_botao)
    rects_botoes_pausa["menu"] = pygame.Rect(btn_x, y_start + 2 * (btn_h + 20), btn_w, btn_h)

def desenhar_mostrar_buff():
    global jogador_com_buff
    if not jogador_com_buff: return # Segurança
    
    # Desenha o jogo por baixo (com o peão no início)
    desenhar_jogo()

    # Prepara o texto
    nome_jogador = jogador_com_buff['nome']
    tecla_str = pygame.key.name(jogador_com_buff['tecla']).upper()
    
    # Texto (mantendo 70% para bater com jogo.py)
    texto = (f"Saudações, {nome_jogador}. Não desista. Eu estou aqui com você.\n\n"
             "**BUFF ATIVO:**\n"
             "Suas chances de pegar cartas Boas aumentaram para **80%**.\n"
             "Suas chances de pegar cartas Ruins caíram para **20%**.\n\n"
             f"*Pressione sua tecla ({tecla_str}) para continuar...*")

    # Desenha a janela do Neo
    w, h = LARGURA * 0.7, 450 
    cx, cy = LARGURA // 2, ALTURA // 2
    ret_fundo = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
    pygame.draw.rect(TELA, (10, 25, 10), ret_fundo, border_radius=8)
    pygame.draw.rect(TELA, VERDE_MATRIX, ret_fundo, 3, border_radius=8)
    
    titulo = ">>> CONEXÃO ESTABELECIDA <<<"
    desenhar_texto(TELA, titulo, cx, ret_fundo.top + 30, VERDE_MATRIX, True, fonte_subtitulo)
    
    y_pos_sprite = ret_fundo.top + 80
    if "neo" in personagem_sprites:
        sprite = personagem_sprites["neo"]
        sprite_rect = sprite.get_rect(center=(cx, y_pos_sprite + sprite.get_height()//2 - 20))
        TELA.blit(sprite, sprite_rect); y_pos_texto = sprite_rect.bottom + 10
    else: 
        y_pos_texto = y_pos_sprite
    
    padding = 40
    ret_texto = pygame.Rect(ret_fundo.left + padding, y_pos_texto, w - padding*2, h - (y_pos_texto - ret_fundo.top) - 60)
    desenhar_texto_formatado(TELA, texto, BRANCO, ret_texto, fonte)


rodando = True
clock = pygame.time.Clock()
posicao_final_texto_prologo = 0 
posicao_final_texto_epilogo = 0 

# =====================================================================================
# ## <<< LOOP PRINCIPAL DO JOGO
# =====================================================================================
while rodando:
    delta_time = clock.tick(60)
    eventos = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos() 

    for evento in eventos:
        if evento.type == pygame.QUIT: rodando = False
        if evento.type == pygame.VIDEORESIZE:
            LARGURA, ALTURA = evento.size; TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
            rain_effect = MatrixRain(LARGURA, ALTURA, fonte_mono)
            jogo.criar_tabuleiro(LARGURA, ALTURA) 

        if evento.type == pygame.MOUSEBUTTONUP:
            if evento.button == 1: 
                if estado == MENU:
                    if "iniciar" in rects_botoes_menu and rects_botoes_menu["iniciar"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        estado = PROLOGO 
                        PROLOGO_LINES = [] 
                        prologo_scroll_y = ALTURA + 50 
                    elif "opcoes" in rects_botoes_menu and rects_botoes_menu["opcoes"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        estado = OPCOES
                        estado_anterior_opcoes = MENU 
                    elif "sair" in rects_botoes_menu and rects_botoes_menu["sair"].collidepoint(mouse_pos):
                        pygame.quit(); sys.exit()
                
                elif estado == PROLOGO:
                    if "pular" in rects_botoes_prologo and rects_botoes_prologo["pular"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        PROLOGO_LINES = [] 
                        estado = QTD_JOGADORES
                
                elif estado == REGRAS:
                    if "iniciar" in rects_botoes_regras and rects_botoes_regras["iniciar"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        pygame.mixer.music.stop() # ## <<< MUDANÇA: Para a música do menu
                        estado = CUTSCENE
                        cutscene_frame_atual = 0
                        cutscene_timer_frame = 0
                        cutscene_som_iniciado = False 

                elif estado == OPCOES:
                    if "geral-" in rects_botoes_opcoes and rects_botoes_opcoes["geral-"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        VOLUME_GERAL = max(0.0, round(VOLUME_GERAL - 0.1, 1))
                    elif "geral+" in rects_botoes_opcoes and rects_botoes_opcoes["geral+"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        VOLUME_GERAL = min(1.0, round(VOLUME_GERAL + 0.1, 1))
                    elif "musica-" in rects_botoes_opcoes and rects_botoes_opcoes["musica-"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        VOLUME_MUSICA = max(0.0, round(VOLUME_MUSICA - 0.1, 1))
                    elif "musica+" in rects_botoes_opcoes and rects_botoes_opcoes["musica+"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        VOLUME_MUSICA = min(1.0, round(VOLUME_MUSICA + 0.1, 1))
                    elif "efeitos-" in rects_botoes_opcoes and rects_botoes_opcoes["efeitos-"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        VOLUME_EFEITOS = max(0.0, round(VOLUME_EFEITOS - 0.1, 1))
                    elif "efeitos+" in rects_botoes_opcoes and rects_botoes_opcoes["efeitos+"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        VOLUME_EFEITOS = min(1.0, round(VOLUME_EFEITOS + 0.1, 1))
                    elif "res1" in rects_botoes_opcoes and rects_botoes_opcoes["res1"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        LARGURA, ALTURA = 1280, 720; TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
                        rain_effect = MatrixRain(LARGURA, ALTURA, fonte_mono) 
                        jogo.criar_tabuleiro(LARGURA, ALTURA)
                    elif "res2" in rects_botoes_opcoes and rects_botoes_opcoes["res2"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        LARGURA, ALTURA = 1440, 900; TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
                        rain_effect = MatrixRain(LARGURA, ALTURA, fonte_mono) 
                        jogo.criar_tabuleiro(LARGURA, ALTURA)
                    elif "resFull" in rects_botoes_opcoes and rects_botoes_opcoes["resFull"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        TELA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN); LARGURA, ALTURA = TELA.get_size()
                        rain_effect = MatrixRain(LARGURA, ALTURA, fonte_mono) 
                        jogo.criar_tabuleiro(LARGURA, ALTURA)
                    elif "voltar" in rects_botoes_opcoes and rects_botoes_opcoes["voltar"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        if estado_anterior_opcoes == PAUSA:
                            estado = PAUSA 
                        else:
                            estado = MENU 
                        estado_anterior_opcoes = None 
                    
                    pygame.mixer.music.set_volume(VOLUME_GERAL * VOLUME_MUSICA)
                    if click_sound: click_sound.set_volume(VOLUME_GERAL * VOLUME_EFEITOS)
                    if move_sound: move_sound.set_volume(VOLUME_GERAL * VOLUME_EFEITOS)
                    if dice_roll_sound: dice_roll_sound.set_volume(VOLUME_GERAL * VOLUME_EFEITOS)
                    if falha_sound: falha_sound.set_volume(VOLUME_GERAL * VOLUME_EFEITOS) 
                    if splash_sound: splash_sound.set_volume(VOLUME_GERAL * VOLUME_EFEITOS) 
                    if cutscene_sound: cutscene_sound.set_volume(VOLUME_GERAL * VOLUME_EFEITOS)
                        
                elif estado == QTD_JOGADORES:
                    for i in range(2, 5):
                        if i in rects_botoes_qtd and rects_botoes_qtd[i].collidepoint(mouse_pos):
                            if click_sound: click_sound.play()
                            num_jogadores = i
                            jogo.criar_jogadores(num_jogadores)
                            nomes = ["", "", "", ""]
                            estado = NOME
                            break
                elif estado == NOME:
                    if "confirmar" in rects_botoes_nome and rects_botoes_nome["confirmar"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        for i in range(num_jogadores):
                            if nomes[i].strip(): jogo.peoes[i]["nome"] = nomes[i].strip()
                        estado = SELECAO_PERSONAGEM
                elif estado == SELECAO_PERSONAGEM:
                    for i in range(1, len(selecao_sprites) + 1):
                        if i in rects_botoes_selecao and rects_botoes_selecao[i].collidepoint(mouse_pos) and i not in personagens_escolhidos:
                            if click_sound: click_sound.play()
                            jogo.peoes[jogador_selecionando]["personagem_id"] = i
                            personagens_escolhidos.append(i); jogador_selecionando += 1
                            if jogador_selecionando >= num_jogadores:
                                jogador_selecionando = 0; personagens_escolhidos = []
                                estado = REGRAS 
                            break
                
                elif estado == PILULA_FINAL:
                    if "azul" in rects_botoes_pilula and rects_botoes_pilula["azul"].collidepoint(mouse_pos):
                         if click_sound: click_sound.play()
                         resultado = jogo.aplicar_escolha_pilula_final(0)
                         if resultado == "sair": 
                             pagina_epilogo_atual = 0; estado = FIM
                             EPILOGO_LINES = []; fim_scroll_acabou = False 
                         else: 
                             estado = PILULA_FALHA
                             if falha_sound: falha_sound.play() 
                    elif "vermelha" in rects_botoes_pilula and rects_botoes_pilula["vermelha"].collidepoint(mouse_pos):
                         if click_sound: click_sound.play()
                         resultado = jogo.aplicar_escolha_pilula_final(1)
                         if resultado == "sair": 
                             pagina_epilogo_atual = 0; estado = FIM
                             EPILOGO_LINES = []; fim_scroll_acabou = False 
                         else: 
                             estado = PILULA_FALHA
                             if falha_sound: falha_sound.play() 
                
                elif estado == FIM:
                    if fim_scroll_acabou: 
                        if "reiniciar" in rects_botoes_fim and rects_botoes_fim["reiniciar"].collidepoint(mouse_pos):
                            if click_sound: click_sound.play()
                            jogo.resetar_partida() 
                            estado = JOGO
                            EPILOGO_LINES = []; fim_scroll_acabou = False
                        elif "menu" in rects_botoes_fim and rects_botoes_fim["menu"].collidepoint(mouse_pos):
                            if click_sound: click_sound.play()
                            jogo.resetar_partida()
                            estado = MENU
                            EPILOGO_LINES = []; fim_scroll_acabou = False
                
                elif estado == PAUSA:
                    if "continuar" in rects_botoes_pausa and rects_botoes_pausa["continuar"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        estado = JOGO 
                        pygame.mixer.music.unpause() 
                    elif "opcoes" in rects_botoes_pausa and rects_botoes_pausa["opcoes"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        estado = OPCOES
                        estado_anterior_opcoes = PAUSA 
                    elif "menu" in rects_botoes_pausa and rects_botoes_pausa["menu"].collidepoint(mouse_pos):
                        if click_sound: click_sound.play()
                        estado = MENU 
                        pygame.mixer.music.unpause() 
                        jogo.resetar_partida() 
                        estado_anterior_opcoes = None 

        if evento.type == pygame.KEYDOWN:
            if estado == SPLASH_SCREEN: 
                estado = MENU 
                if splash_sound:
                    splash_sound.stop()
                if not pygame.mixer.music.get_busy(): 
                    pygame.mixer.music.play(-1)
            
            elif estado == PROLOGO:
                PROLOGO_LINES = [] 
                estado = QTD_JOGADORES 
            
            elif estado == CUTSCENE:
                estado = JOGO 
                if cutscene_sound: cutscene_sound.stop()
                if not pygame.mixer.music.get_busy(): # ## <<< MUDANÇA: Toca a música
                    pygame.mixer.music.play(-1)
                
            elif estado == REGRAS: 
                pygame.mixer.music.stop() # ## <<< MUDANÇA: Para a música do menu
                estado = CUTSCENE 
                cutscene_frame_atual = 0
                cutscene_timer_frame = 0
                cutscene_som_iniciado = False 
            
            elif estado == NOME:
                if evento.key == pygame.K_TAB: foco_jogador = (foco_jogador + 1) % num_jogadores
                elif evento.key == pygame.K_BACKSPACE: nomes[foco_jogador] = nomes[foco_jogador][:-1]
                elif evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                     for i in range(num_jogadores):
                         if nomes[i].strip(): jogo.peoes[i]["nome"] = nomes[i].strip()
                     estado = SELECAO_PERSONAGEM
                else:
                    ch = evento.unicode
                    if ch and len(ch) == 1 and ch.isprintable() and len(nomes[foco_jogador]) < 18: nomes[foco_jogador] += ch
            
            elif estado == PILULA_FALHA:
                jogador_com_buff = pilula_final_peao # Salva quem falhou

                if not jogador_com_buff["buff_ativo"]:
                    jogador_com_buff["buff_ativo"] = True
                
                movimento = 0 - jogador_com_buff["pos"] 
                
                animacao_em_andamento = True
                peao_animando = jogador_com_buff
                passos_restantes = abs(movimento)
                passos_direcao = -1 
                o_que_fazer_depois_anim = "MOSTRAR_BUFF" 

                estado = JOGO 

            elif estado == MOSTRAR_BUFF:
                if jogador_com_buff and evento.key == jogador_com_buff["tecla"]: 
                    estado = JOGO
                    jogador_com_buff = None 
            
            elif estado == FIM:
                if not fim_scroll_acabou: 
                    fim_scroll_acabou = True 
            
            elif estado == JOGO:
                if evento.key == pygame.K_ESCAPE:
                    estado = PAUSA
                    pygame.mixer.music.pause() 
                
                elif not jogador_com_buff:
                    jogador = jogo.peoes[jogo.jogador_atual]
                    if evento.key == jogador["tecla"]:
                        
                        if not animacao_em_andamento and not jogo.aguardando_carta and estado_anim_dado == "nenhum":
                            estado_anim_dado = "rolando"
                            timer_anim_dado = 0
                            dado_frame_timer = 0
                            dado_frame_atual = 0
                            if dice_roll_sound:
                                dice_roll_sound.stop() 
                                dice_roll_sound.play()
                        
                        elif jogo.aguardando_carta:
                            efeitos = jogo.aplicar_carta(jogador, jogo.carta_atual)
                            
                            jogo.aguardando_carta = False
                            jogo.mensagem_carta = None
                            jogador['dado'] = 0 

                            movimento = 0
                            destino_final = jogador["pos"]
                            passos_direcao = 1
                            animacao_replay = efeitos.get("replay", False) 
                            
                            if "mov" in efeitos:
                                movimento = efeitos["mov"] 
                            elif "voltar_turno" in efeitos:
                                movimento = jogador["pos_anterior"] - jogador["pos"] 
                            elif "voltar_inicio_fileira" in efeitos:
                                destino_final = (jogador["pos"] // 8) * 8
                                movimento = destino_final - jogador["pos"] 
                            
                            if movimento != 0:
                                destino_final = jogador["pos"] + movimento
                                destino_final = max(0, min(jogo.NUM_CASAS - 1, destino_final))
                                movimento = destino_final - jogador["pos"]

                                animacao_em_andamento = True
                                peao_animando = jogador
                                passos_restantes = abs(movimento)
                                passos_direcao = 1 if movimento > 0 else -1
                                o_que_fazer_depois_anim = "AVANCAR_TURNO" 
                            
                            else:
                                jogo.avancar_turno(replay=animacao_replay)
            
            elif estado == PAUSA:
                if evento.key == pygame.K_ESCAPE:
                    estado = JOGO
                    pygame.mixer.music.unpause() 
                    estado_anterior_opcoes = None 

    # Lógica de atualização (só roda se não estiver pausado)
    if estado != PAUSA:
        if estado == SPLASH_SCREEN:
            if not splash_som_iniciado:
                if splash_sound:
                    splash_sound.play()
                splash_som_iniciado = True

            if not splash_anim_concluida and splash_frames:
                splash_timer_frame += delta_time
                if splash_timer_frame > TEMPO_FRAME_SPLASH:
                    splash_timer_frame = 0
                    splash_frame_atual += 1
                
                if splash_frame_atual >= len(splash_frames):
                    splash_frame_atual = len(splash_frames) - 2 
                    splash_anim_concluida = True
                    if not pygame.mixer.music.get_busy(): 
                        pygame.mixer.music.play(-1)
        
        if estado == PROLOGO:
            prologo_scroll_y -= PROLOGO_SCROLL_SPEED * (delta_time / 16.6) 
            if posicao_final_texto_prologo < 0: 
                PROLOGO_LINES = [] 
                estado = QTD_JOGADORES 

        if estado == CUTSCENE and cutscene_frames:
            if not cutscene_som_iniciado:
                if cutscene_sound:
                    cutscene_sound.play()
                cutscene_som_iniciado = True

            cutscene_timer_frame += delta_time
            if cutscene_timer_frame > TEMPO_FRAME_CUTSCENE:
                cutscene_timer_frame = 0
                cutscene_frame_atual += 1
            
            if cutscene_frame_atual >= len(cutscene_frames):
                estado = JOGO 
                if cutscene_sound:
                    cutscene_sound.stop() 
                if not pygame.mixer.music.get_busy(): # ## <<< MUDANÇA: Toca a música
                    pygame.mixer.music.play(-1)
        
        if estado == FIM and not fim_scroll_acabou:
            epilogo_scroll_y -= EPILOGO_SCROLL_SPEED * (delta_time / 16.6)
            if posicao_final_texto_epilogo < -200: 
                fim_scroll_acabou = True

        if estado_anim_dado == "rolando":
            timer_anim_dado += delta_time
            dado_frame_timer += delta_time
            if dado_frame_timer > TEMPO_FRAME_DADO and dice_roll_sprites:
                dado_frame_timer = 0
                dado_frame_atual = random.randint(0, len(dice_roll_sprites) - 1)
            if timer_anim_dado > DURACAO_ANIM_DADO:
                estado_anim_dado = "resultado"
                timer_anim_dado = 0 
                jogador = jogo.peoes[jogo.jogador_atual]
                dado_resultado_sorteado = jogo.jogar_vez(jogador)
                jogador['dado'] = dado_resultado_sorteado 
        elif estado_anim_dado == "resultado":
            timer_anim_dado += delta_time
            if timer_anim_dado > DURACAO_MOSTRAR_DADO:
                estado_anim_dado = "nenhum"
                timer_anim_dado = 0
                if dice_roll_sound:
                    dice_roll_sound.stop()
                
                animacao_em_andamento = True
                peao_animando = jogo.peoes[jogo.jogador_atual]
                passos_restantes = dado_resultado_sorteado
                passos_direcao = 1 
                o_que_fazer_depois_anim = "PUXAR_CARTA"
                
                dado_resultado_sorteado = 0 
        
        if animacao_em_andamento:
            timer_animacao += delta_time 
            if timer_animacao > TEMPO_PASSO: 
                timer_animacao = 0
                if passos_restantes > 0:
                    peao_animando["pos"] += passos_direcao 
                    passos_restantes -= 1
                    if move_sound:
                        move_sound.play()
                
                if passos_restantes == 0:
                    animacao_em_andamento = False
                    peao_animando["pos"] = max(0, min(jogo.NUM_CASAS - 1, peao_animando["pos"]))
                    
                    if o_que_fazer_depois_anim == "PUXAR_CARTA":
                        if jogo.is_escolha_pilula_final(peao_animando["pos"]):
                            pilula_final_peao = peao_animando; estado = PILULA_FINAL; jogo.sortear_pilulas_final()
                        else:
                            jogo.puxar_carta(peao_animando) 
                    
                    elif o_que_fazer_depois_anim == "AVANCAR_TURNO":
                        jogo.avancar_turno(replay=animacao_replay)
                        animacao_replay = False 
                    
                    elif o_que_fazer_depois_anim == "MOSTRAR_BUFF":
                        estado = MOSTRAR_BUFF

                    o_que_fazer_depois_anim = None 

    # Desenho
    TELA.fill(PRETO_MATRIX)
    if estado == SPLASH_SCREEN: desenhar_splash_screen()
    elif estado == MENU: desenhar_menu()
    elif estado == OPCOES: desenhar_opcoes()
    elif estado == QTD_JOGADORES: desenhar_qtd_jogadores()
    elif estado == NOME: desenhar_nome()
    elif estado == SELECAO_PERSONAGEM: desenhar_selecao_personagem()
    elif estado == PROLOGO: 
        posicao_final_texto_prologo = desenhar_prologo() 
    elif estado == CUTSCENE: desenhar_cutscene() 
    elif estado == REGRAS: desenhar_regras()
    elif estado == JOGO: desenhar_jogo()
    elif estado == PILULA_FALHA: desenhar_falha_pilula()
    elif estado == MOSTRAR_BUFF: desenhar_mostrar_buff() 
    elif estado == PILULA_FINAL:
        rects_botoes_pilula = {}
        # Desenha o jogo por baixo
        rain_effect.update_and_draw(TELA); desenhar_tabuleiro(); desenhar_linhas_tabuleiro()
        for i, p in enumerate(jogo.peoes): # Desenha os peões
            char_id = p.get("personagem_id"); idx = min(p["pos"], len(jogo.CASAS)-1); x, y = jogo.CASAS[idx]
            if char_id in peao_sprites:
                spritesheet = peao_sprites[char_id]; frame_width = spritesheet.get_width() // 2; frame_rect = pygame.Rect(frame_width * frame_atual, 0, frame_width, spritesheet.get_height())
                peao_img = spritesheet.subsurface(frame_rect); peao_img_redimensionada = pygame.transform.scale(peao_img, (65, 65)); peao_rect = peao_img_redimensionada.get_rect(center=(x + jogo.CASA_TAM//2, y + jogo.CASA_TAM//2))
                TELA.blit(peao_img_redimensionada, peao_rect); nome_jogador = p['nome']; nome_x = peao_rect.centerx; nome_y = peao_rect.top - 10
                desenhar_texto(TELA, nome_jogador, nome_x, nome_y, BRANCO, True, fonte_peao_nome)
            else:
                offset = (i - (num_jogadores-1)/2) * 15; circ_x = x + jogo.CASA_TAM//2 + offset; circ_y = y + jogo.CASA_TAM//2
                pygame.draw.circle(TELA, p["cor"], (circ_x, circ_y), 20); nome_jogador = p['nome']; nome_x = circ_x; nome_y = circ_y - 30
                desenhar_texto(TELA, nome_jogador, nome_x, nome_y, BRANCO, True, fonte_peao_nome)
        desenhar_hud()
        
        # Desenha a janela da pílula
        texto_morpheus = ("A voz do Operador soa distorcida...\n\n'É agora! Encontramos uma brecha, mas ela não vai durar.\nUma pílula te levará para a saída... a outra irá te prender ao código-fonte, reiniciando seu loop.\n\nConfie no seu instinto. Acredite.'")
        desenhar_janela_central(TELA, 1200, 500, (10,25,10), VERDE_MATRIX, "A ESCOLHA FINAL", texto_morpheus, fonte_subtitulo, fonte)
        btn_w, btn_h = 400, 100
        y_btn = ALTURA//2 + 120
        desenhar_botao(TELA, "Pílula Azul", LARGURA//2 - btn_w - 30, y_btn, btn_w, btn_h, (10,10,60), (20,20,120), fonte_botao)
        rects_botoes_pilula["azul"] = pygame.Rect(LARGURA//2 - btn_w - 30, y_btn, btn_w, btn_h)
        desenhar_botao(TELA, "Pílula Vermelha", LARGURA//2 + 30, y_btn, btn_w, btn_h, (60,10,10), (120,20,20), fonte_botao)
        rects_botoes_pilula["vermelha"] = pygame.Rect(LARGURA//2 + 30, y_btn, btn_w, btn_h)
    
    elif estado == FIM: 
        posicao_final_texto_epilogo = desenhar_fim() 
    
    elif estado == PAUSA:
        desenhar_jogo() 
        desenhar_pausa() 

    pygame.display.flip()

pygame.quit()
sys.exit()
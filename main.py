import pygame
import sys
import os
from utils import (
    desenhar_texto, desenhar_botao, desenhar_janela_central, MatrixRain,
    BRANCO, PRETO, VERDE, VERMELHO, AZUL, AMARELO, CINZA,
    VERDE_MATRIX, PRETO_MATRIX, desenhar_texto_formatado
)
import jogo

pygame.init()


LARGURA, ALTURA = 1440, 900
TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
pygame.display.set_caption("Jogo da Vida - A Matrix")


fonte = pygame.font.SysFont("arial", 28)
fonte_titulo = pygame.font.SysFont("arialblack", 70)
fonte_subtitulo = pygame.font.SysFont("arialblack", 40)
fonte_botao = pygame.font.SysFont("arialblack", 30)
fonte_mono = pygame.font.SysFont("consolas", 22)


pygame.mixer.init()
VOLUME = 0.5
pygame.mixer.music.set_volume(VOLUME)
try:
    pygame.mixer.music.load(os.path.join("assets", "musica_menu.mp3"))
    pygame.mixer.music.play(-1)
except Exception as e:
    print(f"⚠️ Música de menu não encontrada: {e}")
try:
    click_sound = pygame.mixer.Sound(os.path.join("assets", "click.wav"))
    click_sound.set_volume(VOLUME)
except Exception as e:
    click_sound = None
    print(f"⚠️ Som de clique não encontrado: {e}")
try:
    move_sound = pygame.mixer.Sound(os.path.join("assets", "move.wav")) 
    move_sound.set_volume(VOLUME)
except:
    move_sound = None


personagem_sprites = {}
selecao_sprites = {}
peao_sprites = {}

personagens_nomes_cartas = ["neo", "trinity", "morpheus", "oraculo", "operador", "smith", "merovingio", "gemeos", "arquiteto"]
for nome in personagens_nomes_cartas:
    try:
        imagem = pygame.image.load(os.path.join("assets", "images", f"{nome}.png")).convert_alpha()
        personagem_sprites[nome] = pygame.transform.scale(imagem, (100, 100))
    except Exception as e:
        print(f"⚠️ Sprite de carta '{nome}' não encontrada: {e}")

for i in range(1, 5):
    try:
        img_selecao = pygame.image.load(os.path.join("assets", "images", f"programador_{i}.png")).convert_alpha()
        selecao_sprites[i] = pygame.transform.scale(img_selecao, (150, 150))
        peao_sprites[i] = pygame.image.load(os.path.join("assets", "personagens", f"programador_{i}.png")).convert_alpha()
    except Exception as e:
        print(f"⚠️ Sprite do programador {i} não encontrada: {e}")


jogo.criar_tabuleiro()
jogo.criar_jogadores(num_jogadores=2)
rain_effect = MatrixRain(LARGURA, ALTURA, pygame.font.SysFont("consolas", 18, bold=True))


SPLASH_SCREEN = "splash_screen"
MENU = "menu"
OPCOES = "opcoes"
QTD_JOGADORES = "qtd_jogadores"
NOME = "nome"
SELECAO_PERSONAGEM = "selecao_personagem"
PROLOGO = "prologo"
REGRAS = "regras"
JOGO = "jogo"
PILULA_FINAL = "pilula_final"
PILULA_FALHA = "pilula_falha" 
FIM = "fim"
estado = SPLASH_SCREEN


nomes = ["", "", "", ""]
foco_jogador = 0
cursor_on = True
cursor_timer = 0
num_jogadores = 2
pagina_lore_atual = 0
pagina_epilogo_atual = 0
jogador_selecionando = 0
personagens_escolhidos = []


animacao_em_andamento = False
peao_animando = None
passos_restantes = 0
timer_animacao = 0
TEMPO_PASSO = 150
frame_atual = 0
timer_frame = 0
TEMPO_FRAME = 200 



def desenhar_splash_screen():
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_texto(TELA, "JOGO DA VIDA - A MATRIX", LARGURA//2, ALTURA//2 - 50, VERDE_MATRIX, True, fonte_titulo)
    desenhar_texto(TELA, "APERTE QUALQUER TECLA PARA COMEÇAR", LARGURA//2, ALTURA//2 + 50, BRANCO, True, fonte_botao)

def desenhar_menu():
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_texto(TELA, "Jogo da Vida - A Matrix", LARGURA//2, 120, VERDE_MATRIX, True, fonte_titulo)
    if desenhar_botao(TELA, "Iniciar Jogo", LARGURA//2 - 150, 300, 300, 70, (10,40,10), (20,80,20), fonte_botao, click_sound):
        return QTD_JOGADORES
    if desenhar_botao(TELA, "Opções", LARGURA//2 - 150, 400, 300, 70, (10,10,40), (20,20,80), fonte_botao, click_sound):
        return OPCOES
    if desenhar_botao(TELA, "Sair", LARGURA//2 - 150, 500, 300, 70, (40,10,10), (80,20,20), fonte_botao, click_sound):
        pygame.quit(); sys.exit()
    return MENU

def desenhar_opcoes():
    global VOLUME, TELA, LARGURA, ALTURA
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_texto(TELA, "Opções", LARGURA//2, 80, VERDE_MATRIX, True, fonte_titulo)
    desenhar_texto(TELA, "Volume", LARGURA//2, 180, BRANCO, True, fonte_botao)
    if desenhar_botao(TELA, "-", LARGURA//2 - 150, 220, 80, 80, (40,40,40), (80,80,80), fonte_botao, click_sound):
        VOLUME = max(0.0, VOLUME - 0.1)
    desenhar_texto(TELA, f"{int(VOLUME*100)}%", LARGURA//2, 260, BRANCO, True, fonte_botao)
    if desenhar_botao(TELA, "+", LARGURA//2 + 70, 220, 80, 80, (40,40,40), (80,80,80), fonte_botao, click_sound):
        VOLUME = min(1.0, VOLUME + 0.1)
    pygame.mixer.music.set_volume(VOLUME)
    if click_sound: click_sound.set_volume(VOLUME)
    desenhar_texto(TELA, "Resolução", LARGURA//2, 350, BRANCO, True, fonte_botao)
    if desenhar_botao(TELA, "1280 x 720", LARGURA//2 - 200, 400, 400, 60, (40,40,40), (80,80,80), fonte_botao, click_sound):
        LARGURA, ALTURA = 1280, 720; TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
    if desenhar_botao(TELA, "1440 x 900", LARGURA//2 - 200, 480, 400, 60, (40,40,40), (80,80,80), fonte_botao, click_sound):
        LARGURA, ALTURA = 1440, 900; TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
    if desenhar_botao(TELA, "Tela Cheia", LARGURA//2 - 200, 560, 400, 60, (40,40,40), (80,80,80), fonte_botao, click_sound):
        TELA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN); LARGURA, ALTURA = TELA.get_size()
    if desenhar_botao(TELA, "Voltar ao Menu", LARGURA//2 - 200, ALTURA - 150, 400, 70, (40,10,10), (80,20,20), fonte_botao, click_sound):
        return MENU
    return OPCOES

def desenhar_qtd_jogadores():
    global num_jogadores, nomes
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_texto(TELA, "Quantidade de Programadores", LARGURA//2, 120, VERDE_MATRIX, True, fonte_titulo)
    for i in range(2, 5):
        x_pos = LARGURA//2 - (100 * 1.5 + 20 * 1) + (i-2)*120
        if desenhar_botao(TELA, str(i), x_pos, 300, 100, 100, (10,40,10), (20,80,20), fonte_botao, click_sound):
            num_jogadores = i
            jogo.criar_jogadores(num_jogadores)
            nomes = ["", "", "", ""]
            return NOME
    return QTD_JOGADORES

def desenhar_nome():
    global cursor_on, cursor_timer, foco_jogador, nomes
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_texto(TELA, "Identifiquem-se, Programadores", LARGURA//2, 120, VERDE_MATRIX, True, fonte_titulo)
    cursor_timer += 1
    if cursor_timer > 25:
        cursor_on = not cursor_on; cursor_timer = 0
    teclas_legenda = ["A", "G", "J", "L"]
    campo_w, campo_h = 520, 70
    campos_y = 220
    for i in range(num_jogadores):
        x = LARGURA//2 - campo_w//2
        y = campos_y + i*(campo_h+16)
        pygame.draw.rect(TELA, (5,25,5), (x, y, campo_w, campo_h), border_radius=8)
        pygame.draw.rect(TELA, VERDE_MATRIX, (x, y, campo_w, campo_h), 2, border_radius=8)
        texto = nomes[i] + ("_" if cursor_on and foco_jogador == i else "")
        desenhar_texto(TELA, f"Programador {i+1} (tecla: {teclas_legenda[i]}): {texto}", x+12, y+20, VERDE_MATRIX, False, fonte_mono)
    btn_y = campos_y + num_jogadores*(campo_h+16) + 30
    if desenhar_botao(TELA, "Confirmar Nomes", LARGURA//2 - 150, btn_y, 300, 70, (10,40,10), (20,80,20), fonte_botao, click_sound):
        for i in range(num_jogadores):
            if nomes[i].strip():
                jogo.peoes[i]["nome"] = nomes[i].strip()
        return SELECAO_PERSONAGEM
    return NOME

def desenhar_selecao_personagem():
    global jogador_selecionando, personagens_escolhidos
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    nome_jogador = jogo.peoes[jogador_selecionando]['nome']
    desenhar_texto(TELA, f"{nome_jogador}, escolha seu avatar:", LARGURA//2, 120, VERDE_MATRIX, True, fonte_titulo)
    num_chars = len(selecao_sprites)
    total_w = num_chars * 150 + (num_chars - 1) * 30
    start_x = LARGURA//2 - total_w//2
    for i in range(1, num_chars + 1):
        x = start_x + (i - 1) * (150 + 30)
        y = ALTURA//2 - 150//2
        sprite = selecao_sprites[i]
        rect = sprite.get_rect(topleft=(x, y))
        mouse_pos = pygame.mouse.get_pos()
        clicado = pygame.mouse.get_pressed()[0]
        if i in personagens_escolhidos:
            surf = pygame.Surface(rect.size, pygame.SRCALPHA); surf.fill((50, 50, 50, 180)); TELA.blit(sprite, rect); TELA.blit(surf, rect)
            desenhar_texto(TELA, "Escolhido", rect.centerx, rect.bottom + 20, CINZA, True, fonte)
        else:
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(TELA, VERDE_MATRIX, (rect.x-5, rect.y-5, rect.w+10, rect.h+10), 3, border_radius=8)
                if clicado:
                    if click_sound: click_sound.play()
                    jogo.peoes[jogador_selecionando]["personagem_id"] = i
                    personagens_escolhidos.append(i); jogador_selecionando += 1; pygame.time.delay(200)
            TELA.blit(sprite, rect)
    if jogador_selecionando >= num_jogadores:
        jogador_selecionando = 0; personagens_escolhidos = []; return PROLOGO
    return SELECAO_PERSONAGEM

def desenhar_prologo():
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    texto_pagina = jogo.PAGINAS_DA_LORE[pagina_lore_atual]
    desenhar_janela_central(TELA, 1200, 500, (10,25,10), VERDE_MATRIX, "PRÓLOGO", texto_pagina, fonte_subtitulo, fonte)
    desenhar_texto(TELA, "Pressione qualquer tecla para continuar...", LARGURA//2, ALTURA - 100, BRANCO, True, fonte)

def desenhar_regras():
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    regras = ("1. Use sua tecla (A, G, J, L) para jogar o dado na sua vez.\n\n"
              "2. O peão se moverá casa por casa. Após parar, a carta do local será revelada.\n\n"
              "3. Siga as instruções das cartas para avançar ou recuar.\n\n"
              "4. O objetivo é chegar à 'Saída' e fazer a escolha final correta para escapar da Matrix.")
    desenhar_janela_central(TELA, 1200, 500, (10,25,10), VERDE_MATRIX, "REGRAS", regras, fonte_subtitulo, fonte)
    desenhar_texto(TELA, "Pressione qualquer tecla para iniciar o jogo", LARGURA//2, ALTURA - 100, BRANCO, True, fonte)

def desenhar_tabuleiro():
    for idx, (x, y) in enumerate(jogo.CASAS):
        pygame.draw.rect(TELA, (0, 30, 0), (x, y, jogo.CASA_TAM, jogo.CASA_TAM), border_radius=4)
        pygame.draw.rect(TELA, (0, 80, 0), (x, y, jogo.CASA_TAM, jogo.CASA_TAM), 2, border_radius=4)
        if idx == 0: desenhar_texto(TELA, "Início", x + jogo.CASA_TAM//2, y + jogo.CASA_TAM//2, VERDE_MATRIX, True, fonte)
        elif idx == jogo.NUM_CASAS - 1: desenhar_texto(TELA, "Saída", x + jogo.CASA_TAM//2, y + jogo.CASA_TAM//2, VERDE_MATRIX, True, fonte)

def desenhar_hud():
    y0 = 20
    teclas_legenda = ["A", "G", "J", "L"]
    for i, p in enumerate(jogo.peoes):
        cor = AMARELO if i == jogo.jogador_atual else VERDE_MATRIX
        desenhar_texto(TELA, f"{p['nome']} [{teclas_legenda[i]}] - Casa: {p['pos']+1}", 30, y0 + i*30, cor, False, fonte_mono)
    jogador_da_vez = jogo.peoes[jogo.jogador_atual]
    desenhar_texto(TELA, f"Vez de: {jogador_da_vez['nome']}", LARGURA - 250, 20, AMARELO, True, fonte_mono)
    if "dado" in jogador_da_vez and jogador_da_vez['dado'] > 0:
        desenhar_texto(TELA, f"Dado rolado: {jogador_da_vez['dado']}", LARGURA - 250, 50, BRANCO, True, fonte_mono)

def desenhar_jogo():
    global frame_atual, timer_frame
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_tabuleiro()

    timer_frame += clock.get_time()
    if timer_frame > TEMPO_FRAME:
        timer_frame = 0; frame_atual = (frame_atual + 1) % 2

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
        else:
            offset = (i - (num_jogadores-1)/2) * 15
            pygame.draw.circle(TELA, p["cor"], (x + jogo.CASA_TAM//2 + offset, y + jogo.CASA_TAM//2), 20)

    desenhar_hud()
    
    if jogo.mensagem_carta:
        w, h = 1000, 350; cx, cy = LARGURA // 2, ALTURA // 2
        ret_fundo = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
        pygame.draw.rect(TELA, (10, 25, 10), ret_fundo, border_radius=8)
        pygame.draw.rect(TELA, VERDE_MATRIX, ret_fundo, 3, border_radius=8)
        titulo = ">>> TRANSMISSÃO RECEBIDA <<<"
        desenhar_texto(TELA, titulo, cx, ret_fundo.top + 30, VERDE_MATRIX, True, fonte_subtitulo)
        y_pos_sprite = ret_fundo.top + 80
        if jogo.personagem_carta and jogo.personagem_carta in personagem_sprites:
            sprite = personagem_sprites[jogo.personagem_carta]
            sprite_rect = sprite.get_rect(center=(cx, y_pos_sprite + sprite.get_height()//2 - 20))
            TELA.blit(sprite, sprite_rect); y_pos_texto = sprite_rect.bottom
        else: y_pos_texto = y_pos_sprite
        padding = 40; ret_texto = pygame.Rect(ret_fundo.left + padding, y_pos_texto, w - padding*2, h - (y_pos_texto - ret_fundo.top) - 60)
        desenhar_texto_formatado(TELA, jogo.mensagem_carta, BRANCO, ret_texto, fonte)
        if jogo.aguardando_carta:
            tecla_str = pygame.key.name(jogo.peoes[jogo.jogador_atual]['tecla']).upper()
            desenhar_texto(TELA, f"Pressione sua tecla ({tecla_str}) para continuar!", cx, ret_fundo.bottom - 30, AMARELO, True, fonte)


def desenhar_falha_pilula():
    TELA.fill(PRETO_MATRIX)
    rain_effect.update_and_draw(TELA)
    desenhar_tabuleiro()
    desenhar_hud() 
    desenhar_janela_central(TELA, 1000, 350, (25, 10, 10), VERMELHO, "FALHA NA CONEXÃO", jogo.MENSAGEM_FALHA_PILULA, fonte_subtitulo, fonte)
    desenhar_texto(TELA, "Pressione qualquer tecla para reiniciar o loop...", LARGURA//2, ALTURA - 100, BRANCO, True, fonte)

def desenhar_fim():
    TELA.fill(PRETO_MATRIX); rain_effect.update_and_draw(TELA)
    vencedor = None
    for p in jogo.peoes:
        if p["pos"] >= jogo.NUM_CASAS -1: vencedor = p; break
    if not vencedor: vencedor = {"nome": "Ninguém"}
    texto_pagina = jogo.PAGINAS_DO_EPILOGO[pagina_epilogo_atual]
    desenhar_janela_central(TELA, 1200, 500, (10,25,10), VERDE_MATRIX, "EPÍLOGO", texto_pagina, fonte_subtitulo, fonte)
    if pagina_epilogo_atual == len(jogo.PAGINAS_DO_EPILOGO) - 1:
        desenhar_texto(TELA, f"Parabéns, {vencedor['nome']}!", LARGURA//2, ALTURA - 150, AMARELO, True, fonte_botao)
        desenhar_texto(TELA, "Pressione 1 para Reiniciar ou 2 para Voltar ao Menu", LARGURA//2, ALTURA - 100, BRANCO, True, fonte)
    else:
        desenhar_texto(TELA, "Pressione qualquer tecla para continuar...", LARGURA//2, ALTURA - 100, BRANCO, True, fonte)


rodando = True
clock = pygame.time.Clock()

while rodando:
    delta_time = clock.tick(60)
    eventos = pygame.event.get()

    for evento in eventos:
        if evento.type == pygame.QUIT: rodando = False
        if evento.type == pygame.VIDEORESIZE:
            LARGURA, ALTURA = evento.size; TELA = pygame.display.set_mode((LARGURA, ALTURA), pygame.RESIZABLE)
            rain_effect = MatrixRain(LARGURA, ALTURA, pygame.font.SysFont("consolas", 18, bold=True))

        if evento.type == pygame.KEYDOWN:
            if estado == SPLASH_SCREEN: estado = MENU
            elif estado == PROLOGO:
                pagina_lore_atual += 1
                if pagina_lore_atual >= len(jogo.PAGINAS_DA_LORE): pagina_lore_atual = 0; estado = REGRAS
            elif estado == REGRAS: estado = JOGO
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
                estado = JOGO
            elif estado == FIM:
                if pagina_epilogo_atual < len(jogo.PAGINAS_DO_EPILOGO) - 1: pagina_epilogo_atual += 1
                else:
                    if evento.key == pygame.K_1: jogo.resetar_partida(); estado = JOGO
                    elif evento.key == pygame.K_2: estado = MENU; pagina_epilogo_atual = 0
            elif estado == JOGO:
                jogador = jogo.peoes[jogo.jogador_atual]
                if evento.key == jogador["tecla"]:
                    if not animacao_em_andamento and not jogo.aguardando_carta:
                        dado = jogo.jogar_vez(jogador)
                        animacao_em_andamento = True; peao_animando = jogador; passos_restantes = dado
                    elif jogo.aguardando_carta:
                        efeitos = jogo.aplicar_carta(jogador, jogo.carta_atual)
                        if "mov" in efeitos: jogador["pos"] += efeitos["mov"]
                        if "voltar_turno" in efeitos: jogador["pos"] = jogador["pos_anterior"]
                        if "voltar_inicio_fileira" in efeitos: jogador["pos"] = (jogador["pos"] // 8) * 8
                        if "ignorar_proxima_negativa" in efeitos: jogador["ignorar_proxima_negativa"] = True
                        jogador["pos"] = max(0, min(jogo.NUM_CASAS - 1, jogador["pos"]))
                        jogo.aguardando_carta = False; jogo.mensagem_carta = None
                        if jogo.is_escolha_pilula_final(jogador["pos"]):
                            pilula_final_peao = jogador; estado = PILULA_FINAL; jogo.sortear_pilulas_final()
                        else:
                            jogo.avancar_turno(replay=efeitos.get("replay"))

    if animacao_em_andamento:
        timer_animacao += delta_time
        if timer_animacao > TEMPO_PASSO:
            timer_animacao = 0
            if passos_restantes > 0:
                peao_animando["pos"] += 1
                if move_sound: move_sound.play()
                passos_restantes -= 1
            if passos_restantes == 0:
                animacao_em_andamento = False
                peao_animando["pos"] = max(0, min(jogo.NUM_CASAS - 1, peao_animando["pos"]))
                if jogo.is_escolha_pilula_final(peao_animando["pos"]):
                    pilula_final_peao = peao_animando; estado = PILULA_FINAL; jogo.sortear_pilulas_final()
                else:
                    jogo.puxar_carta()
    
    TELA.fill(PRETO_MATRIX)
    if estado == SPLASH_SCREEN: desenhar_splash_screen()
    elif estado == MENU: estado = desenhar_menu()
    elif estado == OPCOES: estado = desenhar_opcoes()
    elif estado == QTD_JOGADORES: estado = desenhar_qtd_jogadores()
    elif estado == NOME: estado = desenhar_nome()
    elif estado == SELECAO_PERSONAGEM: estado = desenhar_selecao_personagem()
    elif estado == PROLOGO: desenhar_prologo()
    elif estado == REGRAS: desenhar_regras()
    elif estado == JOGO: desenhar_jogo()
    elif estado == PILULA_FALHA: desenhar_falha_pilula() 
    elif estado == PILULA_FINAL:
        rain_effect.update_and_draw(TELA); desenhar_tabuleiro(); desenhar_hud()
        texto_morpheus = ("A voz do Operador soa distorcida...\n\n'É agora! Encontramos uma brecha, mas ela não vai durar.\nUma pílula te levará para a saída... a outra irá te prender ao código-fonte, reiniciando seu loop.\n\nConfie no seu instinto. Acredite.'")
        desenhar_janela_central(TELA, 1200, 500, (10,25,10), VERDE_MATRIX, "A ESCOLHA FINAL", texto_morpheus, fonte_subtitulo, fonte)
        btn_w, btn_h = 400, 100
        y_btn = ALTURA//2 + 120
        if desenhar_botao(TELA, "Pílula Azul", LARGURA//2 - btn_w - 30, y_btn, btn_w, btn_h, (10,10,60), (20,20,120), fonte_botao, click_sound):
            resultado = jogo.aplicar_escolha_pilula_final(0)
            if resultado == "sair": pagina_epilogo_atual = 0; estado = FIM
            else: pilula_final_peao["pos"] = 0; estado = PILULA_FALHA 
        if desenhar_botao(TELA, "Pílula Vermelha", LARGURA//2 + 30, y_btn, btn_w, btn_h, (60,10,10), (120,20,20), fonte_botao, click_sound):
            resultado = jogo.aplicar_escolha_pilula_final(1)
            if resultado == "sair": pagina_epilogo_atual = 0; estado = FIM
            else: pilula_final_peao["pos"] = 0; estado = PILULA_FALHA 
    elif estado == FIM: desenhar_fim()
    
    pygame.display.flip()

pygame.quit()
sys.exit()
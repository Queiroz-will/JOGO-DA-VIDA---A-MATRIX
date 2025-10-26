
import pygame
import random


BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 200, 0)
VERMELHO = (200, 0, 0)
AZUL = (0, 0, 200)
ROXO = (128, 0, 128)
AMARELO = (255, 255, 0)
LARANJA = (255, 165, 0)
CINZA = (128, 128, 128)

VERDE_MATRIX = (0, 255, 70)
PRETO_MATRIX = (0, 0, 0)


def desenhar_texto(tela, texto, x, y, cor, centralizado=False, fonte=None):
    if fonte is None:
        fonte = pygame.font.SysFont("arial", 28)
    
    surf = fonte.render(str(texto), True, cor)
    rect = surf.get_rect()
    if centralizado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    tela.blit(surf, rect)


def desenhar_texto_formatado(tela, texto, cor, rect, fonte):
    """
    Desenha um texto com quebra de linha, parágrafos e centralização vertical.
    """
    linhas_finais = []
    
    paragrafos = texto.split('\n\n')
    
    for paragrafo in paragrafos:
        palavras = paragrafo.replace('\n', ' ').split(' ')
        linha_atual = ""
        for palavra in palavras:
            
            linha_teste = linha_atual + palavra + " "
            if fonte.size(linha_teste)[0] < rect.width:
                linha_atual = linha_teste
            else:
                
                linhas_finais.append(linha_atual)
                linha_atual = palavra + " "
        linhas_finais.append(linha_atual)
        
        linhas_finais.append("")

    
    if linhas_finais and linhas_finais[-1] == "":
        linhas_finais.pop()

    
    altura_total_texto = len(linhas_finais) * fonte.get_linesize()
    
    y_inicial = rect.top + (rect.height - altura_total_texto) // 2
    
    
    for i, linha in enumerate(linhas_finais):
        superficie_linha = fonte.render(linha, True, cor)
        
        x_pos = rect.centerx - superficie_linha.get_width() // 2
        y_pos = y_inicial + i * fonte.get_linesize()
        tela.blit(superficie_linha, (x_pos, y_pos))

def desenhar_botao(tela, texto, x, y, w, h, cor_fundo, cor_hover, fonte, click_sound=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    ret = pygame.Rect(x, y, w, h)
    cor = cor_hover if ret.collidepoint(mouse) else cor_fundo
    pygame.draw.rect(tela, cor, ret, border_radius=8)
    if "\n" in texto:
        linhas = texto.split("\n")
        for i, linha in enumerate(linhas):
            desenhar_texto(
                tela, linha,
                x + w // 2,
                y + h // 2 - 20 + i*32 if len(linhas) == 2 else y + h // 2,
                BRANCO, True, fonte
            )
    else:
        desenhar_texto(tela, texto, x + w // 2, y + h // 2, BRANCO, True, fonte)
    if ret.collidepoint(mouse) and click[0]:
        if click_sound:
            try:
                click_sound.play()
            except:
                pass
        pygame.time.delay(150)
        return True
    return False

def desenhar_fundo_gradiente(tela, cor1, cor2):
    altura = tela.get_height()
    largura = tela.get_width()
    if altura <= 0: return
    for i in range(altura):
        proporcao = i / altura
        r = int(cor1[0] * (1 - proporcao) + cor2[0] * proporcao)
        g = int(cor1[1] * (1 - proporcao) + cor2[1] * proporcao)
        b = int(cor1[2] * (1 - proporcao) + cor2[2] * proporcao)
        pygame.draw.line(tela, (r, g, b), (0, i), (largura, i))


def desenhar_janela_central(tela, w, h, cor_fundo, cor_borda, titulo="", texto="", fonte_titulo=None, fonte_texto=None):
    if fonte_titulo is None:
        fonte_titulo = pygame.font.SysFont("arialblack", 40)
    if fonte_texto is None:
        fonte_texto = pygame.font.SysFont("arial", 28)

    cx, cy = tela.get_width() // 2, tela.get_height() // 2
    ret_fundo = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
    
    pygame.draw.rect(tela, cor_fundo, ret_fundo, border_radius=8)
    pygame.draw.rect(tela, cor_borda, ret_fundo, 3, border_radius=8)
    
    desenhar_texto(tela, titulo, cx, ret_fundo.top + 40, cor_borda, True, fonte_titulo)

    
    padding_vertical = 100 
    padding_horizontal = 40
    ret_texto = pygame.Rect(
        ret_fundo.left + padding_horizontal, 
        ret_fundo.top + padding_vertical, 
        w - padding_horizontal * 2, 
        h - padding_vertical * 1.5 
    )
    
    desenhar_texto_formatado(tela, texto, cor_borda, ret_texto, fonte_texto)

def desenhar_controle_volume(tela, x, y, fonte, volume, click_sound=None):
    w, h = 60, 60
    if desenhar_botao(tela, "-", x, y, w, h, (40,40,40), (80,80,80), fonte, click_sound):
        volume -= 0.1
    if desenhar_botao(tela, "+", x + w + 20, y, w, h, (40,40,40), (80,80,80), fonte, click_sound):
        volume += 0.1
    volume = max(0.0, min(1.0, volume))
    desenhar_texto(tela, f"Volume: {int(volume*100)}%", x + 2*w + 60, y + h//2, BRANCO, False, fonte)
    return volume

class MatrixRain:
    def __init__(self, largura, altura, fonte, tam_fonte=18, velocidade_min=1, velocidade_max=4):
        self.largura = largura
        self.altura = altura
        self.fonte = fonte
        self.tam_fonte = tam_fonte
        self.colunas = max(1, largura // tam_fonte)
        self.y_pos = [random.randint(-1000, 0) for _ in range(self.colunas)]
        self.vel = [random.randint(velocidade_min, velocidade_max) for _ in range(self.colunas)]
        self.caracteres = [chr(i) for i in range(33, 127)]

    def update_and_draw(self, tela):
        for i in range(self.colunas):
            char = random.choice(self.caracteres)
            try:
                surf = self.fonte.render(char, True, VERDE_MATRIX)
            except:
                surf = pygame.font.SysFont("consolas", self.tam_fonte).render(char, True, VERDE_MATRIX)
            x = i * self.tam_fonte
            y = self.y_pos[i] * self.tam_fonte
            if -self.tam_fonte <= y <= self.altura:
                tela.blit(surf, (x, y))
            self.y_pos[i] += self.vel[i]
            if self.y_pos[i] * self.tam_fonte > self.altura:
                self.y_pos[i] = random.randint(-20, 0)
                self.vel[i] = random.randint(1, 4)
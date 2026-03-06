# 🟢 Jogo da Vida: A Matrix

Um simulador de jogo de tabuleiro digital desenvolvido inteiramente em **Python** e **Pygame**, inspirado no universo de Matrix. O projeto vai muito além de um jogo simples, englobando controle complexo de estados (State Machine), renderização customizada de UI e algoritmos de probabilidade.

## 💻 Sobre o Projeto

O objetivo deste projeto foi aplicar conceitos avançados de lógica de programação, modularização de código e manipulação de assets visuais/sonoros. O jogo simula um tabuleiro em zigue-zague onde até 4 jogadores disputam uma corrida contra o sistema, enfrentando eventos aleatórios baseados no código-fonte do jogo.

### 🚀 Principais Destaques Técnicos
* **Máquina de Estados (State Machine):** Navegação fluida entre mais de 15 estados diferentes (Splash Screen, Loading, Menu, Cutscenes, Gameplay, Pausa, Tela de Fim).
* **Loading Dinâmico:** Sistema de carregamento assíncrono de assets (mais de 300 frames de animação e arquivos de áudio) com barra de progresso em tempo real.
* **Separação de Responsabilidades (Clean Code):**
  * `main.py`: Responsável pelo loop principal, controle de eventos (event listener) e renderização visual.
  * `jogo.py`: Isola toda a regra de negócio, algoritmos de tabuleiro, mecânicas de buff/nerf (probabilidades dinâmicas de 60/40) e controle de turnos.
  * `utils.py`: Biblioteca de componentes visuais reutilizáveis (botões customizados, formatação de textos em blocos, efeito Matrix Rain).
* **Efeitos Visuais Customizados:** Implementação matemática orientada a objetos do efeito "Matrix Rain" caindo na tela de fundo.

## 🛠️ Tecnologias Utilizadas
* **Python 3.x**
* **Pygame** (Engine gráfica e manipulação de áudio)
* Matemática e Probabilidade (`random`)
* Manipulação do Sistema (`os`, `sys`)

## 📂 Estrutura do Projeto

```text
📦 JOGO-DA-VIDA---A-MATRIX
 ┣ 📂 assets/                # Imagens, fontes, spritesheets e sons do jogo
 ┃ ┣ 📂 dados/               # Sprites de rolagem e faces do dado
 ┃ ┣ 📂 frames_cutscene/     # Frames renderizados para as cutscenes
 ┃ ┣ 📂 frames_splash/       # Animação de entrada
 ┃ ┣ 📂 images/              # Backgrounds e assets estáticos
 ┃ ┣ 📂 personagens/         # Sprites de movimentação dos peões
 ┃ ┗ 🎵 *.mp3 / *.wav        # Efeitos sonoros e trilhas
 ┣ 📜 main.py                # Ponto de entrada e Loop Principal da engine gráfica
 ┣ 📜 jogo.py                # Core da lógica de negócio e regras do tabuleiro
 ┗ 📜 utils.py               # Funções auxiliares de renderização gráfica e UI

⚙️ Como Executar
Certifique-se de ter o Python instalado na sua máquina.

Clone este repositório:

Bash
git clone [https://github.com/SEU_USUARIO/jogo-da-vida-matrix.git](https://github.com/SEU_USUARIO/jogo-da-vida-matrix.git)
Instale a dependência do Pygame:

Bash
pip install pygame
Execute o arquivo principal:

Bash
python main.py

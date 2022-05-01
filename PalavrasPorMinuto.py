#Programa Iniciantes Python- Jogo Palavras Por Minuto by @guicstefani
#Obs: Você precisa ter o curses no seu computador para importá-lo
import curses
from curses import wrapper
import time #importante para calcular o tempo das PPM
import random #precisa para que os textos sejam exibidos aleatoriamente
import io #para poder usar acentos sem bugar


#Começamos com a tela inicial
def tela_inicial(stdscr):
	stdscr.clear() # o comando clear é pra eliminar o texto anterior
	stdscr.addstr("Seja bem vindo! Descubra quantas Palavras por Minuto você escreve!")
	stdscr.addstr("\nAperte qualquer tecla para começar :)") 
	stdscr.refresh() # o comando refresh é pra atualizar/ mudar a página
	stdscr.getkey() #Esse comando serve pra identificar que tecla o jogador clicou

#parâmetros da função, ppm=0 significa que é opcional, vamos usar ele depois
def mostrar_texto(stdscr, texto_doTeste, texto_usuario, ppm = 0):
	stdscr.addstr(texto_doTeste)
	stdscr.addstr(2,0, f"PPM: {ppm}")

#definindo varíavel de cor
	for i, char in enumerate(texto_usuario):
		char_correto = texto_doTeste [i]
		color = curses.color_pair(1) #cor verde para correto
		if char != char_correto:
		    color = curses.color_pair(2) #cor vermelha para incorreto

		stdscr.addstr(0, i, char, color)

#essa função irá indicar o texto a ser escrito no teste de ppm, para isso é necessário ter uma arquivo txt na mesma pasta desse arquivo.
#encoding e io serve para o programa ler caracteres especiais
def carregar_textos():
	with io.open("TextosPPM.txt", "r", encoding="utf8") as f:
		frases = f.readlines()
		return random.choice (frases).strip()

#aqui configuramos a matemática e a lógica para o cálculo das Palavras por Minuto ocorrerem simultaneamente enquanto o usuário digita o texto
def ppm_teste(stdscr):
	texto_doTeste = carregar_textos()
	texto_usuario = []
	ppm = 0
	temporizador_inicio = time.time()
	stdscr.nodelay(True)

	while True:
		temporizador_iniciado = max(time.time() - temporizador_inicio, 1)
		ppm = round((len(texto_usuario) / (temporizador_iniciado / 60)) / 5) #dessa maneira se você digitar 30 palavras em 30 segundos sua PPM = 60

		stdscr.clear()
		mostrar_texto(stdscr, texto_doTeste, texto_usuario, ppm)

		stdscr.refresh() 
		#aqui colocamos a finalização da rodada, quando o usuário escrever tudo corretamente e assim poder continuar jogando
		if "".join(texto_usuario) == texto_doTeste:
			stdscr.nodelay(False)
			break

		try:
			key = stdscr.getkey()
		except:
			continue

#esse if indica que se você clicar no 'esc' você consegue sair do programa
		if ord(key) == 27:
			break
		if key in("KEY_BACKSPACE", '\b', '\x7f'):
			if len(texto_usuario) > 0:
				texto_usuario.pop()
		elif len(texto_usuario) < len (texto_doTeste):
			texto_usuario.append(key)


def main(stdscr):
	curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
	#essa cores indicam que quando verde = texto correto, quando vermelho texto incorreto, em branco o texto do teste e o fundo sempre preto.

	tela_inicial(stdscr)
	while True:
		ppm_teste(stdscr)
		stdscr.addstr(3, 0, "Você completou o teste! Aperte qualquer tecla para continuar...")
		key = stdscr.getkey()

		if ord(key) == 27:
			break

wrapper(main)
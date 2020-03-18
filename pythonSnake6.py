import curses
from curses import KEY_RIGHT, KEY_UP, KEY_LEFT, KEY_DOWN
import time
from random import randint

class Jeu:
	def __init__(self, hauteur: int, largeur: int):
		print(f"Construction d'un objet de la classe Jeu de dimension {hauteur}x{largeur}")
		self.largeur = largeur
		self.hauteur = hauteur
		self.niveau = 1
		self.score = 0

	def afficher_banniere(self, titre: tuple) -> None:
		redimentionnement_terminal = f"\x1b[8;{len(titre) + 2};{self.largeur}t"
		print(redimentionnement_terminal)
		print('\x1b[1J')
		for ligne in titre:
			print(ligne)
		time.sleep(2)
		redimentionnement_terminal = f"\x1b[8;{self.hauteur};{self.largeur}t"
		print(redimentionnement_terminal)
		print('\x1b[1J')
		time.sleep(1)

	def affichage_aire_de_jeu(self, titre: str) -> curses:
		curses.initscr()
		curses.start_color()
		curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
		curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_YELLOW)
		curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
		win = curses.newwin(self.hauteur, self.largeur, 0, 0)
		win.keypad(1)
		curses.noecho()
		curses.curs_set(0)
		win.nodelay(1)
		win.box()
		win.addstr(0, self.largeur // 2 - len(titre) // 2, titre, curses.color_pair(2))
		win.refresh()
		curses.beep()
		self.window = win
		return self.window

	def fin(self) -> None:
		curses.beep()
		curses.endwin()
		redimentionnement_terminal = f"\x1b[8;10;80t"
		print(redimentionnement_terminal)
		print('\n\n\n')
		print(f'Votre score est de : {self.score}')
		print('\n\n\n')

	def controle(self, key: int = KEY_RIGHT, keys: tuple = (KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_UP, 27)) -> int:
		old_key = key
		key = self.window.getch()
		if key == -1 or key not in keys:
			key = old_key
		return key

	def affiche_score(self):
		self.window.addstr(0, 2, 'Score : ' + str(self.score) + ' ')
		self.window.addstr(0, self.largeur - 16, 'Niveau : ' + str(self.niveau) + ' ')
		self.window.refresh()

	def perdu(self, snake):
		end = False
		if snake.tete() in snake.corps():
			self.window.addstr(self.hauteur // 2,
							   self.largeur // 2 - 4,
							   'GAME OVER !', curses.color_pair(4))
			self.window.refresh()
			curses.napms(2000)
			end = True
		return end

	def calcul_niveau(self) -> int:
		self.niveau += (self.score % 5 == 0)
		if self.niveau > 10:
			self.niveau = 10
		if self.niveau < 1:
			self.niveau = 1
		return self.niveau


class Pomme:
	def __init__(self, win: curses):
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
		self.coordonnees = [0, 0]
		self.window = win

	def afficher(self):
		self.coordonnees[0] = randint(1, self.window.getmaxyx()[0] - 2)
		self.coordonnees[1] = randint(1, self.window.getmaxyx()[1] - 2)
		self.window.addch(self.coordonnees[0], self.coordonnees[1], chr(211), curses.color_pair(1))
		self.window.refresh()

	def get_xy(self) -> list:
		return self.coordonnees


class Serpent:
	def __init__(self, win: curses):
		curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_YELLOW)
		self.snake = [[4, 10], [4, 9], [4, 8]]
		self.window = win

	def afficher(self):
		for i in range(len(self.snake)):
			self.window.addstr(self.snake[i][0], self.snake[i][1], '*', curses.color_pair(3))
			self.window.refresh()

	def corps(self) -> list:
		return self.snake[1:]

	def tete(self) -> list:
		return self.snake[0]

	def deplacement(self, key: int, niveau: int) -> list:

		# si la touche est KEY_RIGHT : ajouter la tête une colonne à droite
		if key == KEY_RIGHT:
			self.snake.insert(0, [self.tete()[0], self.tete()[1] + 1])

		# # si la touche est KEY_LEFT : ajouter la tête une colonne à gauche
		elif key == KEY_LEFT:
			self.snake.insert(0, [self.tete()[0], self.tete()[1] - 1])

		# si la touche est KEY_UP : ajouter la tête une ligne au dessus
		elif key == KEY_UP:
			self.snake.insert(0, [self.tete()[0] - 1, self.tete()[1]])

		# si la touche est KEY_DOWN : ajouter la tête une ligne en dessous
		elif key == KEY_DOWN:
			self.snake.insert(0, [self.tete()[0] + 1, self.tete()[1]])

		# Si la tête du serpent touche les bords de l'aire de jeu
		if self.tete()[0] == 0:
			self.tete()[0] = self.window.getmaxyx()[0] - 2
		if self.tete()[1] == 0:
			self.tete()[1] = self.window.getmaxyx()[1] - 2
		if self.tete()[0] == self.window.getmaxyx()[0] - 1:
			self.tete()[0] = 1
		if self.tete()[1] == self.window.getmaxyx()[1] - 1:
			self.tete()[1] = 1

		# Attendre un peu en fonction du niveau
		self.window.timeout(int(150 * (1 / niveau + 1 / (niveau * 2))))

		return self.snake

	def mange_pomme(self, win: curses, pommes: list) -> bool:
		miam = False
		for pomme in pommes:
			if self.tete() == pomme.get_xy():
				curses.beep()
				miam = True
				pomme.afficher()
				while pomme.get_xy() in self.snake:
					pomme.afficher()
		if not miam:
			win.addstr(self.snake[-1][0], self.snake[-1][1], ' ', curses.color_pair(1))
			win.refresh()
			self.snake.pop()
		return miam


if __name__ == '__main__':

	mon_jeu = Jeu(40, 120)
	assert isinstance(mon_jeu, Jeu)
	print(type(mon_jeu))
	key = KEY_RIGHT

	banniere = ("     _______     _________ _    _  ____  _   _    _____ _   _          _  ________ ",
				"    |  __ \ \   / |__   __| |  | |/ __ \| \ | |  / ____| \ | |   /\   | |/ |  ____|",
				"    | |__) \ \_/ /   | |  | |__| | |  | |  \| | | (___ |  \| |  /  \  |   /| |__   ",
				"    |  ___/ \   /    | |  |  __  | |  | | . ` |  \___ \| . ` | / /\ \ |  < |  __|  ",
				"    | |      | |     | |  | |  | | |__| | |\  |  ____) | |\  |/ ____ \| . \| |____ ",
				"    |_|      |_|     |_|  |_|  |_|\____/|_| \_| |_____/|_| \_/_/    \_|_|\_|______|")

	mon_jeu.afficher_banniere(banniere)

	window = mon_jeu.affichage_aire_de_jeu("PYTHON SNAKE")
	les_pommes = []
	une_pomme = Pomme(window)
	une_pomme.afficher()
	la_pomme_en = une_pomme.get_xy()
	les_pommes.append(une_pomme)

	un_serpent = Serpent(window)
	un_serpent.afficher()
	niveau = 1
	precedant_niveau = 1
	ta_perdu = False
	mon_jeu.affiche_score()

	while key != 27 and not ta_perdu:
		mon_jeu.affiche_score()
		key = mon_jeu.controle(key)
		un_serpent.deplacement(key, niveau)
		if un_serpent.mange_pomme(window, les_pommes):
			mon_jeu.score += 1

			niveau = mon_jeu.calcul_niveau()
			if niveau > precedant_niveau:
				une_nouvelle_pomme = Pomme(window)
				une_nouvelle_pomme.afficher()
				les_pommes.append(une_nouvelle_pomme)
				precedant_niveau = niveau
		un_serpent.afficher()
		ta_perdu = mon_jeu.perdu(un_serpent)

	mon_jeu.fin()



import curses
import time
from random import randint

class Jeu:
	def __init__(self, hauteur: int, largeur: int):
		print(f"Construction d'un objet de la classe Jeu de dimension {hauteur}x{largeur}")
		self.largeur = largeur
		self.hauteur = hauteur
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
		curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
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
		return win

	def fin(self) -> None:
		curses.beep()
		curses.endwin()
		redimentionnement_terminal = f"\x1b[8;10;80t"
		print(redimentionnement_terminal)
		print('\n\n\n')
		print(f'Votre score est de : {self.score}')
		print('\n\n\n')


class Pomme:
	def __init__(self, win: curses):
		pass


class Serpent:
	def __init__(self, win: curses):
		pass


if __name__ == '__main__':

	mon_jeu = Jeu(40, 120)
	assert isinstance(mon_jeu, Jeu)
	print(type(mon_jeu))

	banniere = ("     _______     _________ _    _  ____  _   _    _____ _   _          _  ________ ",
				"    |  __ \ \   / |__   __| |  | |/ __ \| \ | |  / ____| \ | |   /\   | |/ |  ____|",
				"    | |__) \ \_/ /   | |  | |__| | |  | |  \| | | (___ |  \| |  /  \  |   /| |__   ",
				"    |  ___/ \   /    | |  |  __  | |  | | . ` |  \___ \| . ` | / /\ \ |  < |  __|  ",
				"    | |      | |     | |  | |  | | |__| | |\  |  ____) | |\  |/ ____ \| . \| |____ ",
				"    |_|      |_|     |_|  |_|  |_|\____/|_| \_| |_____/|_| \_/_/    \_|_|\_|______|")

	mon_jeu.afficher_banniere(banniere)

	window = mon_jeu.affichage_aire_de_jeu("PYTHON SNAKE")

	curses.napms(2000)
	mon_jeu.fin()



import random  # losowanie polozenia bomb


import gi
# wymagamy biblioteki w wersji min 3.0
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Plansza(Gtk.Window):
    """klasa zawierajaca gre."""
    def nowa_gra(self, btn):
        """resetuje gre."""
        self.wolne = self.rozmiar * (self.rozmiar - 1)
        self.tablica = [[0 for col in range(self.rozmiar + 1)] for row in range(self.rozmiar + 1)]
        for i in range(self.rozmiar):
            self.tablica[random.randint(0, self.rozmiar - 1)][random.randint(0, self.rozmiar - 1)] = 9
        for i in range(self.rozmiar):
            for j in range(self.rozmiar):
                self.buttons[i][j].get_child().set_markup("{}-{}".format(i, j))
                self.buttons[i][j].set_sensitive(True)
                if self.tablica[i][j] == 0:
                    if self.tablica[i - 1][j - 1] == 9:
                        self.tablica[i][j] += 1
                    if self.tablica[i - 1][j] == 9:
                        self.tablica[i][j] += 1
                    if self.tablica[i - 1][j + 1] == 9:
                        self.tablica[i][j] += 1
                    if self.tablica[i][j - 1] == 9:
                        self.tablica[i][j] += 1
                    if self.tablica[i][j + 1] == 9:
                        self.tablica[i][j] += 1
                    if self.tablica[i + 1][j - 1] == 9:
                        self.tablica[i][j] += 1
                    if self.tablica[i + 1][j] == 9:
                        self.tablica[i][j] += 1
                    if self.tablica[i + 1][j + 1] == 9:
                        self.tablica[i][j] += 1

    def __init__(self):
        """Inicjuje powstanie planszy. """
        self.window = Gtk.Window()
        self.window.set_title("saper")
        self.window.set_default_size(200, 200)
        self.window.connect("delete-event", lambda x, y: Gtk.main_quit())


        #okresla wielkosc planszy
        self.rozmiar = 5
        self.wolne = 0
        self.tablica = []
        self.znaki_tab = dict([(9, '<span foreground="red"><b>m</b></span>'),
                               (0, '<span foreground="black"><b>0</b></span>'),
                               (1, '<span foreground="blue"><b>1</b></span>'),
                               (2, '<span foreground="orange"><b>2</b></span>'),
                               (3, '<span foreground="tomato"><b>3</b></span>'),
                               (4, '<span foreground="brown"><b>4</b></span>'),
                               (5, '<span foreground="brown"><b>5</b></span>'),
                               (6, '<span foreground="brown"><b>6</b></span>'),
                               (7, '<span foreground="brown"><b>7</b></span>'),
                               (8, '<span foreground="brown"><b>8</b></span>')])


        # ukladam przyciski na siatce
        grid = Gtk.Grid()
        self.buttons = []
        for i in range(self.rozmiar):
            self.buttons.append([])
            for j in range(self.rozmiar):
                b = Gtk.Button.new_with_label("{}-{}".format(i, j))
                self.buttons[i].append(b)
                grid.attach(b, i, j, 1, 1)
                b.connect("clicked", self.kliknieto, i, j)

        # dodaje przycisk nowa gra
        b = Gtk.Button(label="Nowa gra")
        self.buttons.append(b)

        grid.attach(b, 0, self.rozmiar+1, self.rozmiar, 1)
        b.connect("clicked", self.nowa_gra)
        self.window.add(grid)
        # kolumny maja miec identyczna szerokosc, wiersze identyczna wysokosc
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        self.nowa_gra("clicked")
        self.window.show_all()

    def nowa_gra_wiadomocs(self, btn):
        """Tworzy nowa gre i zamyka okno wyniku."""
        self.nowa_gra("clicked")
        self.wiadomosc.destroy()

    def wiad(self, tutul):
        """Otwiera okno z informacjo o wyniku gry."""
        for i in range(self.rozmiar):
            for j in range(self.rozmiar):
                self.buttons[i][j].set_sensitive(False)

        self.wiadomosc = Gtk.Window()
        self.wiadomosc.set_title(tutul)
        self.wiadomosc.set_default_size(400, 100)
        b = Gtk.Button("Nowa gra")
        b.connect("clicked", self.nowa_gra_wiadomocs)
        self.wiadomosc.add(b)
        self.wiadomosc.show_all()

    def ruch(self, x, y):
        """Wykonuje ruch gracza."""
        # Przysisk to kontener ktory zawiera tylko jednego potomka: labelke.
        # Na labelce moge wywolac metode set_markup
        self.buttons[x][y].get_child().set_markup(self.znaki_tab[self.tablica[x][y]])
        self.buttons[x][y].set_sensitive(False)
        self.wolne -= 1

    def kliknieto(self, btn, x, y):
        """obsluguje klikniecie w plansze."""
        self.ruch(x, y)
        if self.tablica[x][y] != 9:
            if self.wolne == 0:
                self.wiad("Wygrana")
        else:
                for i in range(self.rozmiar):
                    for j in range(self.rozmiar):
                        self.buttons[i][j].get_child().set_markup(self.znaki_tab[self.tablica[i][j]])
                self.wiad("Przegrana")


class App(object):
    """Klasa otwiera gre."""
    def __init__(self):
        """Inicjuje otwarcie gry."""
        self.window = Plansza()

if __name__ == "__main__":
    a = App()
    Gtk.main()
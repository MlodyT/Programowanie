import pygame
import math
import random
import time
import os
import string

with open("tekst.txt", "r", encoding="utf8") as file:
    content = "".join(file.readlines())

with open("zasady.txt", "r", encoding="utf8") as file:
    zasady_string = "".join(file.readlines())

if os.path.isfile("wyniki.txt") == False:
    wyniki = open("wyniki.txt", "x")

pygame.mixer.init()

hurt_sound = pygame.mixer.Sound("male_hurt.mp3")
hurt_sound.set_volume(0.1)

death_sound = pygame.mixer.Sound("male_death.mp3")
death_sound.set_volume(0.2)

jump_sound = pygame.mixer.Sound("jump.mp3")
jump_sound.set_volume(0.1)

pygame.init()

długość = 800
wysokość = 350

screen_color = (111, 59, 19)
color_light = (196,181,142) 
color_white = (255,255,255) 
color_black = (0, 0, 0)
color_dark = (187,162,119)

tytuł = "Wild West Run"
big_font_size = 40
normal_font_size = 20
no_results_font_size = 30
best_score_font_size = 45
menu_font_name = "Sancreek.ttf"
font_menu = pygame.font.Font(menu_font_name, big_font_size)
font_second = pygame.font.SysFont("bahnschrift", normal_font_size)
font_no_results = pygame.font.SysFont("bahnschrift", no_results_font_size)
font_best_score = pygame.font.SysFont("bahnschrift", best_score_font_size)
font_saving = pygame.font.Font(menu_font_name, no_results_font_size )

running = True
menu_window = True
game_window = False
rules_window = False
settings_window = False
scoretable_window= False
autorinfo_window = False
gameover_window = False

screen = pygame.display.set_mode([długość, wysokość])
pygame.display.set_caption(tytuł)

class Text():
 
    """
    Klasa reprezentująca tekst w postaci string.

    ...

    Atrybuty
    ----------
    text : string
        tekst jaki będzie chcieli przedstawiać    
    font : pygame.font.Font
        czcionka w jakiej wyświetlany ma być tekst, wygenerowana przy pomocy pygame
    text_color : tuple
        kolor w jakim ma być wyświetlany tekst

    Metody
    -------
    draw_text(display, x, y):
        Rysuje tekst na zadanym ekranie wp odanym miejscu.
    split_text(display, x, y):
        Rysuje długi tekst na zadanym ekranie, przenosząc słowa do nastepnej linijki, gdy się nie mieszczą.
    draw_center_text(display, x_start, y_start, width, height):
        Rysuje wycentrowany tekst na zadanym obszarze ekranu.
    """

    def __init__(self, text, font, text_color):

        """
        Tworzy wszystkie wymagane atrybuty dla obiektu z klasy Text.

        Parametry
        ----------
            text : string
                Tekst jaki będzie chcieli przedstawiać.   
            font : pygame.font.Font
                Czcionka w jakiej wyświetlany ma być tekst, wygenerowana przy pomocy pygame.
            text_color : tuple
                Kolor w jakim ma być wyświetlany tekst, przedstawiony przy pomocy krotki w formacie RGB.
        """
        
        self.text = text
        self.font = font
        self.text_color = text_color

    def draw_text(self, display, x, y):

        """
        Rysuje tekst na podanym przez nas ekranie i miejscu.

        Najpierw renderuje tkst, a nsetępnie wyświetla go na ekranie, przy pomocy funkcji blit.

        Parametry
        ----------
        display: pygame.surface.Surface
            Ekran, na którym ma być wyświetlany nasz tekst.
        x : int
            Współrzędną x miejsca, w którym zacnie być rysowany lewy róg naszego tekstu.
        y : int
            Współrzędną x miejsca, w którym zacnie być rysowany lewy róg naszego tekstu.

        Zwraca
        -------
        Brak
        """

        text_image = self.font.render(self.text, True, self.text_color)
        display.blit(text_image, (x, y))

    def split_text(self, display, x, y):

        """
        Rysuje długi tekst na podanym przez nas ekranie i miejscu, jednak gdy słowa nie mieszczą się już w linijce przenosi je do następnej.

        Najpierw dzieli tekst na pojedyncze słowa, a następnie sprawdza czy to słowo wraz ze spacją będzie dalej mieściło się w tej samej linijce tj. cześć liter nie przekroczy maksymalnej współrzędnej x  okna gry.

        Gdy słowo się nie mieści przenosi je do następnej linijki, zerując x i dodając do y wysokość słowa.

        Parametry
        ----------
        display: pygame.surface.Surface
            Ekran, na którym ma być wyświetlany nasz tekst.
        x : int
            Współrzędną x miejsca, w którym zacnie być rysowany lewy róg naszego tekstu.
        y : int
            Współrzędną x miejsca, w którym zacnie być rysowany lewy róg naszego tekstu.

        Zwraca
        -------
        Brak
        """

        words = [word.split(" ") for word in self.text.splitlines()]
        space = self.font.size(" ")[0]
        max_width = display.get_size()[0]
        x_start = x
        for line in words:
            for word in line:
                text_image = self.font.render(word, 0, self.text_color)
                word_width, word_height = text_image.get_size()
                if x + word_width >= max_width:
                    x = x_start
                    y = y + word_height
                display.blit(text_image, (x, y))
                x =  x + word_width + space
            x = x_start
            y = y + word_height

    def draw_center_text(self, display, x_start, y_start, width, heigth):

        """
        Rysuje wycemtrowany tekst na podanym obszre ekranu.

        Najpierw genruje nasz tekst.
        
        Następnie przy pmocy rozmiaru tekstu oblicza w blicie, gdzie trzeba zacząć rysować lewy góny róg tekstu, aby tekst znalazł się w centrum naszego obszaru.

        Parametry
        ----------
        display: pygame.surface.Surface
            Ekran, na którym ma być wyświetlany nasz tekst.
        x_start : int
            Współrzędna x lewego górnego rogu naszego obszaru.
        y_start : int
            Współrzędna x lewego górnego rogu naszego obszaru.
        width : int
            Szerokość zadanego obszaru.
        heigth : int
            Wysokość zadanego obszaru.

        Zwraca
        -------
        Brak
        """

        text_image = self.font.render(self.text, True , self.text_color)
        word_width, word_height = text_image.get_size()
        display.blit(text_image, (x_start + (width - word_width)/2, y_start + (heigth - word_height)/2))

class Button():

    """
    Klasa reprezentująca przycisk.

    ...

    Atrybuty
    ----------
    x : int
        Współrzędna x lewego górengo rogu, obszaru, w którym będzie reagować nasz przycisk.
    y : int
        Współrzędna y lewego górengo rogu, obszaru, w którym będzie reagować nasz przycisk.
    width : int
        Szerokość obszaru, w którym będzie reagować nasz przycisk.
    heigth : int
        Wysokość obszaru, w którym będzie reagować nasz przycisk.
    xdraw : int
        Współrzędna x lewego górengo rogu, obszaru, w którym nasz przycisk będzie narysowany.
    ydraw : int
        Współrzędna y lewego górengo rogu, obszaru, w którym nasz przycisk będzie narysowany.
    widthdraw : int
        Szerokość obszaru, w którym nasz przycisk będzie narysowany.
    heigthdraw : int
        Wysokość obszaru, w którym nasz przycisk będzie narysowany.
    button_color_notfocused : tuple
        Kolor przycisku, gdy nie najedziemy na niego myszką.
    button_color_focused : tuple
        Kolor przycisku, gdy najedziemy na niego myszką.
    focus : bool
        Wartość logiczna True, gdy najedzie się na przycisk myszką, inaczej False.
    clicked : bool
        Wartość logiczna True, gdy najedzie się na przycisk myszką, inaczej False.

    Metody
    -------
    showButton(dispaly):
        Rysuje przycisk na ekranie.
    focusCheck(display):
        Zmienia kolor przycisku, gdy najedzie się na niego myszką, a dodatkowo zwraca atrybut focus.
    clickedCheck():
        Sprawdza czy przycisk został klikniety i zwraca atrybut clicked.
    """

    def __init__(self, x, y, width, heigth, xdraw, ydraw, widthdraw, heigthdraw, button_color_notfocused, button_color_focused):
        
        """
        Tworzy wszystkie wymagane atrybuty dla obiektu z klasy Button.

        Parametry
        ----------
            x : int
                Współrzędna x lewego górengo rogu, obszaru, w którym będzie reagować nasz przycisk.
            y : int
                Współrzędna y lewego górengo rogu, obszaru, w którym będzie reagować nasz przycisk.
            width : int
                Szerokość obszaru, w którym będzie reagować nasz przycisk.
            heigth : int
                Wysokość obszaru, w którym będzie reagować nasz przycisk.
            xdraw : int
                Współrzędna x lewego górengo rogu, obszaru, w którym nasz przycisk będzie narysowany.
            ydraw : int
                Współrzędna y lewego górengo rogu, obszaru, w którym nasz przycisk będzie narysowany.
            widthdraw : int
                Szerokość obszaru, w którym nasz przycisk będzie narysowany.
            heigthdraw : int
                Wysokość obszaru, w którym nasz przycisk będzie narysowany.
            button_color_notfocused : tuple
                Kolor przycisku, gdy nie najedziemy na niego myszką.
            button_color_focused : tuple
                Kolor przycisku, gdy najedziemy na niego myszką.
            focus : bool, nie wprowadza się go
                Wartość logiczna True, gdy najedzie się na przycisk myszką, inaczej (w tym domyślnie) False.
            clicked : bool, nie wprowadza się go
                Wartość logiczna True, gdy najedzie się na przycisk myszką, inaczej (w tym domyślnie) False.
        """

        self.x = x
        self.y = y
        self.width = width
        self.heigth = heigth
        self.xdraw = xdraw
        self.ydraw = ydraw
        self.widthdraw = widthdraw
        self.heigthdraw = heigthdraw
        self.button_color_notfocused = button_color_notfocused
        self.button_color_focused = button_color_focused
        self.focus = False
        self.clicked = False
 
    def showButton(self, display):
        """
        Rysuje przycisk na zadanym ekranie tekst przy pomocy metody draw.

        Parametry
        ----------
        display: pygame.surface.Surface
            Ekran, na którym ma być wyświetlany nasz przycisk.

        Zwraca
        -------
        Brak
        """

        pygame.draw.rect(display, self.button_color_notfocused,[self.xdraw, self.ydraw, self.widthdraw, self.heigthdraw])
            
    def focusCheck(self, display):
        """
        Sprawdza pozycję myszki, gdy najedzie na przycisk, zmienia jego kolor oraz zmienia atrybut focus na True, inaczej zmienia atrybut focus na False.

        Na konie zwraca atrybut focus.

        Parametry
        ----------
        display: pygame.surface.Surface
            Ekran, na którym ma być wyświetlany nasz przycisk.
        
        Zwraca
        -------
        focus: bool
            Gdy na przycisk najechano myszką True, inaczej False.
        """

        mouse = pygame.mouse.get_pos()

        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.heigth:
            pygame.draw.rect(display, self.button_color_focused,[self.xdraw, self.ydraw, self.widthdraw, self.heigthdraw])
            self.focus = True
        else:
            self.focus = False
        
        return self.focus
        
    def clickedCheck(self):
        """
        Sprawdza pozycję myszki, gdy najedzie na przycisk i go kliknie zmienia atrybut clicked na True, inaczej zmienia atrybut clicked na False.

        Na konie zwraca atrybut clicked.

        Parametry
        ----------
        Brak
        
        Zwraca
        -------
        clicked: bool
            Gdy na przycisk kliknięto myszką True, inaczej False.
        """

        mouse = pygame.mouse.get_pos()

        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.heigth:
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
        else:
            self.clicked = False
        
        return self.clicked

class Player():
    """
    Klasa reprezentująca gracza.

    ...

    Atrybuty
    ----------
    running_image1 : pygame.surface.Surface
        Obraz przedstawiający jedną z dwóch animacji bieagnia gracza.
    running_image2 : pygame.surface.Surface
        Obraz przedstawiający drugą animację bieagnia gracza.
    jumping_image : pygame.surface.Surface
        Obraz przedstawiający animację skoku gracza.
    hurt_image : pygame.surface.Surface
        Obraz przedstawiający animację otrzymania obrażeń przez gracza.
    image : pygame.surface.Surface
        Aktualnie wyświetla animacja gracza.
    rect : pygame.rect.Rect
        Obiekt przechowujący informację o półożeniu, szerokości i wyokości gracza.
    rect.x : int
        Współrzędna x lewego górnego rogu miejsca, w którym wyświetlany jest gracz.
    rect.y : int
        Współrzędna x lewego górnego rogu miejsca, w którym wyświetlany jest gracz.
    is_jumping_and_falling : bool
        Zmienna logiczna mówiąca czy gracz jest w fazie lotu bądź spadania.
    jump_height : int
        Wartość ograniczająca wysokość skoku gracza.
    jump_speed : int
        Wartość kontrolująca szybkość skoku gracza.
    jump_count : int
        Wartość kontrolująca wysokość skoku gracza.
    fall_speed : int
        Wartość kontrolująca szybkość spadania gracza.
    default_position : tuple
        Krotka z domyślną pozycją gracza.
    running_frames : list
        Lista z obrazami potrzebnymi do animacji biegu.
    current_frame : int
        Zmienna kontrolująca, na której jest się kaltce przy animacji biegu.
    lives : int
        Ilość żyć posiadanych przez gracza.
    score : int
        Punkty zgromadzone przez gracza.
    is_hurt : bool
        Zmienna logiczna mówiąca czy gracz otrzymał obrażenia.

    Metody
    -------
    status():
        Uaktualnia pozycję i animację gracza.
    show_lives():
        Wyświetla ilość pozostałych żyć graczowi.
    show_score():
        Wyświetla wynik gracza.
    """

    def __init__(self, x, y):
        """
        Tworzy wszystkie wymagane atrybuty dla obiektu z klasy Player.

        Parametry
        ----------
            running_image1 : pygame.surface.Surface
                Obraz przedstawiający jedną z dwóch animacji bieagnia gracza, nie  wprowadza się.
            running_image2 : pygame.surface.Surface
                Obraz przedstawiający drugą animację bieagnia gracza, nie  wprowadza się.
            jumping_image : pygame.surface.Surface
                Obraz przedstawiający animację skoku gracza, nie  wprowadza się.
            hurt_image : pygame.surface.Surface
                Obraz przedstawiający animację otrzymania obrażeń przez gracza, nie  wprowadza się.
            image : pygame.surface.Surface
                Aktualnie wyświetla animacja gracza, nie  wprowadza się (domyślnie pierwsza z animacji biegu).
            rect : pygame.rect.Rect
                Obiekt przechowujący informację o półożeniu, szerokości i wyokości gracza, nie  wprowadza się, równa self.image.rect z zamienionymi współrzędnymi x i y.
            rect.x : int
                Współrzędna x lewego górnego rogu miejsca, w którym wyświetlany jest gracz.
            rect.y : int
                Współrzędna x lewego górnego rogu miejsca, w którym wyświetlany jest gracz.
            is_jumping_and_falling : bool
                Zmienna logiczna mówiąca czy gracz jest w fazie lotu bądź spadania, nie  wprowadza się (domyślnie False).
            jump_height : int
                Wartość ograniczająca wysokość skoku gracza, nie  wprowadza się (domyślnie 24).
            jump_speed : int
                Wartość kontrolująca szybkość skoku gracza, nie  wprowadza się (domyślnie 10).
            jump_count : int
                Wartość kontrolująca wysokość skoku gracza, nie  wprowadza się (domyślnie 0).
            fall_speed : int
                Wartość kontrolująca szybkość spadania gracza, nie  wprowadza się (domyślnie 8).
            default_position : tuple
                Krotka z domyślną pozycją gracza.
            running_frames : list
                Lista z obrazami potrzebnymi do animacji biegu, nie  wprowadza się (domyślnie 4 pierwsze animacj i potem 4 drugie).
            current_frame : int
                Zmienna kontrolująca, na której jest się kaltce przy animacji biegu (domyślnie 0).
            lives : int
                Ilość żyć posiadanych przez gracza (domyślnie 3).
            score : int
                Punkty zgromadzone przez gracza (domyślnie 0).
            is_hurt : bool
                Zmienna logiczna mówiąca czy gracz otrzymał obrażenia (domyślnie False).
        """

        self.running_image1 = pygame.image.load("soldier_walk1.png")
        self.running_image2 = pygame.image.load("soldier_walk2.png")
        self.jumping_image = pygame.image.load("soldier_jump.png")
        self.hurt_image = pygame.image.load("soldier_hurt.png")
        self.image = self.running_image1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_jumping_and_falling = False
        self.jump_height = 24
        self.jump_speed = 10
        self.jump_count = 0
        self.fall_speed = 8
        self.default_position = (x, y)
        self.running_frames = [self.running_image1, self.running_image1, self.running_image1, self.running_image1,
                               self.running_image2, self.running_image2, self.running_image2, self.running_image2]
        self.current_frame = 0
        self.lives = 3
        self.score = 0
        self.is_hurt = False
    
    def status(self):

        """
        Aktualizuje pozycję i animację gracza, robiać to zależenie od atrybutów is_jumping_and_fallin i is_hurt.

        Podczas biegu zmienia odpoiwednio animacje biegania.

        Parametry
        ----------
        Brak
        
        Zwraca
        -------
        Brak
        """

        if self.is_jumping_and_falling:
            if self.jump_count < self.jump_height:
                self.rect.y -= self.jump_speed
                self.jump_count += 1
                if self.is_hurt:
                    self.image = self.hurt_image
                else:
                    self.image = self.jumping_image
                screen.blit(self.image, (self.rect.x, self.rect.y))
            elif self.rect.y < self.default_position[1]:
                self.rect.y += self.fall_speed
                if self.is_hurt:
                    self.image = self.hurt_image
                    self.is_hurt = False
                else:
                    self.image = self.jumping_image
                screen.blit(self.image, (self.rect.x, self.rect.y))
            else:
                self.is_jumping_and_falling = False
                self.jump_count = 0
        else:
            if self.is_hurt:
                self.image = self.hurt_image
                self.is_hurt = False
            else:
                self.image = self.jumping_image
                frame = self.running_frames[self.current_frame]
                self.image = frame
                self.current_frame = (self.current_frame + 1) % len(self.running_frames)
            screen.blit(self.image, (self.rect.x, self.rect.y))
        
    
    def show_lives(self):

        """
        Wyświetla na ekranie ilość żyć gracza.

        Parametry
        ----------
        Brak
        
        Zwraca
        -------
        Brak
        """

        left_lives = self.lives
        text = font_second.render(f"Życia: {left_lives}", True , (0, 0, 0))
        screen.blit(text, (10, 10))

    def show_score(self):

        """
        Wyświetla na ekranie ilość punktów zgromadzonych przez gracza.

        Parametry
        ----------
        Brak
        
        Zwraca
        -------
        Brak
        """

        gained_score = self.score
        text = font_second.render(f"Wynik: {gained_score}", True , (0, 0, 0))
        screen.blit(text, (300, 10))
        

class Cactus():

    """
    Klasa reprezentująca gracza.

    ...

    Atrybuty
    ----------
    rect : pygame.rect.Rect
        Obiekt przechowujący informację o półożeniu, szerokości i wyokości gracza.
    image  : pygame.surface.Surface
        Obraz przedstawiający kaktusa.
    rect  : pygame.rect.Rect
        Obiekt przechowujący informację o półożeniu, szerokości i wyokości kaktusa.
    rect.x : int
        Położenie na osi x lewego górnego rogu obrazu kaktusa.
    rect.y : int
        Położenie na osi x lewego górnego rogu obrazu kaktusa.
    speed : int
        Szybkość przesuwania się katusa do lewej strony ekranu.
    collided : int
        Zmienna kontrolująca ile razy gracz zderzył się z kaktusem.
    -------
    update():
        Uaktualnia pozycję kaktusa.
    """

    def __init__(self, x, y):

        """
        Tworzy wszystkie wymagane atrybuty dla obiektu z klasy Cactsu.

        Parametry
        ----------
            image  : pygame.surface.Surface
                Obraz przedstawiający kaktusa, nie wprowadza się.
            rect  : pygame.rect.Rect
                Obiekt przechowujący informację o półożeniu, szerokości i wyokości kaktusa, nie  wprowadza się, równa self.image.rect z zamienionymi współrzędnymi x i y.
            rect.x : int
                Położenie na osi x lewego górnego rogu obrazu kaktusa.
            rect.y : int
                Położenie na osi x lewego górnego rogu obrazu kaktusa.
            speed : int
                Szybkość przesuwania się katusa do lewej strony ekranu, nie wprowadza się (domyślnie 6).
            collided : int
                Zmienna kontrolująca ile razy gracz zderzył się z kaktusem, nie wporwadza się (domyślnie 0).
        """

        self.image = pygame.image.load("cactus.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 6
        self.collided = 0

    def update(self):

        """
        Aktualizuje pozcyję kaktusa i wyświetla go w niej na ekranie.

        Parametry
        ----------
        Brak
        
        Zwraca
        -------
        Brak
        """

        self.rect.x -= self.speed
        screen.blit(self.image, (self.rect.x, self.rect.y))

start_menu_not_focused = Text("Rozpocznij grę", font_menu, color_white)
start_menu_focused = Text("Rozpocznij grę", font_menu, color_black)
rules_menu_not_focused = Text("Jak grać?", font_menu, color_white)
rules_menu_focused = Text("Jak grać?", font_menu, color_black)
scoretable_menu_not_focused = Text("Tabela wyników", font_menu, color_white)
scoretable_menu_focused = Text("Tabela wyników", font_menu, color_black)
autorinfo_menu_not_focused = Text("O autorze", font_menu, color_white)
autorinfo_menu_focused = Text("O autorze", font_menu, color_black)
quit_menu_not_focused = Text("Wyjdź z gry", font_menu, color_white)
quit_menu_focused = Text("Wyjdź z gry", font_menu, color_black)

back_text = Text("Powrót", font_second, color_black)
yes_text = Text("Tak", font_second, color_black)
no_text = Text("Nie", font_second, color_black)

rules_text = Text(zasady_string, font_no_results, color_white)
autorinfo_text = Text(content, font_no_results, color_white)

gameover_text = Text("Koniec gry", font_menu, color_black)
saving_text = Text("Czy chcesz zapisać swój wynik?", font_saving, color_black)

background = pygame.image.load("tlo.png").convert()
cactus_image = pygame.image.load("cactus.png")

scroll = 0
background_width = background.get_width()
tiles = math.ceil(długość / background_width) + 1

spawn_cactus = True
cactus_list = []
score_add = 1
score_cactus = 100
tick = 30
max_cactus = 4
multiplication = 2/3
possibility_minimum = 95

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get(): 
          if event.type == pygame.QUIT:
            running = False
    
    if menu_window:
        game_button = Button(10, 3, 600, 46, 10, 7, 600, 46, screen_color, color_light)
        rules_button = Button(10, 50, 600, 49, 10, 56, 600, 46, screen_color, color_light)
        scoretable_button = Button(10, 100, 600, 49, 10, 106, 600, 46, screen_color, color_light)
        autorinfo_button = Button(10, 150, 600, 47, 10, 157, 600, 40, screen_color, color_light)
        quit_button = Button(10, 290, 600, 52, 10, 296, 600, 46, screen_color, color_light)
        
        screen.fill(screen_color) 

        game_button.showButton(screen)
        rules_button.showButton(screen)
        scoretable_button.showButton(screen)
        autorinfo_button.showButton(screen)
        quit_button.showButton(screen)
        
        if game_button.clickedCheck():
            player = Player(50, 240)
            game_window = True
            menu_window = False
        if rules_button.clickedCheck():
            rules_window = True
            menu_window = False
        if scoretable_button.clickedCheck():
            scoretable_window= True
            menu_window = False
        if autorinfo_button.clickedCheck():
            autorinfo_window = True
            menu_window = False
        if quit_button.clickedCheck():
            running = False 


        if game_button.focusCheck(screen):
            start_menu_focused.draw_text(screen, 15, 0)
        else:
            start_menu_not_focused.draw_text(screen, 15, 0)


        if rules_button.focusCheck(screen): 
            rules_menu_focused.draw_text(screen, 15, 50)
        else:
            rules_menu_not_focused.draw_text(screen, 15, 50)


        if scoretable_button.focusCheck(screen):
            scoretable_menu_focused.draw_text(screen, 15, 100)
        else:
            scoretable_menu_not_focused.draw_text(screen, 15, 100)


        if autorinfo_button.focusCheck(screen):
            autorinfo_menu_focused.draw_text(screen, 15, 150)
        else:
            autorinfo_menu_not_focused.draw_text(screen, 15, 150)


        if quit_button.focusCheck(screen):
            quit_menu_focused.draw_text(screen, 15, 290)
        else:
            quit_menu_not_focused.draw_text(screen, 15, 290)

    if game_window:
        screen.blit(background, (0, 0))
        tick = 50

        if pygame.key.get_pressed()[pygame.K_SPACE] and not player.is_jumping_and_falling and player.rect.y == player.default_position[1]:
            player.default_position = (player.rect.x, player.rect.y)
            player.is_jumping_and_falling = True
            pygame.mixer.Sound.play(jump_sound)
            pygame.mixer.music.stop()

        i = 0
        while(i < tiles):
            screen.blit(background, (background_width*i + scroll, 0))
            i += 1
        scroll -= 6
        
        if abs(scroll) > background_width:
            scroll = 0

        player.status()

        if spawn_cactus and len(cactus_list) < max_cactus:
            possibility = random.randint(0, 100)
            if possibility > possibility_minimum:
                cactus_x = długość
                cactus_list.append(Cactus(cactus_x, 260))
                spawn_cactus = False
    
        for obstacle in cactus_list:
            obstacle.update()

        if len(cactus_list) > 0 and cactus_list[-1].rect.right > 15:
            if cactus_list[-1].rect.right < długość * multiplication:
                spawn_cactus = True

            if cactus_list[0].rect.right < 0:
                if cactus_list[0].collided == 0:
                    player.score += score_cactus
                cactus_list.pop(0)

            rect1 = player.rect
            rect2 = cactus_list[0].rect

            if rect1.colliderect(rect2) and cactus_list[0].collided == 0 and 0 < rect2[0] < 85:
                if player.lives > 1:
                    pygame.mixer.Sound.play(hurt_sound)
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.Sound.play(death_sound)
                    pygame.mixer.music.stop()
                player.lives -= 1
                cactus_list[0].collided += 1
                player.is_hurt = True   

        player.show_lives()
        player.show_score()
        player.score += score_add

        if 10000 > player.score > 1500:
            score_add = 2
            score_cactus = 200
            tick = 60
        elif player.score > 10000:
            score_add = 3
            score_cactus = 300
            tick = 90
            max_cactus = 5
            multiplication = 3/4 
            possibility_minimum = 92
        
        if player.lives == 0:
            game_window = False
            gameover_window = True
            for kaktus in cactus_list:
                cactus_list.remove(kaktus)

    if gameover_window:
        save_button = Button(250, 250, 100, 50, 250, 250, 100, 50, color_dark, color_light)
        not_save_button = Button(450, 250, 100, 50, 450, 250, 100, 50, color_dark, color_light)
        screen.fill(screen_color)

        save_button.showButton(screen)
        not_save_button.showButton(screen)
        yes_text.draw_center_text(screen, 250, 250, 100, 50)
        no_text.draw_center_text(screen, 450, 250, 100, 50)

        gameover_text.draw_center_text(screen, 0, 50, 800, 100)
        saving_text.draw_center_text(screen, 0, 175, 800, 50)
        if save_button.clickedCheck():
            with open("wyniki.txt", "a", encoding="utf8") as file:
                file.write(str(player.score) + "\n")
            gameover_window = False
            time.sleep(0.3)
            menu_window = True
        elif not_save_button.clickedCheck():
            gameover_window = False
            time.sleep(0.3)
            menu_window = True

    if rules_window:
        back_button = Button(350, 270, 100, 70, 350, 270, 100, 70, color_dark, color_light)

        screen.fill(screen_color)

        rules_text.split_text(screen, 10, 10)
        back_button.showButton(screen)
        back_text.draw_center_text(screen, 350, 270, 100, 70)
        if back_button.clickedCheck():
            time.sleep(0.3)
            rules_window = False
            menu_window = True

    if scoretable_window:
        back_button = Button(50, 270, 250, 70, 50, 270, 250, 70, color_dark, color_light)

        screen.fill(screen_color)

        with open("wyniki.txt", "r", encoding="utf8") as file:
                scores = file.readlines()

        new_scores = []
        
        for rating in scores:
            new_rating = []
            for i in rating:
                if i in string.digits:
                    new_rating.append(i)
            rating = "".join(new_rating)
            rating = int(rating)
            new_scores.append(rating)
        
        new_scores.sort(reverse = True)

        if len(new_scores) == 0:
            no_results = Text("Aktualnie nie ma żadnych zapisanych wyników", font_no_results, color_white)
            no_results.draw_center_text(screen, 0, 50, 800, 70)
        else:
            scoretable_text = Text("Tabela wyników", font_menu, color_black)
            scoretable_text.draw_center_text(screen, 0, 10, 800, 50)
            if len(new_scores) > 10:
                new_scores = new_scores[:10]
            for i in range(len(new_scores)):
                top_scores = []
                if i == 0:
                    first_score = Text(f"1. {new_scores[0]}", font_best_score, color_white)
                    first_score.draw_text(screen, 10, 60)
                else:
                    top_scores = Text(f"{i+1}. {new_scores[i]}", font_no_results, color_white)
                    top_scores.draw_text(screen, 400, 32+i*32)
        
        back_button.showButton(screen)
        back_text.draw_center_text(screen, 50, 270, 250, 70)
        if back_button.clickedCheck():
            scoretable_window = False
            time.sleep(0.3)
            menu_window = True

    if autorinfo_window:
        back_button = Button(350, 270, 100, 70, 350, 270, 100, 70, color_dark, color_light)

        screen.fill(screen_color) 

        autorinfo_text.split_text(screen, 10, 10)
        back_button.showButton(screen)
        back_text.draw_center_text(screen, 350, 270, 100, 70)
        if back_button.clickedCheck():
            time.sleep(0.3)
            autorinfo_window = False
            menu_window = True

    clock.tick(tick)

    pygame.display.update()

pygame.quit()
pygame.mixer.quit()
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath
from PyQt5.QtTest import QTest


print("Nawiązano polączenie z sererem!")

class Rura:

    def __init__(self, punkty, grubosc=12, kolor=Qt.gray):

        
        self.punkty = [QPointF(float(p[0]), float(p[1])) for p in punkty]
        self.grubosc = grubosc
        self.kolor_rury = kolor
        self.kolor_cieczy = QColor(0, 180, 255) # Jasny niebieski
        self.czy_plynie = False
    def ustaw_przeplyw(self, plynie):
        self.czy_plynie = plynie

    def draw(self, painter):
        if len(self.punkty) < 2:
            return

        path = QPainterPath()
        path.moveTo(self.punkty[0])
        for p in self.punkty[1:]:
            path.lineTo(p)
        # 1. Rysowanie obudowy rury
        pen_rura = QPen(self.kolor_rury, self.grubosc, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen_rura)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path)

        # 2. Rysowanie cieczy
        if self.czy_plynie:
            pen_ciecz = QPen(self.kolor_cieczy, self.grubosc- 4, Qt.SolidLine,Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen_ciecz)
            painter.drawPath(path)

class Zbiornik:
    def __init__(self, x, y, width=100, height=140, nazwa=""):
        self.x = x; self.y = y
        self.width = width; self.height = height
        self.nazwa = nazwa
        self.pojemnosc = 100.0
        self.aktualna_ilosc = 0.0
        self.poziom = 0.0 # Wartosc 0.0-1.0


    def dodaj_ciecz(self, ilosc):
        wolne = self.pojemnosc- self.aktualna_ilosc
        dodano = min(ilosc, wolne)
        self.aktualna_ilosc += dodano
        self.aktualizuj_poziom()
        return dodano

    def usun_ciecz(self, ilosc):
        usunieto = min(ilosc, self.aktualna_ilosc)
        self.aktualna_ilosc-= usunieto
        self.aktualizuj_poziom()
        return usunieto

    def aktualizuj_poziom(self):
        self.poziom = self.aktualna_ilosc / self.pojemnosc

    def czy_pusty(self): return self.aktualna_ilosc <= 0.1
    def czy_pelny(self): return self.aktualna_ilosc >= self.pojemnosc- 0.1

    # Punkty odniesienia do rysowania rur
    def punkt_gora_srodek(self): return (self.x + self.width/2, self.y)
    def punkt_dol_srodek(self): return (self.x + self.width/2, self.y + self.height)
    def draw(self, painter):
    # 1. Rysowanie cieczy
        if self.poziom > 0:
            h_cieczy = self.height * self.poziom
            y_start = self.y + self.height- h_cieczy
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 120, 255, 200))
            painter.drawRect(int(self.x + 3), int(y_start), int(self.width- 6),int(h_cieczy- 2))
        # 2. Rysowanie obrysu
        pen = QPen(Qt.white, 4)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))
        # 3. Podpis
        painter.setPen(Qt.white)
        painter.drawText(int(self.x), int(self.y- 10), self.nazwa)

class turbina:

    def __init__(self, x, y, width=24, height=14, nazwa=""):
        self.x = x; self.y = y
        self.width = width; self.height = height
        self.nazwa = nazwa

    def draw(self, painter):
        pen = QPen(Qt.red, 2)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))
        painter.setPen(Qt.red)
        painter.drawText(int(self.x), int(self.y), self.nazwa)

class grzanie:
    def __init__(self, x, y, width=24, height=24, nazwa=""):
        self.x = x; self.y = y
        self.width = width; self.height = height
        self.nazwa = nazwa
        self.czy_grzeje = False

    def draw(self, painter):
        kolor= Qt.red if self.czy_grzeje else Qt.yellow
        pen = QPen(kolor, 2)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(int(self.x), int(self.y), int(self.width), int(self.height))
        painter.setPen(pen)
        painter.drawText(int(self.x), int(self.y), self.nazwa)

class para:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.widoczna = False

    def draw(self, painter):
        if self.widoczna:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(200, 200, 200, 150))
            painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))

class Zbiornik_para:
    def __init__(self, x, y, width=100, height=140, nazwa=""):
        self.x = x; self.y = y
        self.width = width; self.height = height
        self.nazwa = nazwa
        self.pojemnosc = 100.0
        self.aktualna_ilosc = 0.0
        self.poziom = 0.0

    def usun_ciecz(self, ilosc):
        usunieto = min(ilosc, self.aktualna_ilosc)
        self.aktualna_ilosc-= usunieto
        self.aktualizuj_poziom()
        return usunieto

    def aktualizuj_poziom(self):
        self.poziom = self.aktualna_ilosc / self.pojemnosc

    def dodaj_ciecz(self, ilosc):
        wolne = self.pojemnosc- self.aktualna_ilosc
        dodano = min(ilosc, wolne)
        self.aktualna_ilosc += dodano
        self.aktualizuj_poziom()
        return dodano
    
    def punkt_gora_srodek_P(self): return (self.x + self.width/2, self.y)
    def punkt_dol_srodek_P(self): return (self.x + self.width/2, self.y + self.height)

    def draw(self, painter):
        pen = QPen(Qt.white, 4)
        pen.setJoinStyle(Qt.MiterJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))
        painter.setPen(Qt.white)
        painter.drawText(int(self.x), int(self.y- 10), self.nazwa)

        if self.poziom > 0:
            h_cieczy = self.height * self.poziom
            y_start = self.y + self.height- h_cieczy
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 120, 255, 200))
            painter.drawRect(int(self.x + 3), int(y_start), int(self.width- 6),int(h_cieczy- 2))


        

class okno_drugi_zbiornik(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zbiornik na pare")
        self.setFixedSize(500, 400) #rozmiary okna
        self.setStyleSheet("background-color: #222;")

        self.zp1 = Zbiornik_para(50, 50, nazwa="Zbiornik Para")
        self.zbiorniki_para = [self.zp1]
        

       

    
        
        self.btn = QPushButton("Zbiornik Pary +", self)
        self.btn.setGeometry(50, 300, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.dodaj)

        

        self.btn = QPushButton("Zbiornik Pary -", self)
        self.btn.setGeometry(150, 300, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.odejmij)


        #Rura 4
        p_start4 = self.zp1.punkt_dol_srodek_P()
        x_koniec = -100
        wysokosc_zakretu = p_start4[1] + 50 #--[1] wspolrzedne Y
        self.rura4 = Rura([p_start4, #--poczatek
                            (p_start4[0], wysokosc_zakretu), #--zmienia Y, a X zostaje w miejscu
                            (x_koniec, wysokosc_zakretu)])
        

        self.rury2=[self.rura4]

    
    


    def dodaj(self):
        print("Dodano wodę do Zbiornika o ilości: ", (100-self.zp1.aktualna_ilosc))
        self.zp1.dodaj_ciecz((100-self.zp1.aktualna_ilosc))
        self.update()
    def odejmij(self):
        print("Zabrano wodę ze Zbiornika Pary o ilości: ", (self.zp1.aktualna_ilosc))
        self.zp1.dodaj_ciecz(-(self.zp1.aktualna_ilosc))
        self.update()



    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        for zp in self.zbiorniki_para: zp.draw(p)
        for rura in self.rury2:rura.draw(p)

        


class SymulacjaKaskady(QWidget):
    def dodaj(self):
        print("Dodano wodę do Zbiornika 1 o ilości: ", (100-self.z1.aktualna_ilosc))
        self.z1.dodaj_ciecz((100-self.z1.aktualna_ilosc))
        self.update()
    def odejmij(self):
        print("Zabrano wodę ze Zbiornika 1 o ilości: ", (self.z1.aktualna_ilosc))
        self.z1.dodaj_ciecz(-(self.z1.aktualna_ilosc))
        self.update()
    def dodaj2(self):
        print("Dodano wodę do Zbiornika 2 o ilości: ", (100-self.z2.aktualna_ilosc))
        self.z2.dodaj_ciecz((100-self.z2.aktualna_ilosc))
        self.update()
    def odejmij2(self):
        print("Zabrano wodę ze Zbiornika 2 o ilości: ", (self.z2.aktualna_ilosc))
        self.z2.dodaj_ciecz(-(self.z2.aktualna_ilosc))
        self.update()
    def dodaj3(self):
        print("Dodano wodę do Zbiornika 3 o ilości: ", (100-self.z3.aktualna_ilosc))
        self.z3.dodaj_ciecz((100-self.z3.aktualna_ilosc))
        self.update()
    def odejmij3(self):
        print("Zabrano wodę ze Zbiornika 3 o ilości: ", (self.z3.aktualna_ilosc))
        self.z3.dodaj_ciecz(-(self.z3.aktualna_ilosc))
        self.update()
    def dodaj_zp2(self):
        print("Dodano wodę do Zbiornika Pary 2 o ilości: ", (100-self.zp2.aktualna_ilosc))
        self.zp2.dodaj_ciecz((100-self.zp2.aktualna_ilosc))
        self.update()
    def odejmij_zp2(self):
        print("Zabrano wodę ze Zbiornika Pary 2 o ilości: ", (self.zp2.aktualna_ilosc))
        self.zp2.dodaj_ciecz(-(self.zp2.aktualna_ilosc))
        self.update()

    def __init__(self):

        self.drugie_okno = okno_drugi_zbiornik()
        self.drugie_okno.show()

        super().__init__()
        self.setWindowTitle("Kaskada: Dol-> Gora")
        self.setFixedSize(1000, 650) #rozmiary okna
        self.setStyleSheet("background-color: #222;")

        #--para--
        self.pa1 = para(660, 250, 80, 60)
        self.pary = [self.pa1]

        #---Konfiguracja Zbiornikow --
        self.z1 = Zbiornik(50, 50, nazwa="Zbiornik 1")
        self.z1.aktualna_ilosc = 100.0; self.z1.aktualizuj_poziom() # Pelny
        self.z2 = Zbiornik(350, 200, nazwa="Zbiornik 2")
        self.z3 = Zbiornik(650, 350, nazwa="Zbiornik 3")
        self.zp2 = Zbiornik(850, 400, nazwa= "Zbiornik Para 2")
        self.zbiorniki = [self.z1, self.z2, self.z3, self.zp2]

        #---Konfiguracja Rur--
        # Rura 1: Z1 (Dol)-> Z2 (Gora)
        p_start = self.z1.punkt_dol_srodek()
        p_koniec = self.z2.punkt_gora_srodek()
        mid_y = (p_start[1] + p_koniec[1]) / 2
        self.rura1 = Rura([
        p_start, (p_start[0], mid_y), (p_koniec[0], mid_y), p_koniec])

        # Rura 2: Z2 (Dol)-> Z3 (Gora)
        p_start2 = self.z2.punkt_dol_srodek()
        p_koniec2 = self.z3.punkt_gora_srodek()
        mid_y2 = (p_start2[1] + p_koniec2[1]) / 2
        self.rura2 = Rura([p_start2, (p_start2[0], mid_y2), (p_koniec2[0], mid_y2), p_koniec2])
        #Rura 3
        p_start3 = self.z3.punkt_gora_srodek()
        x_koniec = 1000
        x_srodek = 900
        wysokosc_zakretu = p_start3[1] - 50 #--[1] wspolrzedne Y
        rozgalezienie = (x_srodek, wysokosc_zakretu)
        self.rura3 = Rura([p_start3, #--poczatek
                            (p_start3[0], wysokosc_zakretu), #--zmienia Y, a X zostaje w miejscu
                            (x_koniec, wysokosc_zakretu)])#--[0] wspolrzedne X, zmienia X, Y zostaje ten sam co wyzej
        wysokosc_odnogi = wysokosc_zakretu + 100
        self.rura3_odnoga = Rura([
            rozgalezienie, 
            (x_srodek, wysokosc_odnogi)])
        

        self.rury = [self.rura1, self.rura2, self.rura3, self.rura3_odnoga]


        #---Timer i Sterowanie--
        self.timer = QTimer()
        self.timer.timeout.connect(self.logika_przeplywu)

        #---Konfiguracja Turbin--
        self.t1 = turbina(250, mid_y-7, nazwa="Turbina 1")
        self.t2 = turbina(525, mid_y2-7, nazwa="Turbina 2")
        self.turbiny = [self.t1, self.t2]

        #---Konfiguracja Grzania--
        self.g1 = grzanie(690, 510, nazwa="Grzanie")
        self.grzanie = [self.g1]

         

        #--Sterowanie obiektem -> zbiorniki--
        self.btn = QPushButton("Zbiornik 1 +", self)
        self.btn.setGeometry(150, 550, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.dodaj)

        

        self.btn = QPushButton("Zbiornik 1 -", self)
        self.btn.setGeometry(250, 550, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.odejmij)

        self.btn = QPushButton("Zbiornik 2 +", self)
        self.btn.setGeometry(350, 550, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.dodaj2)

        

        self.btn = QPushButton("Zbiornik 2 -", self)
        self.btn.setGeometry(450, 550, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.odejmij2)

        self.btn = QPushButton("Zbiornik 3 +", self)
        self.btn.setGeometry(550, 550, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.dodaj3)

        

        self.btn = QPushButton("Zbiornik 3 -", self)
        self.btn.setGeometry(650, 550, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.odejmij3)


        self.btn = QPushButton("Zbiornik Pary 2 +", self)
        self.btn.setGeometry(500, 600, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.dodaj_zp2)

        

        self.btn = QPushButton("Zbiornik Pary 2 -", self)
        self.btn.setGeometry(600, 600, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.odejmij_zp2)

        
        
        self.btn_grzanie = QPushButton("Grzanie ON/OFF", self)
        self.btn_grzanie.setGeometry(850, 550, 100, 30)
        self.btn_grzanie.setStyleSheet("background-color: red; color: white;")
        self.btn_grzanie.clicked.connect(self.podgrzewanie)
        

        self.btn = QPushButton("Start / Stop", self)
        self.btn.setGeometry(50, 550, 100, 30)
        self.btn.setStyleSheet("background-color: #444; color: white;")
        self.btn.clicked.connect(self.przelacz_symulacje)
        self.running = False
        self.flow_speed = 0.4

        #--Sterowanie obiektem -> turbiny--
        self.on=False
        self.btn = QPushButton("Turbiny ON/OFF", self)
        self.btn.setGeometry(750, 550, 100, 30)
        self.btn.setStyleSheet("background-color: red; color: white;")
        self.btn.clicked.connect(self.praca_turbin)

    def podgrzewanie(self):
            if not self.g1.czy_grzeje:
                self.g1.czy_grzeje = True
                self.btn_grzanie.setStyleSheet("background-color: green; color: white;")
                self.update()
                for temperatura in range (27, 101):
                    if not self.g1.czy_grzeje:
                        print("Ręcznie wstrzymano podgrzewanie")
                        self.btn_grzanie.setStyleSheet("background-color: red; color: white;")
                        break 
                    print("Temperatura wody wynosi: ", temperatura)
                    QTest.qWait(500) 
                    if(temperatura>=85) and temperatura <= 95 and self.z3.aktualna_ilosc>11:
                        for pa in self.pary: 
                            pa.widoczna = True 
                        
                            if self.zp2.aktualna_ilosc < 100 and self.drugie_okno.zp1.aktualna_ilosc < 100:
                                self.z3.dodaj_ciecz(-(2))
                                self.zp2.dodaj_ciecz(1)
                                self.update()
                                self.drugie_okno.zp1.dodaj_ciecz(1) 
                                self.drugie_okno.update()
                            elif(self.zp2.aktualna_ilosc>=100 and self.drugie_okno.zp1.aktualna_ilosc<100):
                                self.z3.dodaj_ciecz(-(2))
                                self.zp2.dodaj_ciecz(0)
                                self.update()
                                self.drugie_okno.zp1.dodaj_ciecz(2) 
                                self.drugie_okno.update()
                            elif(self.zp2.aktualna_ilosc<100 and self.drugie_okno.zp1.aktualna_ilosc>=100):
                                self.z3.dodaj_ciecz(-(2))
                                self.zp2.dodaj_ciecz(2)
                                self.update()
                                self.drugie_okno.zp1.dodaj_ciecz(0) 
                                self.drugie_okno.update()
                    else:
                        for pa in self.pary: 
                            pa.widoczna = False
                        self.update()
                    if(self.zp2.aktualna_ilosc>=100 and self.drugie_okno.zp1.aktualna_ilosc>=100):
                        self.g1.czy_grzeje = False
                        print("Wylączenie awaryjne, zbiorniki pary pelne!")
                        pa.widoczna = False
                        self.update()
                        self.btn_grzanie.setStyleSheet("background-color: red; color: white;")
                        break
                    if(temperatura>=96):
                        self.g1.czy_grzeje = False
                        self.update()
                        print("Wylączenie awaryjne, za wysoka temperatura wody")
                        self.btn_grzanie.setStyleSheet("background-color: red; color: white;")
                        break
                    if(self.z3.aktualna_ilosc<=11):
                        self.g1.czy_grzeje = False
                        print("Wylączenie awaryjne, za niski poziom wody")
                        pa.widoczna = False
                        self.update()
                        self.btn_grzanie.setStyleSheet("background-color: red; color: white;")
                        break
                   
                self.btn_grzanie.setStyleSheet("background-color: red; color: white;")
                
            else:
                self.g1.czy_grzeje = False
                self.btn_grzanie.setStyleSheet("background-color: red; color: white;")
                self.update()

    def praca_turbin(self):
        if not self.on:
            self.on = True
            self.btn.setStyleSheet("background-color: green; color: white;")
            self.flow_speed = 2*self.flow_speed
            print("Turbina wlączona, prędkość wody dwukrotnie zwiększona")
        else:
            self.on = False
            self.btn.setStyleSheet("background-color: red; color: white;")
            self.flow_speed = self.flow_speed/(2)
            print("Turbina wylączona")


    def przyspiesz_wode(self):
        self.flow_speed=1.5*self.flow_speed

    def przelacz_symulacje(self):
        if self.running: self.timer.stop(); print("Symulacje przeplywu wstrzymana!"); print("Aktualny stan wody w Zbiorniku 1 to: ", self.z1.aktualna_ilosc, "\n" "Aktualny stan wody w Zbiorniku 2 to: ", self.z2.aktualna_ilosc, "\n" "Aktualny stan wody w Zbiorniku 3 to: ", self.z3.aktualna_ilosc)
        else: self.timer.start(20); print("Rozpoczęto symulacje przeplywu!")
        self.running = not self.running
    def logika_przeplywu(self):
        # 1. Przeplyw Z1-> Z2
        plynie_1 = False
        if not self.z1.czy_pusty() and not self.z2.czy_pelny():
            ilosc = self.z1.usun_ciecz(self.flow_speed)
            self.z2.dodaj_ciecz(ilosc)
            plynie_1 = True
        self.rura1.ustaw_przeplyw(plynie_1)
        # 2. Przeplyw Z2-> Z3 (Startuje dopiero gdy Z2 ma ponad 15 wody)
        plynie_2 = False
        if self.z2.aktualna_ilosc > 15 and not self.z3.czy_pelny(): 
                ilosc = self.z2.usun_ciecz(self.flow_speed)
                self.z3.dodaj_ciecz(ilosc)
                plynie_2 = True
                self.rura2.ustaw_przeplyw(plynie_2)
        elif self.z2.aktualna_ilosc > 0 and self.z2.aktualna_ilosc <= 15 and self.z3.aktualna_ilosc<100 and plynie_1 == False:
                ilosc = self.z2.usun_ciecz(self.flow_speed)
                self.z3.dodaj_ciecz(ilosc)
                plynie_2 = True
                self.rura2.ustaw_przeplyw(plynie_2)
        self.update()
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        for r in self.rury: r.draw(p)
        for z in self.zbiorniki: z.draw(p)
        for t in self.turbiny: t.draw(p)
        for g in self.grzanie: g.draw(p)
        for pa in self.pary: pa.draw(p)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    okno = SymulacjaKaskady()
    okno.show()
    sys.exit(app.exec_())
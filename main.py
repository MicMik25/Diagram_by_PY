"""
Program opiera się na pliku .csv który zawiera dane przeżywalności Kobiet(rok 2020 , dane z GUS) w zależności od wieku , przy założeniu początk-
-owej liczby urodzeń 100000. W pierwszej kolumnie znajduje się wiek , a w drugiej liczba kobiet która dożywa takiego wieku. Obliczamy ile kobiet
umiera na przestrzeni kolejnych lat życia , a następnie prezentujemy to na wykresie.Następnie dane o zgonach i wieku zapisujemy w nowo utworzonym
pliku .csv , a
"""
import sys
import numpy
import csv
import xlsxwriter
import matplotlib.pyplot as plt
class WymiarList(Exception):
    komunikat='Listy są różnych rozmiarów - błąd iteracji , nie zapisano do pliku'
    def __init__(self,kom):
        self.komunikat=kom
class IloscArgumentow(Exception):
    komunikat='Nieprawidłowa ilość argumentów na osi X , ilość musi się równać ilości elementów z listy'
    def __init__(self,kom):
        self.komunikat=kom


class Klasa:
    def Odczyt_z_Pliku(self):
        # policzmy zatem ile wg GUS w badanej grupie umiera kobiet z każdym kolejnym rokiem życia .
        lista=[]
        lista_zgonow=[]
        lista_wiek=[]
        try:
            with open(self) as plik:
                czytnik = csv.reader(plik,delimiter=';')
                for wiersz in czytnik:
                    print(wiersz)
                    lista.append(wiersz[1])
                    lista_wiek.append(wiersz[0])
                print('\n')
                print('Lista przeżywalności:')
                lista.pop(0)
                print(lista)
                for i in range (1,len(lista)):
                    lista_zgonow.append(int(lista[0])-int(lista[i]))
                print('\n')
                print('Lista zgonów to:')
                print(lista_zgonow)
        except FileNotFoundError:
            print('Nie znaleziono pliku')
            sys.exit(0)
        #Teraz narysujmy wykrees
        try:
            a=0
            b=100
            c=100
            x=numpy.linspace(a,b,c)
            if a!= 0 or b!=100 or c!=100:
                raise IloscArgumentow('Nie zgadza się liczba argumentów lub wartości na wykresie')
            y=lista_zgonow
            plt.plot(x,y)
            plt.title('Umieralność kobiet względem wieku')
            plt.xlabel('Wiek')
            plt.ylabel('Zgony')
            plt.grid(visible=bool)
            plt.savefig('wykres.png') #tutaj zapisujemy wykres jako plik .png
            plt.show()
        except IloscArgumentow as wyjatek:
            print('Wystąpił wyjątek :')
            print(wyjatek)
        #Zapisujemy dane do pliku
        #tworzenie pliku
        outWorkbook=xlsxwriter.Workbook('out.xlsx')
        outSheet=outWorkbook.add_worksheet()
        #deklarowanie danych
        outSheet.write('A1','Wiek')
        outSheet.write('B1','Umieralność')
        #Poniżej modyfikujemy listę tak by zawierała tylko wartości bez tekstu i była równej długości co lista zgonów
        lista_wiek.pop(0)
        lista_wiek.pop(0)
        #Zapisywanie z obsługą wyjątku , gdy listy byłyby róznych długości
        try:
            for i in range(len(lista_wiek)):
                outSheet.write(i+1,0,lista_wiek[i])
                outSheet.write(i+1,1,lista_zgonow[i])
        except IndexError :
            print('Wystąpił wyjątek')
            print(WymiarList.komunikat)

        outWorkbook.close()


a='tabela.csv'
Klasa.Odczyt_z_Pliku(a)
"""
Wyjątki do obsłużenia :
1.FilenotFoundError
2.Sprawdź czy listy mają równą długość , żeby w razie co nie było błędu indeksacji
3.Błąd przy rysowaniu wykresu w X , drugi parametr musi być równy ilości argumentów
"""


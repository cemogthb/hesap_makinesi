import tkinter as tk

def toplama(a, b):
    return a + b

def cikarma(a, b):
    return a - b

def carpma(a, b):
    return a * b

def bolme(a, b):
    return a / b

def yuzde_alma(a, b):
    return a * b/100

def islem_degistir(y):
    if len(islem) == 0:
        return
    islem[-1] = y
    kutu.config(text="".join(islem))


def temizle():
    global sonuc_gosteriliyor
    sonuc_gosteriliyor = False
    birlestir.clear()
    islem.clear()
    kutu.config(text="")


def sil():
    if len(birlestir) != 0:
        birlestir.pop()
    elif len(islem) == 0:
        return
    else:
        islem.pop() # +'yı sildi
        birlestir.clear()
        for harf in islem.pop():
            birlestir.append(harf)

    kutu.config(text="".join(islem) + "".join(birlestir))
        


def ekran_guncelle(x):
    global sonuc_gosteriliyor
    if sonuc_gosteriliyor:
        birlestir.clear()
        sonuc_gosteriliyor = False
    if birlestir == ["-", "0"] and x != ".":
            birlestir.pop()   
    if birlestir == ["0"] and x != ".":
        birlestir.clear()
    birlestir.append(x)
    kutu.config(text="".join(islem) + "".join(birlestir))




def islemler(A):
    global sonuc_gosteriliyor
    if birlestir == ["-"]:
            return
    sonuc_gosteriliyor = False
    if len(birlestir) == 0:
        islem_degistir(A)
        return
    islem.append("".join(birlestir))
    islem.append(A)
    kutu.config(text="".join(islem))
    birlestir.clear()


def nokta():
    global sonuc_gosteriliyor
    if "." in birlestir:
        return
    
    if sonuc_gosteriliyor:
        birlestir.clear()
        sonuc_gosteriliyor = False
    
    if len(birlestir) == 0:
            birlestir.append("0")    
    ekran_guncelle(".")

def eksi():
    if len(birlestir) == 0:
        birlestir.append("-")
        kutu.config(text="".join(islem) + "".join(birlestir))
    elif birlestir == ["-"]:
        return
    elif len(birlestir) != 0:
        islemler("-") 
    

def esittir():
    global sonuc_gosteriliyor
    if birlestir == ["-"]:
        return
    if len(birlestir) == 0:
        if len(islem) == 0:
            return
        else:
            islem.pop()
            birlestir.append(islem.pop())

    islem.append("".join(birlestir))
    for i in range(0, len(islem), 2):
        islem[i] = float(islem[i]) 
        
    while "x" in islem or "/" in islem or "%" in islem:
        for i in range(1, len(islem), 2):
            if islem[i] == "x":
                hesap = carpma(islem[i-1], islem[i+1])
                islem [i-1] = hesap
                islem.pop(i)
                islem.pop(i)
                break
            elif islem[i] =="/":
                try:
                    hesap = bolme(islem[i-1], islem[i+1])
                except ZeroDivisionError:
                    birlestir.clear()
                    islem.clear()
                    kutu.config(text="Tanımsız")
                    return 
                islem [i-1] = hesap
                islem.pop(i)
                islem.pop(i)
                break
            elif islem[i] =="%":
                    hesap = yuzde_alma(islem[i-1], (islem[i+1]))
                    islem [i-1] = hesap
                    islem.pop(i)
                    islem.pop(i)
                    break
    sonuc = islem[0]

    for i in range(1, len(islem), 2):
        if islem[i] == "+":
            sonuc = toplama(sonuc, (islem[i+1]))
        elif islem[i] == "-":
            sonuc = cikarma(sonuc, (islem[i+1]))

    islem.clear()
    birlestir.clear()
    birlestir.append(f"{sonuc:.15g}")    
    kutu.config(text=f"{sonuc:.15g}")
    sonuc_gosteriliyor = True


birlestir = []
islem = []
sonuc_gosteriliyor = False


ARKA       = "#E3EEF8"   # pencere
YAZI       = "#22364A"   # yazılar (koyu lacivert)
RAKAM      = "#FAFCFE"   # rakamlar
OZEL_A     = "#C6DCEF"   # C, <--, %, .
OZEL_B     = "#B3CFE8"   # basildiginda
ISLEM      = "#9CC3E6"   # + - x /
ESIT       = "#6FA6D8"   # =

pencere = tk.Tk()
pencere.config(bg=ARKA)
pencere.geometry("360x520")
pencere.title("Hesap Makinesi(Calculator)")
t = ("Segoe UI", 20) 


pencere.option_add("*Button.relief", "flat")
pencere.option_add("*Button.borderWidth", 0)
pencere.option_add("*Button.font",t)
pencere.option_add("*Button.foreground", YAZI)
pencere.option_add("*Button.background", RAKAM)
pencere.option_add("*Button.activeBackground", OZEL_B)

for i in range(6):
    pencere.rowconfigure(i, weight=1, uniform="satir")
for i in range (4):
    pencere.columnconfigure(i, weight=1, uniform="buton")



kutu = tk.Label(pencere, font=("Segoe UI", 25) , text="", anchor="w", background=ARKA, fg=YAZI)
kutu.grid(row= 0, column=0,columnspan=4, sticky="ew", padx=10, pady=10)

rakamlar = [("1",4,0),("2",4,1),("3",4,2),("4",3,0),("5",3,1),("6",3,2),("7",2,0),("8",2,1),("9",2,2)]

for rakam, satir, sutun in rakamlar:
    b =tk.Button(pencere,text=rakam, command=lambda r=rakam:ekran_guncelle(r))
    b.grid(row=satir, column=sutun, sticky="nsew")

sifir = tk.Button(pencere, text="0", command=lambda: ekran_guncelle("0"))
sifir.grid(row=5, column=0, columnspan=2, sticky="nsew")

topla_buton = tk.Button(pencere, text="+", font=t, command=lambda:islemler("+"),bg=ISLEM)
topla_buton.grid(row=4, column=3, sticky="nsew")

cikar_buton = tk.Button(pencere, text="-", font=t, command=eksi,bg=ISLEM)
cikar_buton.grid(row=3, column=3, sticky="nsew")

carp_buton = tk.Button(pencere, text="X", font=t,command=lambda:islemler("x"),bg=ISLEM)
carp_buton.grid(row=2, column=3, sticky="nsew")

bol_buton = tk.Button(pencere, text="/", font=t, command=lambda:islemler("/"),bg=ISLEM)
bol_buton.grid(row=1, column=3, sticky="nsew")

yuzde_buton = tk.Button(pencere, text="%",command=lambda:islemler("%"),bg=OZEL_A)
yuzde_buton.grid(row=1, column=2, sticky="nsew" )


clear_buton = tk.Button(pencere, text="C",command=temizle,bg=OZEL_A)
clear_buton.grid(row=1, column=0, sticky="nsew")

sil_buton = tk.Button(pencere, text="<--",command=sil,bg=OZEL_A)
sil_buton.grid(row=1, column=1, sticky="nsew" )

esit_buton = tk.Button(pencere, text="=",command=esittir,bg=ESIT)
esit_buton.grid(row=5, column=3, sticky="nsew" )

nokta_buton = tk.Button(pencere, text=".",command=nokta,bg=OZEL_A)
nokta_buton.grid(row=5, column=2, sticky="nsew" )

for parca in pencere.grid_slaves():
    if parca != kutu:
        parca.grid_configure(padx =3, pady=3)


pencere.mainloop()
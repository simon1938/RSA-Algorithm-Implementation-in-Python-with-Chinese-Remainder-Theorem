# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:44:40 2020

@author: Mr ABBAS-TURKI
"""

import hashlib
import binascii
import random
random.seed()

def home_mod_expnoent(x,y,n):#exponentiation modulaire

    carre=x   

    resultat=1

    while y>0:        
        if y%2==1:

            resultat=(resultat*carre) % n #On verifie si y est impair pour éviter des calculs inutiles
        carre = (carre*carre) % n
        y=y//2

    return resultat           


def home_ext_euclide(y, b):#algorithme d'euclide étendu pour la recherche de l'exposant secret
  
    dividend = y
    divisor = b
    quotient = y // b
    remainder = y % b
    list = [0, 1]
    i = 0

    while (remainder != 0):

        i = i + 1
        if i >= 1:
            list.append(list[i-1] - quotient*list[i])
        dividend = divisor
        divisor = remainder
        quotient = dividend // divisor
        remainder = dividend % divisor

    return list[-1] % y

def home_pgcd(a,b): #recherche du pgcd
    if(b==0): 
        return a 
    else: 
        return home_pgcd(b,a%b)

def home_string_to_int(x): # pour transformer un string en int
    z=0
    for i in reversed(range(len(x))):
        z=int(ord(x[i]))*pow(2,(8*i))+z
    return(z)


def home_int_to_string(x): # pour transformer un int en string
    txt=''
    res1=x
    while res1>0:
        res=res1%(pow(2,8))
        res1=(res1-res)//(pow(2,8))
        txt=txt+chr(res)
    return txt



def mot10char(): #entrer le secret
    secret=input("donner un secret: ")
    while len(secret)==0:
        secret = input("Veuillez entrer un secret")
    return secret

def CRT(message_chiffre, facteur1, facteur2, exposant_prive, modulo):   

    if facteur1 > facteur2:
        facteur1, facteur2 = facteur2, facteur1

    dp = exposant_prive % (facteur1 - 1)
    dq = exposant_prive % (facteur2 - 1)

    facteur2_inv=home_ext_euclide(facteur2,facteur1)
    mp=home_mod_expnoent(message_chiffre,dp,facteur1)
    mq=home_mod_expnoent(message_chiffre,dq,facteur2)

    h=(facteur2_inv*(mp-mq))%facteur1
    m=(mq+h*facteur2)%modulo

    return m
#pour enlever les espaces dans un texte car j'avais des erreur avec
def remove_spaces(text):
    return text.replace(" ", "")

#voici les éléments de la clé d'Alice

x1a=3503815992030544427564583819137897895645343456451321234534564646453453456456456456454545458764549189 #p
x2a=3503815992030544427564583819137897895645343456451321234534564646453453456456456456454545642354565471 #q
na=x1a*x2a  #n
phia=((x1a-1)*(x2a-1))//home_pgcd(x1a-1,x2a-1)
ea=17 #exposant public
da=home_ext_euclide(phia,ea) #exposant privé
#voici les éléments de la clé de bob
x1b=4932857219512528676440106034047625505005004262342462342452624255264252574542224462250521525425345743 #p
x2b=9420734535044410552424350537132123002156432123156423112515050515231212312315315123123123154561322453 #q
nb=x1b*x2b # n
phib=((x1b-1)*(x2b-1))//home_pgcd(x1b-1,x2b-1)
eb=23 # exposants public
db=home_ext_euclide(phib,eb) #exposant privé
k=30 #longeur du bloc
liste_bloc=[] #liste de blocs


print("Vous êtes Bob, vous souhaitez envoyer un secret à Alice")
print("voici votre clé publique que tout le monde a le droit de consulter")
print("n =",nb)
print("exposant :",eb)
print("voici votre précieux secret")
print("d =",db)
print("*******************************************************************")
print("Voici aussi la clé publique d'Alice que tout le monde peut conslter")
print("n =",na)
print("exposent :",ea)
print("*******************************************************************")
print("il est temps de lui envoyer votre secret ")
print("*******************************************************************")
x=input("appuyer sur entrer")
secret=mot10char()
secret=remove_spaces(secret)
print("*******************************************************************")
print("voici la version en nombre décimal de ",secret," : ")
num_sec=home_string_to_int(secret)
print(num_sec)
# Transformation en bytes et mise en forme de blocs
num_sec=num_sec.to_bytes((num_sec.bit_length() + 7) // 8, 'little') 
#little signifie que la représentation des octets est de poids faible à droite

#mettre max 50% du contenu dans les blocs 
j=k//2
for i in range(0,len(num_sec),j):
    liste_bloc.append(num_sec[i:i+j])
print("*******************************************************************")
print("Message de 30 octets avec le bourrage")
# Bourrage des blocs
message_avec_bourrage=[]
#Bourrage des blocs avec la forme suivante : 00‖02‖𝑥‖00‖𝑚𝑖‖, avec 00, 02 sont des octets valant 0 et 2 en hexadécimal.

for i in range(len(liste_bloc)):
    j=len(liste_bloc[i])
    x=random.randbytes(k-j-3)
    message_avec_bourrage.append(b'\x00\x02'+x+b'\x00'+liste_bloc[i])

print(message_avec_bourrage)
# Chiffrement RSA avec la clé publique d'Alice
print("voici le message chiffré avec la publique d'Alice : ")
message_chiffré_paralice=[]
for i in range(len(message_avec_bourrage)):

    cle_public_alice=home_mod_expnoent(int.from_bytes(message_avec_bourrage[i],'little'),ea,na)
    message_chiffré_paralice.append(cle_public_alice.to_bytes((cle_public_alice.bit_length() + 7) // 8, 'little'))

print("*******************************************************************")
print("On utilise la fonction de hashage sha256 pour obtenir le hash du message",secret)
Bhachis0=hashlib.sha256(secret.encode(encoding='UTF-8',errors='strict')).digest() #sha256 du message
print("voici le hash en nombre décimal ")
Bhachis1=binascii.b2a_uu(Bhachis0)
Bhachis2=Bhachis1.decode() #en string
Bhachis3=home_string_to_int(Bhachis2)
print(Bhachis3)
print("voici la signature avec la clé privée de Bob du hachis")
signe=home_mod_expnoent(Bhachis3, db, nb)
print(signe)
print("*******************************************************************")
print("Bob envoie \n \t 1-le message chiffré avec la clé public d'Alice \n",cle_public_alice,"\n \t 2-et le hash signé \n",signe)
print("*******************************************************************")
x=input("appuyer sur entrer")
print("*******************************************************************")
print("Alice déchiffre le message chiffré \n",cle_public_alice,"\nce qui donne ")
# Déchiffrement RSA avec la clé privée de Bob
dechif=message=""

for i in range(len(message_chiffré_paralice)):
    dechif=CRT(int.from_bytes(message_chiffré_paralice[i],'little'),x1a,x2a,da,na)
    dechif=dechif.to_bytes((dechif.bit_length() + 7) // 8, 'little')

    i=len(dechif)

    while dechif[i-1]!=0:
        i=i-1

    message=message + "".join(dechif[i:].decode())

print(message)
dechif=message
print("*******************************************************************")
print("Alice déchiffre la signature de Bob \n",signe,"\n ce qui donne  en décimal")
designe=home_mod_expnoent(signe, eb, nb)
print(designe)
print("Alice vérifie si elle obtient la même chose avec le hash de ",dechif)
Ahachis0=hashlib.sha256(dechif.encode(encoding='UTF-8',errors='strict')).digest()
Ahachis1=binascii.b2a_uu(Ahachis0)
Ahachis2=Ahachis1.decode()
Ahachis3=home_string_to_int(Ahachis2)
print(Ahachis3%nb)

print(Ahachis3%nb)

print("La différence =",Ahachis3%nb-designe)
if (Ahachis3%nb-designe==0):
    print("Alice : Bob m'a envoyé : ",dechif)
else:
    print("oups")
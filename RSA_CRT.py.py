# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 13:44:40 2020

@author: Mr ABBAS-TURKI
"""
import hashlib
import binascii

def home_mod_expnoent(x,y,n):

    carre=x   

    resultat=1

    while y>0:        
        if y%2==1:

            resultat=(resultat*carre) % n #verifie si y est impaire pour éviter des calculs inutiles
        carre = (carre*carre) % n
        y=y//2

    return resultat           


def home_ext_euclide(y, b):
  
    dividend = y
    divisor = b
    quotient = y // b
    remainder = y % b
    v = [0, 1]
    i = 0

    while remainder != 0:

        i = i + 1
        if i >= 1:
            v.append(v[i-1] - quotient*v[i])
        dividend = divisor
        divisor = remainder
        quotient = dividend // divisor
        remainder = dividend % divisor

    return v[-1] % y

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
    secret=input("donner un secret de 40 caractères au maximum : ")
    while (len(secret)>40):
        secret=input("c'est beaucoup trop long, 40 caractères S.V.P : ")
    return(secret)

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


#voici les éléments de la clé d'Alice
x1a=1841012782626654791989340437774975776878257414906855005095878146390894495346703847473627534121294047 #p
x2a=6694442657485121180631641354634123474242785578652352559107448706134078460922396671024732776460403011 #q
na=x1a*x2a  #n
phia=((x1a-1)*(x2a-1))//home_pgcd(x1a-1,x2a-1)
ea=17 #exposant public
da=home_ext_euclide(phia,ea) #exposant privé
#voici les éléments de la clé de bob
x1b=6129625445896084923399674943303764489975082945366768036587606072410105985004059623133803156960793269 #p
x2b=8445562999779033221275781615876550285943913753598193295171296846596873121082226298324607058064223051 #q
nb=x1b*x2b # n
phib=((x1b-1)*(x2b-1))//home_pgcd(x1b-1,x2b-1)
eb=23 # exposants public
db=home_ext_euclide(phib,eb) #exposant privé

k=25 #Taille du bloc en octet
liste_bloc=[] #liste des blocs 

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
print("*******************************************************************")
print("voici la version en nombre décimal de ",secret," : ")
num_sec=home_string_to_int(secret)
print(num_sec)

print("voici le message chiffré avec la publique d'Alice : ")
chif=home_mod_expnoent(num_sec, ea, na)
print(chif)
print("*******************************************************************")
print("On utilise la fonction de hashage sha 256 pour obtenir le hash du message",secret)
Bhachis0=hashlib.sha256(secret.encode(encoding='UTF-8',errors='strict')).digest() #sha 256 du message
print("voici le hash en nombre décimal ")
Bhachis1=binascii.b2a_uu(Bhachis0)
Bhachis2=Bhachis1.decode() #en string
Bhachis3=home_string_to_int(Bhachis2)
print(Bhachis3)
print("voici la signature avec la clé privée de Bob du hachis")
signe=home_mod_expnoent(Bhachis3, db, nb)
print(signe)
print("*******************************************************************")
print("Bob envoie \n \t 1-le message chiffré avec la clé public d'Alice \n",chif,"\n \t 2-et le hash signé \n",signe)
print("*******************************************************************")
x=input("appuyer sur entrer")
print("*******************************************************************")
print("Alice déchiffre le message chiffré \n",chif,"\nce qui donne ")
dechif=home_int_to_string(CRT(chif,x1a,x2a,da,na))
print(dechif)
print("*******************************************************************")
print("Alice déchiffre la signature de Bob \n",signe,"\n ce qui donne  en décimal")
designe=home_mod_expnoent(signe, eb, nb)
print(designe)
print("Alice vérifie si elle obtient la même chose avec le hash de ",dechif)
Ahachis0=hashlib.sha256(dechif.encode(encoding='UTF-8',errors='strict')).digest()
Ahachis1=binascii.b2a_uu(Ahachis0)
Ahachis2=Ahachis1.decode()
Ahachis3=home_string_to_int(Ahachis2)
print(Ahachis3)
print("La différence =",Ahachis3-designe)
if (Ahachis3-designe==0):
    print("Alice : Bob m'a envoyé : ",dechif)
else:
    print("oups")
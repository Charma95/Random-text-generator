###
###  Gabarit pour l'application de traitement des frequences de mots dans les oeuvres d'auteurs divers
###  Le traitement des arguments a ete inclus:
###     Tous les arguments requis sont presents et accessibles dans args
###     Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
###
###  Frederic Mailhot, 26 fevrier 2018
###    Revise 16 avril 2018
###    Revise 7 janvier 2020

###  Parametres utilises, leur fonction et code a generer
###
###  -d   Deja traite dans le gabarit:  la variable rep_auth contiendra le chemin complet vers le repertoire d'auteurs
###       La liste d'auteurs est extraite de ce repertoire, et est comprise dans la variable authors
###
###
###
###  -P   Si utilise, indique au systeme d'utiliser la ponctuation.  Ce qui est considére comme un signe de ponctuation
###       est defini dans la liste PONC
###       Si -P EST utilise, cela indique qu'on désire conserver la ponctuation (chaque signe est alors considere
###       comme un mot.  Par defaut, la ponctuation devrait etre retiree
###
###  -m   mode d'analyse:  -m 1 indique de faire les calculs avec des unigrammes, -m 2 avec des bigrammes.
###
###  -a   Auteur (unique a traiter).  Utile en combinaison avec -g, -G, pour la generation d'un texte aleatoire
###       avec les caracteristiques de l'auteur indique
###
###  -G   Indique qu'on veut generer un texte (voir -a ci-haut), le nombre de mots à generer doit être indique
###
###  -g   Indique qu'on veut generer un texte (voir -a ci-haut), le nom du fichier en sortie est indique
###
###  -F   Indique qu'on desire connaitre le rang d'un certain mot pour un certain auteur.  L'auteur doit etre
###       donné avec le parametre -a, et un mot doit suivre -F:   par exemple:   -a Verne -F Cyrus
###
###  -v   Deja traite dans le gabarit:  mode "verbose",  va imprimer les valeurs données en parametre
###
###
###  Le systeme doit toujours traiter l'ensemble des oeuvres de l'ensemble des auteurs.  Selon la presence et la valeur
###  des autres parametres, le systeme produira differentes sorties:
###
###  avec -a, -g, -G:  generation d'un texte aleatoire avec les caracteristiques de l'auteur identifie
###  avec -a, -F:  imprimer la frequence d'un mot d'un certain auteur.  Format de sortie:  "auteur:  mot  frequence"
###                la frequence doit être un nombre reel entre 0 et 1, qui represente la probabilite de ce mot
###                pour cet auteur
###  avec -f:  indiquer l'auteur le plus probable du texte identifie par le nom de fichier qui suit -f
###            Format de sortie:  "nom du fichier: auteur"
###  avec ou sans -P:  indique que les calculs doivent etre faits avec ou sans ponctuation
###  avec -v:  mode verbose, imprimera l'ensemble des valeurs des paramètres (fait deja partie du gabarit)


import math
import argparse
import glob
import sys
import os
import math
from pathlib import Path
from random import randint
from random import choice
from functools import reduce

### Ajouter ici les signes de ponctuation à retirer
PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_"]

##  Vous devriez inclure vos classes et méthodes ici, qui seront appellées à partir du main
class Auteur:
    def __init__(self, author, path, m):
        self.author = author
        self.path = path
        self.m = m
        self.dictionnary = {}

## Cette methode normalise le mega dictionnaire
    def normalise_dict(self,dict, list):
        for k in range(len(dict)):
            dict[k] /= len(list)
        return dict

## Cette methode fait
    def listText(self,m):
        m_list = []
        i = 0
        for file in self.path.glob("*.txt"):
            new_dict = self.buildDictionnary(file, m)
            m_list.append(new_dict)
            i += 1
            print("{} is done".format(file))
        return m_list

## Cette methode fait un n-grammes pour tous les auteurs
    def buildDictionnary(self, inFile, m):
      f = open(inFile, 'r', encoding = "utf8")
      list = {}  ## dict
      global PONC
      a = f.read().lower()
      b = "".join([char if char not in PONC else " " for char in a]).split()
      c = [word for word in b if len(word) > m]
      for i in range(len(c) - 1):
          check = " ".join([word for word in c[i -m : i]]).lower()
          if i in list:
              list[check] += 1
          else:
              list[check] = 1
      f.close()
      n_mots = len(c)
      for j in list.keys():
          list[j] /= n_mots

      return list
    
## Cette methode...
    def vector_author(self,m):
        list_text = self.listText(m)
        #for file in self.path.iterdir():
            #list_text.append(self.buildDictionnary(file,m))
            #mergeAuthor(self.m_list[len(self.m_list - 1)])
        #print("{}is done".format(file))

        self.dictionnary = self.normalise_dict(self.dictionnary, list_text)
## Cette methode imprime les dictionnaires
    def view(self, vec=0):
        print("This is {} at {}".format(self.author, self.path))
        if vec:
            print(self.dictionnary)

## Cette methode compare les auteurs et trouvent les distances
    def compare(self, auteur, file, m):
        texte = self.buildDictionnary(file, m)
        norm_a = {x: y/len(norm_a) for x, y in auteur.items() if x in texte}
        norm_t = {x: y/len(norm_t) for x, y in texte.items() if x in auteur}
        return math.sqrt(reduce(lambda x, y: x+y, [(norm_a[x]-norm_t[x])**2 for x in norm_a.keys()]))

## Cette methode trouve le rang de l'occurence
    def getRank(self, word):
        if word in self.dictionnary:
            print("{} has a rank of {} for {}".format(word, self.dictionnary[word], self.author))
        else:
            print("The word {} is not present for {}".format(word, self.author))

## Cette methode mixe tous les n-grammes
    def mergeAuthor(self, new_dict):
        for i, j in new_dict.items():
            if i in self.dictionnary:
                self.dictionnary[i] += new_dict[i]
            else:
                self.dictionnary.update({i:j})
        return self.dictionnary

## Cette methode fait de lart??
    def generateText(self, words, m, title = 0):
        words = words//m
        if title == 0:
            title = "Essaie sur {}".format(self.name)
        f = open(title)
        for i in words:
            f.write("word")
        f.close()



### Main: lecture des paramètres et appel des méthodes appropriées
###
###       argparse permet de lire les paramètres sur la ligne de commande
###             Certains paramètres sont obligatoires ("required=True")
###             Ces paramètres doivent êtres fournis à python lorsque l'application est exécutée
if __name__ == "__main__":
    print("Je suis ici")
    parser = argparse.ArgumentParser(prog='markov_cip1_cip2.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int, choices=range(1, 2),
                        help='Mode (1 ou 2) - unigrammes ou digrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    args = parser.parse_args()

    ### Lecture du répertoire des auteurs, obtenir la liste des auteurs
    ### Note:  args.d est obligatoire
    ### auteurs devrait comprendre la liste des répertoires d'auteurs, peu importe le système d'exploitation
    cwd = os.getcwd()
    if os.path.isabs(args.d):
        rep_aut = args.d
    else:
        rep_aut = os.path.join(cwd, args.d)

    rep_aut = os.path.normpath(rep_aut)
    authors = os.listdir(rep_aut)

    ### Enlever les signes de ponctuation (ou non) - Définis dans la liste PONC
    if args.P:
        remove_ponc = True
    else:
        remove_ponc = False

    ### Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
    if args.v:
        print("Mode verbose:")
        print("Calcul avec les auteurs du repertoire: " + args.d)
        if args.f:
            print("Fichier inconnu a,"
                  " etudier: " + args.f)

        print("Calcul avec des " + str(args.m) + "-grammes")
        if args.F:
            print(str(args.F) + "e mot (ou digramme) le plus frequent sera calcule")

        if args.a:
            print("Auteur etudie: " + args.a)

        if args.P:
            print("Retirer les signes de ponctuation suivants: {0}".format(" ".join(str(i) for i in PONC)))

        if args.G:
            print("Generation d'un texte de " + str(args.G) + " mots")

        if args.g:
            print("Nom de base du fichier de texte genere: " + args.g)

        print("Repertoire des auteurs: " + rep_aut)
        print("Liste des auteurs: ")
        for a in authors:
            aut = a.split("/")
            print("    " + aut[-1])

### À partir d'ici, vous devriez inclure les appels à votre code
    print("Je suis ici")
    for author_path in Path(args.d).iterdir():
        if author_path.name.lower() == args.a.lower():
            auteur = Auteur(args.a, author_path, args.m)
            break
    #auteur = Auteur(args.a, Path(args.d), args.m)
    print(auteur.author)
    print(auteur.path)
    print(auteur.m)
    print("constructeur")
    auteur.vector_author(args.m)
    auteur.getRank("la")
    print(auteur.dictionnary)
    print("fin")




# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

import word
import controller
import random

import array
class statistic():
    t=""
    proposed=0
    wrong=0
    correct=0
    revised_section=""
    def __init__(self,time,proposed,wrong,revised_section):
        self.t = time
        self.proposed = proposed
        self.wrong = wrong
        self.correct = proposed-wrong
        self.revised_section = revised_section
        return
    def print_stat_after_recap(self):
        print("Vocaboli proposti in totale: ",self.proposed)
        print ("Corretti (al primo tentativo): {} ({})".format(self.correct,self.perc_right()))
        print ("Sbagliati (almeno una volta): {} ({})".format(self.wrong,self.perc_wrong()))
        self.print_all_stats()
    def perc_right (self):
        corr_perc = (self.proposed-self.wrong) * 100 / self.proposed
        return  corr_perc
    def perc_wrong (self):
        wrong_perc = self.wrong * 100 / self.proposed
        return wrong_perc
    def stat_for_file(self):
        stringa = str(self.t) + ";"+str(self.proposed)+";"+str(self.wrong)+";"+str(self.revised_section)
        return stringa

    def print_all_stats (self):
        prepareString = "{} - Ripassati: {}, Corretti: {}, ({}%), Sbagliati: {} ({}%), Sezioni ripassate: {}"\
            .format(self.t,self.proposed,self.correct,round(self.perc_right(),2),self.wrong, round(self.perc_wrong(),2),self.revised_section)
        print(prepareString)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def menu():
   print ("Benvenuta/o! Menu principale:")
   choice = input("""
                         R: Ripassa tutto
                         RS: Ripassa una sezione
                         S: Stampa sezioni
                         STAT: Visualizza le tue statistiche
                         Q: Esci dal programma

                         Please enter your choice: """)
   choice = choice.lower()
   if choice == "R" or choice == "r":
       print ("vuoi ripassare tutto")
       ripasso_totale()
       menu()
   elif choice == "RS" or choice == "rs":
       print ("vuoi ripassare una sezione")
       ripassa_sezione()
       menu()
   elif choice == "S" or choice == "s":
       print ("vuoi stampare le sezioni")
       stampa_sezioni()
       menu()
   elif choice == "Q" or choice == "q":
       print ("Alla prossima!")
       exit()
   elif choice == "stat":
        stampa_statistiche()
        menu()
   else:
       print ("scegli tra R, RS, S o Q")
       print ("Per favore riprova")
       menu()

def stampa_sezioni():
    for x in categorie:
        print ("Sezione {}: {}".format(x,categorie[x]))

def stampa_statistiche():
    if len(stats) == 0:
        print ("Non ci sono ancora statistiche")
        return menu()
    print ("Corretti: al primo tentativo, Sbagliati: almeno una volta")
    for x in stats:
        x.print_all_stats()

    menu()

def ripassa_tutto():
    test2 = termini;

    randomValue = random.randint(0,len(test2));
    underAnalysis = termini[randomValue]
    underAnalysis.printTerm()
    typeOfterm = categorie.get(underAnalysis.group)
    underAnalysis.giveChoice(typeOfterm)


def ripasso_totale():
    terms_to_recap = []
    for x in termini:

        terms_to_recap.append(x)
        categories_to_recap=""
        for x in categorie.values():
            categories_to_recap+=x+","

        categories_to_recap=categories_to_recap.removesuffix(",")
    controllerEx.gestisci_ripasso_sezione(terms_to_recap, categorie,categories_to_recap,stats)


def ripassa_sezione():


    stampa_sezioni()

    selezione= input("""Quale sezione/i vuoi ripassare? per ripassare più sezioni usa 1,2,3 etc.: """)
    # print(selezione)
    #print(categorie)
    chosen_section= selezione.split(",")
    for sect in chosen_section:
        if sect not in categorie:
            print ("Selezione non valida, ritorno al menu principale")
            return

    #if we are here all section were ok
    terms_to_recap = []
    chosen_cat_for_stat=""
    for sect in chosen_section:
        #print("sect", sect)


        sezione = categorie.get(sect)
        chosen_cat_for_stat+=sezione+","



        for x in termini:
            #print (x.group, "", sezione)
            if (x.group == sezione):
               # print("Adding term to recap")
                #print(x.right_answer)
                terms_to_recap.append(x)


    sez =categorie.get(sezione)
    # print (len(termini), "" ,len(terms_to_recap))
    chosen_cat_for_stat = chosen_cat_for_stat.removesuffix(",")
    #print (chosen_cat_for_stat)
    #print(terms_to_recaprs)
    controllerEx.gestisci_ripasso_sezione(terms_to_recap, categorie,chosen_cat_for_stat,stats)










# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    filename="vocabolario.txt"
    termini = []
    categorie = {}
    stats = []
    controllerEx = controller.controller();
    controllerEx.welcome_message()
    controllerEx.loadFile(termini,categorie,filename);
    termini_counter=len(termini)
    if termini_counter == 0:
        print ("Nessun termine presente in ",filename," il programma sarà chiuso")
        exit(0)
    else:
        print("Caricati: ",termini_counter,"termini\n\n")

    stats=controllerEx.loadStats(stats)




    #menu()
    #ripassa_tutto()
    #ripassa_sezione("1")
    #ripasso_totale()
    #stampa_sezioni()
    menu()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

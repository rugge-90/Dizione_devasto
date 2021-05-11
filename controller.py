import random
import word
import time
import main
import os


class bcolors:

    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

class controller:
    def loadStats (self,stats):

        if not os.path.exists("stat.txt"):
            f = open("stat.txt", 'a+', encoding='latin')
            #writing header of the file
            f.write("###date,total,correct,revised sections###\n")
            f.close()
            return stats
        f = open("stat.txt", encoding='latin')

        lines=f.readlines()
        stat=None
        for line in lines:
            if not line.startswith("#"):
                stat = self.validate_stat_line(line)
            if stat is not None:
                stats.append(stat)
        return stats


    def validate_stat_line (self,line):
        splitted_line=line.split(";")
        if (len(splitted_line) != 4):
            #this line must be ignored
            return None
        ts=splitted_line[0]
        proposed=splitted_line[1]
        wrong=splitted_line[2]
        try:
            proposed_int=int(proposed)
            wrong_int=int(wrong)
        except ValueError:
            #error is wrong
            return
        #if here alles gut!
        revised_sect=splitted_line[3]
        revised_sect=revised_sect.removesuffix("\n")
        return main.statistic(ts,proposed_int,wrong_int,revised_sect);


    def create_def_file(self,filename):
        f = open(filename, 'a+', encoding='latin')
        # writing header of the file
        f.write("###file vocabolario contiene termini per il ripasso###\n")
        f.write("#formato linea: soluzione;regola;termine;gruppo (; separatore)\n")
        f.write("#esempio soluzione: è,é,e(doppia prununcia)ò,ó,o(doppia pronuncia),ss (s sorda),s(s sonora),sss(doppia prounncia), zz (z sorda), z (z sonora),sss(doppia pronuncia)\n")
        f.write("#esempio regola: dittongo ie\n")
        f.write("#esempio termine: miele ie\n")
        f.write("#esempio gruppo: e,o,s,z\n")
        f.write("#Esempi righe (caricate)::\n")
        f.write("è;rèi,rèbbe,rèbbero del condizionale;amerei;e\n")
        f.write("zzz;iniziale in z con seconda sillaba sorda o sonora: molti vocaboli accettano doppia pronuncia;zimbèllo;z")
        f.close()
    def processa_linea_vocabolo(self,line):

        splittedline = line.split(";")
        if len(splittedline) != 4:
            # every line supposed to have four char
            print(bcolors.FAIL, "Linea: " + line + " ignorata, non contiene 4 campi distinti separati dal \";\"",
                  bcolors.RESET)
            return None
        solution = splittedline[0]
        rule = splittedline[1]
        term = splittedline[2]
        group = splittedline[3]
        splitted_line = line.split(";")


        solution_set = {}
        solution_set["e"]=["è","é","e"]
        solution_set["o"] = ["ò", "ó","o"]
        solution_set["s"] = ["ss", "s","sss"]
        solution_set["z"] = ["zz", "z","zzz"]
        if group not in solution_set.keys():
            print(bcolors.FAIL,"Linea: "+line+" ignorata; Il gruppo: ",group," non è valido",bcolors.RESET)
            return None
        elif solution not in solution_set[group]:
            print(bcolors.FAIL,"Linea: "+line+" ignorata; per il  gruppo: ",group," le soluzioni accettate sono: ",solution_set[group],bcolors.RESET)
            return None
        #if here alles ist gut
        lexic = word.word(solution, rule, term, group)
        return lexic
        possible_solution_set =["è","é","ò","ó"]

    def welcome_message (self):
        print("---------- ")
        print("\nBenvenuta/o")
        print("Come funziona il ripasso? ")
        print("Per le categorie scelte vengono proposti in ordine casuale i vocaboli da ripassare con le opzioni possibli ")
        print("Se sbagli un vocabolo ti verrà riproposto in seguito - l'esercizio finisce quando:")
        print("- L'utente risponde correttamente a tutti i vocaboli proposti (e riproposti) ")
        print("- L'utente sceglie l'opzione \"esci\"")
        print("Calcolo statistiche:")
        print("La prima volta che ti viene proposto un vocabolo nell'esercizio: la risposta viene conteggiata"
              " come giusta o sbagliata")
        print("Quando il vocabolo viene riproposto all'interno dello stesso ripasso non è più considerato ai fini statistici")
        print("Vuoi cancellare le statistiche?\nrimuovi il file stat.txt ne verrà automaticamente generato uno nuovo al "
              "prossimo avvio\n")
        print("Qualche vocabolo da aggiungere? segui la spiegazione nel file vocabolario.txt e aggiungi una riga")
        print("Se la linea è sbagliata verrà ignorata e stampata dal programma in fase di avvio")
        print("\n----------\n ")





    def loadFile(self, termini, categorie,filename):
        distincted_groups=1
        #print ("loading file")
        filename="vocabolario.txt"
        if not os.path.exists(filename):
            self.create_def_file(filename)

        f =  open(filename, encoding='latin')
        lines = f.readlines()
        for line in lines:
            #print ("line under analysis: "+line)
            #line starting with # are ingnored
            if not line.startswith("#"):

                line = line.replace("\n","")

                lexic = self.processa_linea_vocabolo(line)
                if lexic is not None:
                    if lexic.group not in categorie.values():
                            categorie[str(distincted_groups)]= lexic.group;
                            distincted_groups=distincted_groups+1
                    termini.append(lexic)

        f.close()


    def ripasso_in_o (self, term):
        print("\nTermine da ripassare: ", term.term)
        choice = input("""Digita:
                             1 - ò aperta
                             2 - ó chiusa
                             3 - doppia pronuncia ok
                             4 - esci
                             """)
        if choice == 1 or choice == "1":
            if term.right_answer == "ò":
                return True;
            elif term.right_answer == "o":
                print(bcolors.WARNING, "Giusta MA: doppia pronuncia", bcolors.RESET)
                return True
            else:
                return False;
        elif choice == 2 or choice == "2":
            if term.right_answer == "ó":
                return True
            elif term.right_answer == "o":
                print(bcolors.WARNING, "Giusta MA: doppia pronuncia", bcolors.RESET)
                return True
            else:
                return False
        elif choice == 3 or choice == "3":
            if term.right_answer == "o":
                return True
            else:
                return False
        elif choice == 4 or choice == "4":
            return None
        else:
            print("Scelta non valida, ripeti selezione")
            return self.ripasso_in_o(term)

    def add_stat_to_file(self,stat):
        statisticFile = open("stat.txt", 'a', encoding='latin')
        ts = time.gmtime()
        prepare_string = stat.stat_for_file()
        statisticFile.write(prepare_string+"\n")
        statisticFile.close()

    def ripasso_in_e(self, term):
        print("\nTermine da ripassare: ", term.term)
        choice = input("""Digita:
                               1 - è aperta
                               2 - é chiusa
                               3 - doppia pronuncia ok
                               4 - esci
                               """)
        if choice == 1 or choice == "1":
            if term.right_answer == "è":
                return True;
            elif term.right_answer == "e":
                print(bcolors.WARNING, "Giusta MA: doppia pronuncia", bcolors.RESET)
                return True
            else:
                return False;
        elif choice == 2 or choice == "2":
            if (term.right_answer == "é"):
                return True
            elif term.right_answer == "e":
                print(bcolors.WARNING, "Giusta MA: doppia pronuncia", bcolors.RESET)
                return True
            else:
                return False
        elif choice == 3 or choice == "3":
            if term.right_answer == "e":
                return True
            else:
                return False
        elif choice == 4 or choice == "4":
            return None
        else:
            print("Not a valid choice")
            return self.ripasso_in_e(term)

    def ripasso_s(self, term):
        print("\nTermine da ripassare: ", term.term)
        choice = input("""Digita:
                               1 - s sorda / aspra (es. sasso) 
                               2 - s sonora / dolce (es. asilo)
                               3 - doppia pronuncia 
                               4 - esci
                               """)
        if choice == 1 or choice == "1":
            if term.right_answer == "ss":
                return True;
            elif term.right_answer == "sss":
                print(bcolors.WARNING, "Giusta MA: doppia pronuncia", bcolors.RESET)
                return True
            else:
                return False;
        elif choice == 2 or choice == "2":
            if (term.right_answer == "s"):
                return True
            elif term.right_answer == "sss":
                print(bcolors.WARNING, "Giusta MA: doppia pronuncia", bcolors.RESET)
                return True
            else:
                return False
        elif choice == 3 or choice == "3":
            if term.right_answer == "sss":
                return True
            else:
                return False

        elif choice == 4 or choice == "4":
            return None
        else:
            print("Not a valid choice")
            return self.ripasso_in_e(term)

    def ripasso_z(self, term):
        print("\nTermine da ripassare: ", term.term)
        choice = input("""Digita:
                                  1 - z sorda / aspra (es. pazzia) 
                                  2 - z sonora / dolce (es. zanzara)
                                  3 - Doppia pronuncia ok
                                  4 - esci
                                  """)
        if choice == 1 or choice == "1":
            if term.right_answer == "zz":
                return True;
            elif term.right_answer == "zzz":
                print(bcolors.WARNING, "Giusta MA: doppia pronuncia",bcolors.RESET)
                return True;
            else:
                return False;
        elif choice == 2 or choice == "2":
            if (term.right_answer == "z"):
                return True
            elif term.right_answer == "zzz":
                print(bcolors.WARNING, "Giusta MA: doppia pronuncia",bcolors.RESET)
                return True;
            else:
                return False
        elif choice == 3 or choice == "3":
            if (term.right_answer == "zzz"):
                return True
            else:
                return False
        elif choice == 4 or choice == "4":
            return None
        else:
            print("Not a valid choice")
            return self.ripasso_in_e(term)

    def ripassa_vocalbolo (self, term,categorie):
        group=term.group
        if term.group == "o":
            #print("Ripasso in o")
            return self.ripasso_in_o(term)
        if term.group == "e":
            #print("Ripasso in e")
            return self.ripasso_in_e(term)
        if term.group == "s":
            return self.ripasso_s(term)
        if term.group == "z":
            return self.ripasso_z(term)





    def gestisci_ripasso_sezione(self, sezione_da_ripassare, categorie, chosen_cat_for_stat,stats):
        terminate = False
        revised = 0
        total_to_revise = len(sezione_da_ripassare)
        #print(total_to_revise)
        mistakes=0;
        mistakes_collection=[]
        proposed_vocab=0;

        while terminate is False and len(sezione_da_ripassare) > 0:
                randomValue = random.randint(0, len(sezione_da_ripassare)-1)
                vocabolo = sezione_da_ripassare[randomValue]
                result = self.ripassa_vocalbolo(vocabolo,categorie)
                if result is None:
                    terminate = True
                    print("Ritorno al menu principale")

                if result is True:
                    revised=revised+1
                    if vocabolo not in mistakes_collection:
                        proposed_vocab=proposed_vocab+1
                    sezione_da_ripassare.remove(vocabolo)
                    print (bcolors.OK+ "Esatto! hai ripassato ", revised, " su ", total_to_revise, " vocaboli")
                    print ("Hai ancora ", len(sezione_da_ripassare)," da ripassare")
                    print ("Regola: ",vocabolo.printable_solution(), " - " ,vocabolo.rule,bcolors.RESET)
                if result is False:
                    print(bcolors.FAIL + "Sbagliato!\n")
                    print ("Regola: ",vocabolo.printable_solution(), " - " ,vocabolo.rule)

                    print ("Hai ancora ", len(sezione_da_ripassare)," da ripassare",bcolors.RESET)


                    print(vocabolo.rule+bcolors.RESET)
                    if vocabolo not in mistakes_collection:
                        mistakes = mistakes +1;
                        proposed_vocab = proposed_vocab+1;
                        mistakes_collection.append(vocabolo);
                        print ("added to mistake collection")

       # 3*10/100
       #percentage_mistake=revised*100.0/mistakes
       # print (percentage_mistake)
        #choice = input("Hai finito questo ripasso: vuoi vedere come sei andato? Y (per sì), ogni altra scelta tornerà al menù principale")
        #if choice == "Y" or choice == "y":
        print ("Proposed verb to recap: ", proposed_vocab)
        if proposed_vocab == 0:
            return
        ts = time.localtime()


        readablets = time.strftime("%Y-%m-%d %H:%M:%S", ts)
        stat = main.statistic(readablets,proposed_vocab,len(mistakes_collection),chosen_cat_for_stat);
        stat.print_stat_after_recap();



        for x in mistakes_collection:
            termini_sbagliati = x.term+", "
            termini_sbagliati = termini_sbagliati.removesuffix(", ")
            print(termini_sbagliati)

        self.add_stat_to_file(stat)
        stats.append(stat)

        #print ("added stat")



       #  percentage_wrong =
       #  print("Ripassati in totale: ",revised)
       #  return "c"









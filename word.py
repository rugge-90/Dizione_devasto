class word:
    solution = "example"
    rule = "example rule"
    term = "example term"
    right_answer = ""
    group = 1

    #method
    def __init__(self,solution,rule,term,group):
        self.rule = rule
        self.term = term
        self.group = group
        self.right_answer = solution


    def printTerm (self):
        print ("Parola da analizzare: "+self.term)
    def printable_solution (self):
        if self.group == "s":
            if self.right_answer == "ss":

                return "s sorda / aspra (es. sasso)"
            if self.right_answer == "s":

                return "s sonora / dolce (es. asilo)"
            if self.right_answer == "sss":
                return "s con doppia pronuncia accettata"
        elif self.group == "z":
            if self.right_answer == "zz":
                return "z sorda / aspra (es. pazzo)"
            if self.right_answer == "z":
                return "z sonora / dolce (es. zanzara)"
            if self.right_answer == "zzz":
                return "z con doppia pronuncia accettata"
        else:
            return self.right_answer

    def giveChoice (self,type):
        if type == "o" or type == "O":
            choice = input ("""
                            Scegli tra le due seguenti opzioni:
                            1 - ò aperta
                            2 - ò chiusa 
                            3 - esci
                            """)
           # if choice == 1:


        elif type == "e" or type == "e":
            print ("ciao2")

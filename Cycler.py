class Cycler: 
    def __init__(self):
        self.checkers = [] #collection of threads that will run checker functions
        self.relations = []
    #creates the relation objects based off of the database form sever-admin side 
    def load_from_dataBase(self):
        return None 

    def start_checkers(self): 
        for checker in self.checkers: 
            checker.start(); 

    def monitor(self): 
        for relation in relations: 
            if isPulled = True: 
                self.sendOutputSource(relation) 
         
    def sendOutputSource(self, relation): 
        print(relation.outputSource.text)
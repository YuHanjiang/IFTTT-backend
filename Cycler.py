import threading  
import time 
import json

from Relation import Relation  
from Trigger import Trigger 
from OutputSource import OutputSource 
from Checker import Checker

class Cycler: 
    def __init__(self):
        self.checkers = [] #collection of threads that will run checker functions
        self.relations = [] # relations  

        self.testCheckerItem = 0
         

    #creates the relation objects based off of the database form sever-admin side 
    def load_from_dataBase(self):   
        with open("testDB/testRelations.json") as file:
            relationsDB = json.load(file)  
            
            for r in relationsDB: 
                trigger = Trigger(); 
                trigger.src = r["trigger"]["src"]
                trigger.method = r["trigger"]["method"] 
                trigger.condition = r["trigger"]["condition"]     
                trigger.interval = r["trigger"]["interval"] 

                output = OutputSource() 
                output.text = r["output"]["text"] 
                output.severity = r["output"]["severity"] 
                output.key = r["output"]["key"] 
                output.audience = r["output"]["audience"]      

                relation = Relation() 
                relation.trigger = trigger 
                relation.outputSource = output 
                
                self.relations.append(relation)  

        print("relations loaded")

    #create and start threads for each each relation with appropiat checker function
    def start_checkers(self):  
        for relation in self.relations:   
          
                checker = Checker(relation)
                self.checkers.append(threading._start_new_thread(checker.start,()))



    #checks the relations to see if any have been set to true then sends output src
    def monitor(self):  
        while True: 
            length = range(len(self.relations))
            for i in length:
                if self.relations[i].isPulled == True: 
                    self.sendOutputSource(self.relations[i])  
                    self.relations.pop(i) 
                    length = range(len(self.relations)) 
            print("NEXT CHECK")
               

            time.sleep(0.5)
        
         
    def sendOutputSource(self, relation): 
        print(relation.outputSource.text) 
    
def testChecker(relation):  
    while True:
        if 5 > 10: 
            relation.isPulled = True 
            break  
        time.sleep(0.5)


cycler = Cycler() 
cycler.load_from_dataBase() 
cycler.start_checkers() 
cycler.monitor()
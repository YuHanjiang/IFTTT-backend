import threading  
import time 
import json

from Relation import Relation  
from Trigger import Trigger 
from OutputSource import OutputSource

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
                trigger.conditon = r["trigger"]["condition"]     
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
            if relation.trigger.method == "TEST":
                self.checkers.append(threading._start_new_thread(testChecker,(relation,)))
            if relation.trigger.method == "HTTPRESP":  
                self.checkers.append(threading._start_new_thread(testHTTPChecker,(relation,)))



    #checks the relations to see if any have been set to true then sends output src
    def monitor(self):  
        while True:
            for relation in self.relations: 
                if relation.isPulled == True: 
                    self.sendOutputSource(relation)  
                else:  
                    print("stable")  

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
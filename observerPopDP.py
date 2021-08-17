from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from simulation import Simulation

class PopulationSubject(ABC):
    """
    The Publisher/ subject interface
    """

    @abstractmethod
    def subscribe():
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def unsubscribe():
        """
        Detach an observer from the subject.
        """
        pass
    @abstractmethod
    def notify():
        """
        Notifies subscribed observers.
        """
        pass
    


class ConcretePublisher(PopulationSubject):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """
    def __init__(self):
        self._sim = Simulation()
        self._population = self._sim.population
        self._exclusive_display = False 
        self._callbacks: List[ObserverInterface] = []
        self._changes = {"healthy" : [], "sick" : [], "immune" : [], "dead" : [], "infectious" : []}
        
    def subscribe(self, *argv):
        for observer in argv:
            print(f"Publisher: Attached {observer} observer")
            self._callbacks.append(observer)

    def unsubscribe(self, *argv):
        for observer in argv:
            print(f"Publisher: Removed {observer} observer")
            self._callbacks.remove(observer)
        
    def notify(self):
        for observer in self._callbacks:
            observer.summary(self._changes)
            if(self._exclusive_display):
                observer.relatedOnlyInfo(self._population, self._changes)

    """
    The subscription management methods.
    """
        
    def startSimulation(self):  
        self._sim.Config.simulation_steps = 100 
        self._sim.run()
        
    def detectChange(self):
        for i in range(len(self._sim.population)):
            if(self._population[i][6] == 0):
                self._changes["healthy"].append(i)
            elif(self._population[i][6] == 1):
                self._changes["sick"].append(i)
            elif(self._population[i][6] == 2):
                self._changes["immune"].append(i)
            elif(self._population[i][6] == 3):
                self._changes["dead"].append(i)
            elif(self._population[i][6] == 4):
                self._changes["infectious"].append(i)
        self.notify()
        
    def exclusiveDisplay(self, val):
        self._exclusive_display = val
        self.detectChange()     
        
    
    
class ObserverInterface(ABC):
    """
    The Observer interface
    """

    @abstractmethod
    def summary():
        """
        Receive update from Configuration.
        """
        pass

    @abstractmethod
    def relatedOnlyInfo():
        pass
        
    
    
"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""
class HealthyPopulation(ObserverInterface):
    def summary(self, changes):
        print("HealthyPopulation: Below are the person with latest changes\n")
        print(f"Healthy: {changes['healthy']}\n Sick: {changes['sick']}\n Immune: {changes['immune']}\n Dead: {changes['dead']}\n Infectious: {changes['infectious']}\n")

    def relatedOnlyInfo(self, population, changes):
        print(f"HealthyPopulation: Healthy: {changes['healthy']}")
        print("[unique ID, [x,y] coordinate, [x,y] heading, speed, state, age, frame of infection, recovery vector",
              "in treatment, active destination, at destination, [x,y] wander range]", sep=" ")
        for i in changes["healthy"]:
            print(f"{population[i][0]}, [{population[i][1]},{population[i][2]}], [{population[i][3]},{population[i][4]}],", flush= True, end=' ')
            print(f"{population[i][5]}, {population[i][6]}, {population[i][7]}, {population[i][8]}, {population[i][9]}, {population[i][10]}, {population[i][11]}", flush= True, end=' ')
            print(f"{population[i][12]}, [{population[i][13]}, {population[i][14]}]", flush= True, end='\n')
        
class SickPopulation(ObserverInterface):
    def summary(self, changes):
        print("SickPopulation: Below are the person with latest changes\n")
        print(f"Healthy: {changes['healthy']}\n Sick: {changes['sick']}\n Immune: {changes['immune']}\n Dead: {changes['dead']}\n Infectious: {changes['infectious']}\n")

    def relatedOnlyInfo(self, population, changes):
        print(f"SickPopulation: Sick: {changes['sick']}")
        print("[unique ID, [x,y] coordinate, [x,y] heading, speed, state, age, frame of infection, recovery vector",
              "in treatment, active destination, at destination, [x,y] wander range]", sep=" ")
        for i in changes["sick"]:
            print(f"{population[i][0]}, [{population[i][1]},{population[i][2]}], [{population[i][3]},{population[i][4]}],", flush= True, end=' ')
            print(f"{population[i][5]}, {population[i][6]}, {population[i][7]}, {population[i][8]}, {population[i][9]}, {population[i][10]}, {population[i][11]}", flush= True, end=' ')
            print(f"{population[i][12]}, [{population[i][13]}, {population[i][14]}]", flush= True, end='\n')
  
class ImmunePopulation(ObserverInterface):
    def summary(self, changes):
        print("ImmunePopulation: Below are the person with latest changes\n")
        print(f"Healthy: {changes['healthy']}\n Sick: {changes['sick']}\n Immune: {changes['immune']}\n Dead: {changes['dead']}\n Infectious: {changes['infectious']}\n")

    def relatedOnlyInfo(self, population, changes):
        print(f"HealthyPopulation: Immune: {changes['immune']}")
        print("[unique ID, [x,y] coordinate, [x,y] heading, speed, state, age, frame of infection, recovery vector",
              "in treatment, active destination, at destination, [x,y] wander range]", sep=" ")
        for i in changes["immune"]:
            print(f"{population[i][0]}, [{population[i][1]},{population[i][2]}], [{population[i][3]},{population[i][4]}],", flush= True, end=' ')
            print(f"{population[i][5]}, {population[i][6]}, {population[i][7]}, {population[i][8]}, {population[i][9]}, {population[i][10]}, {population[i][11]}", flush= True, end=' ')
            print(f"{population[i][12]}, [{population[i][13]}, {population[i][14]}]", flush= True, end='\n')
        
class DeadPopulation(ObserverInterface):
    def summary(self, changes):
        print("DeadPopulation: Below are the person with latest changes\n")
        print(f"Healthy: {changes['healthy']}\n Sick: {changes['sick']}\n Immune: {changes['immune']}\n Dead: {changes['dead']}\n Infectious: {changes['infectious']}\n")

    def relatedOnlyInfo(self, population, changes):
        print(f"HealthyPopulation: Dead: {changes['dead']}")
        print("[unique ID, [x,y] coordinate, [x,y] heading, speed, state, age, frame of infection, recovery vector",
              "in treatment, active destination, at destination, [x,y] wander range]", sep=" ")
        for i in changes["dead"]:
            print(f"{population[i][0]}, [{population[i][1]},{population[i][2]}], [{population[i][3]},{population[i][4]}],", flush= True, end=' ')
            print(f"{population[i][5]}, {population[i][6]}, {population[i][7]}, {population[i][8]}, {population[i][9]}, {population[i][10]}, {population[i][11]}", flush= True, end=' ')
            print(f"{population[i][12]}, [{population[i][13]}, {population[i][14]}]", flush= True, end='\n')
        
        
class InfectiousPopulation(ObserverInterface):
    def summary(self, changes):
        print("InfectiousPopulation: Below are the person with latest changes\n")
        print(f"Healthy: {changes['healthy']}\n Sick: {changes['sick']}\n Immune: {changes['immune']}\n Dead: {changes['dead']}\n Infectious: {changes['infectious']}\n")

    def relatedOnlyInfo(self, population, changes):
        print(f"InfectiousPopulation: Infectious: {changes['infectious']}")
        print("[unique ID, [x,y] coordinate, [x,y] heading, speed, state, age, frame of infection, recovery vector",
              "in treatment, active destination, at destination, [x,y] wander range]", sep="", flush=True)
        for i in changes["infectious"]:
            print(f"{population[i][0]}, [{population[i][1]},{population[i][2]}], [{population[i][3]},{population[i][4]}],", flush= True, end=' ')
            print(f"{population[i][5]}, {population[i][6]}, {population[i][7]}, {population[i][8]}, {population[i][9]}, {population[i][10]}, {population[i][11]}", flush= True, end=' ')
            print(f"{population[i][12]}, [{population[i][13]}, {population[i][14]}]", flush= True, end='\n')
        
if __name__ == "__main__":
    # The client code.

    CONFIG = ConcretePublisher()
    SICK = SickPopulation()
    INF = InfectiousPopulation()
    CONFIG.subscribe(SICK, INF)
    CONFIG.startSimulation()
    CONFIG.detectChange()
    CONFIG.unsubscribe(INF)
    CONFIG.exclusiveDisplay(True)

    


    

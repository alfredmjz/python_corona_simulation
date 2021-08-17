from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from config import Configuration
from simulation import Simulation

class ConfigurationSubject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
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
    


class ConcreteConfiguration(ConfigurationSubject):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """
    def __init__(self):
        self._config = Configuration()
        self._callbacks: List[ObserverInterface] = []
        self._states = {}
        self.scenario = None
        
    def subscribe(self, *argv):
        for observer in argv:
            print(f"Configuration: Attached {observer} observer")
            self._callbacks.append(observer)

    def unsubscribe(self, *argv):
        for observer in argv:
            print(f"Configuration: Removed {observer} observer")
            self._callbacks.remove(observer)
        
    def notify(self):
        for observer in self._callbacks:
            observer.receiveSignal(self._states)

    """
    The subscription management methods.
    """
        
    def updateParameters(self, setting, value):       
        print(f"Configuration: {setting} has just changed to {value}")
        self._config.set(setting, value)
        self._states[setting] = value
        

    def printConfigurationList(self):
        for key in self._config.__dict__:
            print(key, " = ", self._config.get(key))        
        
    def syncAll(self):
        for observers in self._callbacks:
            observers.sync(self._config)
    
    
class ObserverInterface(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def receiveSignal():
        """
        Receive update from Configuration.
        """
        pass

    @abstractmethod
    def sync(): 
        """
        Sync updated parameters.
        """
        pass
    
    
"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""
class SimulationObserver(ObserverInterface):
    def receiveSignal(self, states):
        print("SimulationObserver: Amendments made: ", states)
        
    def sync(self, config):
        print("SimulationObserver: Syncing new configuration options...\n")
        simulation = Simulation()
        simulation.Config = config
        simulation.population_init()
        simulation.run()
        print("\n")

class ScenarioObserver(ObserverInterface):
    def receiveSignal(self, states):
        print("PopulationObserver: Amendments made: ", states)
    
    def sync(self, config): 
        print("ScenarioObserver: Syncing new configuration options...")
        simulation = Simulation()
        simulation.Config = config
        if(config.lockdown):
            simulation.Config.set_lockdown()
            print(f"Lockdown is set to {simulation.Config.lockdown}")
        if(config.self_isolate):
            simulation.Config.set_self_isolate()
            print(f"Self-isolation is set to {simulation.Config.self_isolate}")
        simulation.population_init()
        simulation.run()
        print("\n")

if __name__ == "__main__":
    # The client code.

    CONFIG = ConcreteConfiguration()
    SIM = SimulationObserver()
    SCE = ScenarioObserver()
    CONFIG.subscribe(SIM, SCE)
    CONFIG.updateParameters("pop_size", 300)
    CONFIG.updateParameters("simulation_steps", 10)
    CONFIG.notify()
    CONFIG.syncAll()
    
    CONFIG.unsubscribe(SIM)
    
    CONFIG.updateParameters("lockdown", True)
    CONFIG.notify()
    CONFIG.syncAll()
    CONFIG.printConfigurationList()


    

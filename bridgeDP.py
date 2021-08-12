from abc import ABC, abstractmethod
from simulation import Simulation


class SimulationAbstraction:
    """
    The abstraction class which is act as the core of Bridge Design Pattern by providing the reference to the implementation
    """
    
    def __init__(self, environment):
        self._simulation = Simulation()
        self._config = self._simulation.Config
        
        self._environment = environment #the environment to run in

    def updatePopulationSize(self, val):
        self._environment.setPopulationSize(self._config, val)
        
    def updateSimulationSteps(self, val):
        self._environment.setSimulationSteps(self._config, val)
        
    def instantiate(self): 
        self._environment.produce_population(self._simulation)
        self._environment.run_simulation(self._simulation)
    

            
    
class SimulationVariants(SimulationAbstraction):
    """
    Extends the SimulationAbstraction without changing the Implementation classes.
    Provides additional variants besides the base in SimulationAbstraction
    """
    def noHealthcare(self):
        self._environment.setHealthcareCapacity(self._config, 0)
    
    def increaseInfectionChance(self, percent):
        self._environment.setInfectionChance(self._config, percent)
    
    def toggleColorblind(self, mode, colorblind_type):
        self._environment.setColorblind(self._config, mode, colorblind_type)
        
    def applyLockdown(self, lockdown_percentage, lockdown_compliance):
        self._environment.setLockdownVariables(self._config, lockdown_percentage, lockdown_compliance)
        self._config.set_lockdown(lockdown_percentage=0.1, lockdown_compliance=0.9)
        
    def applySelfIsolation(self, self_isolate_proportion, isolation_bounds, traveling_infects): 
        self._environment.setSelfIsolationVariables(self._config, self_isolate_proportion, isolation_bounds, traveling_infects)
        self._config.set_self_isolation(self_isolate_proportion=0.9,
                           isolation_bounds = [0.02, 0.02, 0.09, 0.98],
                           traveling_infects=False)

    def applyReducedInteraction(self, speed): 
        self._environment.setReducedInteraction(self._config, speed)
        self._config.set_reduced_interaction(speed = 0.001) 
        
class Implementator(ABC):
    """
    The Implementator defines the interface for all implementation classes. It
    doesn't have to match the Abstraction's interface.
    """
    @abstractmethod
    def setPopulationSize(): pass
    
    @abstractmethod
    def setSimulationSteps() : pass
    
    @abstractmethod
    def setColorblind() : pass

    @abstractmethod
    def produce_population(): pass

    @abstractmethod
    def run_simulation(): pass


"""
Each Concrete Implementation corresponds implements
the Implementation interface
"""

class highDensityPopulation(Implementator):
    """
    The Abstraction maintains a reference to an object of the
    Implementation hierarchy and delegates all of the real work to this object.
    """

    def setPopulationSize(config, val=6000):
        config.pop_size = val
    
    def setSimulationSteps(config, val):
        config.simulation_steps = val
    
    
    def setColorblind(config, mode, colorblind_type="deuteranopia"):
        config.colorblind_mode = mode
        config.colorblind_type = colorblind_type
        
    def setHealthcareCapacity(config, val):
        config.healthcare_capacity = val
    
    def setInfectionChance(config, percent):
        config.infection_chance *= percent
        
    def setLockdownVariables(config, lockdown_percentage, lockdown_compliance):
        config.lockdown_percentage = lockdown_percentage
        config.lockdown_compliance = lockdown_compliance
        
    def setSelfIsolationVariables(config, self_isolate_proportion, isolation_bounds, traveling_infects): 
        config.self_isolate_proportion = self_isolate_proportion
        config.isolation_bounds = isolation_bounds
        config.traveling_infects = traveling_infects
        
    def setReducedInteractionVariables(config, speed): 
        config.speed = speed
        
    def produce_population(simulation):
        simulation.population_init()

    def run_simulation(simulation):
        simulation.run()
        
    

class lowDensityPopulation(Implementator):
    def setPopulationSize(config, val=500):
        config.pop_size = val
    
    def setSimulationSteps(config, val):
        config.simulation_steps = val
    
    def setHealthcareCapacity(config, val):
        config.healthcare_capacity = val
    
    def setInfectionChance(config, percent):
        config.infection_chance *= percent
        
    def setLockdownVariables(config, lockdown_percentage, lockdown_compliance):
        config.lockdown_percentage = lockdown_percentage
        config.lockdown_compliance = lockdown_compliance
        
    def setSelfIsolationVariables(config, self_isolate_proportion, isolation_bounds, traveling_infects): 
        config.self_isolate_proportion = self_isolate_proportion
        config.isolation_bounds = isolation_bounds
        config.traveling_infects = traveling_infects
        
    def setReducedInteractionVariables(config, speed): 
        config.speed = speed
        
    def produce_population(simulation):
        simulation.population_init()

    def run_simulation(simulation):
        simulation.run()
        


if __name__ == "__main__":
    """
    The client code should be able to work with any pre-configured abstraction-
    implementation combination.
    """

    environment = highDensityPopulation
    SIMULATION1 = SimulationAbstraction(environment)
    SIMULATION1.updateSimulationSteps(1000)
    SIMULATION1.updatePopulationSize(5000)
    SIMULATION1.instantiate()

    
    environment = lowDensityPopulation
    SIMULATION2 = SimulationVariants(environment)
    SIMULATION2.increaseInfectionChance(0.2) 
    SIMULATION2.updateSimulationSteps(1000)
    SIMULATION2.applyLockdown(0.5,0.9)
    SIMULATION2.noHealthcare()
    SIMULATION2.instantiate()


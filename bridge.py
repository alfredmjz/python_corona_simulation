from abc import ABC, abstractmethod
from simulation import Simulation


class SimulationAbstraction:
    """
    The abstractin class which is act as the core of Bridge Design Pattern by providing the reference to the implementer
    """
    
    def __init__(self, environment):
        self.__simulation = Simulation()
        self.config = self.__simulation.Config
        
        self.__environment = environment #the environment to run in

    def addScenario(self, scenario):
        if(scenario == None):
            pass  
        
        elif (scenario == "lockdown"):
            self.config.set_lockdown(lockdown_percentage=0.1, lockdown_compliance=0.9)
            
        elif (scenario == "self-isolation"):
            self.config.set_self_isolation(self_isolate_proportion=0.9,
                           isolation_bounds = [0.02, 0.02, 0.09, 0.98],
                           traveling_infects=False)
            
        elif (scenario == "reduced interaction"):
            self.config.set_reduced_interaction(speed = 0.001) 
        
    
    def instantiate(self):
        self.__environment.setPopulationSize(self.config)
        self.__environment.produce_population(self.__simulation)
        self.__environment.run_simulation(self.__simulation)
    

            
    
class SimulationVariants(SimulationAbstraction):
    """
    Extends the SimulationAbstraction without changing the Implementation classes.
    Provides additional function besides the absolute necessary in SimulationAbstraction
    """
    
    def setSimulationSteps(self, val):
        self.config.simulation_steps = val
        
    def noHealthcare(self):
        self.config.healthcare_capacity = 0
    
    def setInfectionChance(self, val):
        self.config.infection_chance = val
    
    def setLockdownVariables(self, lockdown_percentage, lockdown_compliance):
        self.config.lockdown_percentage = lockdown_percentage
        self.config.lockdown_compliance = lockdown_compliance
        
    def setSelfIsolationVariables(self, self_isolate_proportion, isolation_bounds, traveling_infects): 
        self.config.self_isolate_proportion = self_isolate_proportion
        self.config.isolation_bounds = isolation_bounds
        self.config.traveling_infects = traveling_infects
        
    def setReducedInteractionVariables(self, speed): 
        self.config.speed = speed
        
    
        
class Implementation(ABC):
    """
    The Implementation defines the interface for all implementation classes. It
    doesn't have to match the Abstraction's interface.
    """
    @abstractmethod
    def setPopulationSize(): pass
    
    @abstractmethod
    def setPopulationVariables() : pass
    
    @abstractmethod
    def produce_population(): pass

    @abstractmethod
    def run_simulation(): pass

"""
Each Concrete Implementation corresponds implements
the Implementation interface
"""

class highDensityPopulation(Implementation):
    """
    The Abstraction maintains a reference to an object of the
    Implementation hierarchy and delegates all of the real work to this object.
    """

    def setPopulationSize(config):
        config.pop_size = 6000
    
    def setPopulationVariables(config):
        config.mean_age = 45
        config.max_age = 105
        config.age_dependent_risk = True #whether risk increases with age
        config.risk_age = 55 #age where mortality risk starts increasing
        config.critical_age = 75 #age at and beyond which mortality risk reaches maximum
        config.critical_mortality_chance = 0.1 #maximum mortality risk for older age
        config.risk_increase = 'quadratic'
        
    def produce_population(simulation):
        simulation.population_init()

    def run_simulation(simulation):
        simulation.run()
        
    

class lowDensityPopulation(Implementation):
    def setPopulationSize(config):
        config.pop_size = 500
    
    def setPopulationVariables(config):
        config.mean_age = 20
        config.max_age = 55
        config.age_dependent_risk = True #whether risk increases with age
        config.risk_age = 35 #age where mortality risk starts increasing
        config.critical_age = 50 #age at and beyond which mortality risk reaches maximum
        config.critical_mortality_chance = 0.1 #maximum mortality risk for older age
        config.risk_increase = 'exponential'
        
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
    SIMULATION1.addScenario("self-isolation")
    SIMULATION1.instantiate()
    
    environment = lowDensityPopulation
    SIMULATION2 = SimulationVariants(environment)
    SIMULATION2.addScenario("lockdown")
    SIMULATION2.noHealthcare()
    SIMULATION2.instantiate()


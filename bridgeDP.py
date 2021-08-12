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


    def updateSimulationSteps(self, val):
        self._environment.setSimulationSteps(self._config, val)
    
    def toggleColorblind(self, mode, colorblind_type):
        self._environment.setColorblind(self._config, mode, colorblind_type)
    
    def changePlotStyle(self, plot_style):
        self._environment.setPlotStyle(self._config, plot_style)
        
    def instantiate(self):
        self._environment.produce_population(self._simulation)
        self._environment.run_simulation(self._simulation)
    

            
    
class SimulationVariants(SimulationAbstraction):
    """
    Extends the SimulationAbstraction without changing the Implementation classes.
    Provides additional variants besides the base in SimulationAbstraction
    """
    
    def updatePopulationSize(self, val):
        self._environment.setPopulationSize(self._config, val)
        
    def updatePopulationAge(self, mean_age, max_age):
        self._environment.setPopulationAge(self._config, mean_age, max_age)
    
    def enable_ageRiskDependencies(self, risk_age, critical_age, critical_mortality_chance, risk_increase):
        self._environment.ageRiskDependencies(self._config, risk_age, critical_age, 
                                              critical_mortality_chance, risk_increase)
        
    def noHealthcare(self):
        self._environment.setHealthcareCapacity(self._config, 0)
    
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

class populationDependent(Implementator):
    """
    The Abstraction maintains a reference to an object of the
    Implementation hierarchy and delegates all of the real work to this object.
    """

    def setPopulationSize(config, val):
        config.pop_size = val
    
    def setPopulationAge(config, mean_age, max_age):
        config.mean_age = mean_age
        config.max_age = max_age
    
    def ageRiskDependencies(config, risk_age, critical_age, critical_mortality_chance, risk_increase):
        config.age_dependent_risk = True
        config.risk_age = risk_age
        config.critical_age = critical_age
        config.critical_mortality_chance = critical_mortality_chance
        config.risk_increase = risk_increase
        
    def setSimulationSteps(config, val):
        config.simulation_steps = val
    
    def setColorblind(config, mode, colorblind_type):
        config.colorblind_mode = mode
        config.colorblind_type = colorblind_type
    
    def setPlotStyle(config, plot_style):
        config.plot_style = plot_style
    
    def produce_population(simulation):
        simulation.population_init()

    def run_simulation(simulation):
        simulation.run()
        
    

class scenarioDependent(Implementator):
    def setLockdownVariables(config, lockdown_percentage, lockdown_compliance):
        config.lockdown_percentage = lockdown_percentage
        config.lockdown_compliance = lockdown_compliance
        
    def setSelfIsolationVariables(config, self_isolate_proportion, isolation_bounds, traveling_infects): 
        config.self_isolate_proportion = self_isolate_proportion
        config.isolation_bounds = isolation_bounds
        config.traveling_infects = traveling_infects
        
    def setReducedInteractionVariables(config, speed): 
        config.speed = speed

    def setHealthcareCapacity(config, val):
        config.healthcare_capacity = val
       
    def setSimulationSteps(config, val):
        config.simulation_steps = val
    
    def setColorblind(config, mode, colorblind_type):
        config.colorblind_mode = mode
        config.colorblind_type = colorblind_type
    
    def setPlotStyle(config, plot_style):
        config.plot_style = plot_style
        
    def produce_population(simulation):
        simulation.population_init()

    def run_simulation(simulation):
        simulation.run()
        


if __name__ == "__main__":
    """
    The client code should be able to work with any pre-configured abstraction-
    implementation combination.
    """

    environment = populationDependent
    SIMULATION1 = SimulationAbstraction(environment)
    SIMULATION1.updateSimulationSteps(10)
    SIMULATION1.changePlotStyle("dark")
    SIMULATION1.toggleColorblind(True, "deuteranopia")
    SIMULATION1.instantiate()


    SIMULATION2 = SimulationVariants(environment)
    SIMULATION2.updateSimulationSteps(10)
    SIMULATION2.updatePopulationSize(5000)
    SIMULATION2.updatePopulationAge(20,80)
    SIMULATION2.enable_ageRiskDependencies(35, 50, 0.3, "linear")
    SIMULATION2.instantiate()

    
    environment = scenarioDependent
    SIMULATION3 = SimulationAbstraction(environment)
    SIMULATION3.updateSimulationSteps(10)
    SIMULATION3.changePlotStyle("dark")
    SIMULATION3.toggleColorblind(True, "deuteranopia")
    SIMULATION3.instantiate()
    

    SIMULATION4 = SimulationVariants(environment)
    SIMULATION4.updateSimulationSteps(10)
    SIMULATION4.applyLockdown(0.5, 0.9)
    SIMULATION4.noHealthcare()
    SIMULATION4.instantiate()


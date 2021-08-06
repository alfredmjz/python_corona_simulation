from abc import ABCMeta, abstractstaticmethod
from simulation import Simulation

class ISimulationBuilder(metaclass=ABCMeta):
    """The ISimulationBuilder Interface"""

    @abstractstaticmethod
    def getPopulation(self): pass
    
    @abstractstaticmethod
    def getScenario(self): pass
    
    @abstractstaticmethod
    def getPlot(self): pass
    
    @abstractstaticmethod
    def getFig(self): pass
        
class SimulationBuilder(ISimulationBuilder):
    """The Concrete Simulation Builder"""
    
    def __init__(self):
        self.simulation = Simulation()
        self.__config = self.simulation.Config

        
    def setPopulation(self, mean_age, max_age, xbounds, ybounds):
        self.__config.mean_age = mean_age
        self.__config.max_age = max_age
        self.__config.xbounds = xbounds
        self.__config.ybounds = ybounds
        self.__population = self.simulation.population_init
        
    def setScenario(self, scenario):
        if(scenario == None):
            self.__scenario = None
            
        elif(scenario == "lockdown"):
            self.__scenario = self.__config.set_lockdown()
            self.__population = self.simulation.population_init() #reinitialize population to enforce new variables
            
        elif(scenario == "self isolation"):
            self.__scenario = self.__config.set_self_isolation()
            self.__population = self.simulation.population_init() #reinitialize population to enforce new roaming bounds

        elif(scenario == "reduced interaction"):
            self.__scenario = self.__config.set_reduced_interaction()
            self.__population = self.simulation.population_init() #reinitialize population to enforce new speed

           
    def setPlot(self, plot_style, colorblind_mode, colorblind_type):
        self.__config.plot_style = plot_style
        self.__config.colorblind_mode = colorblind_mode
        self.__config.colorblind_type = colorblind_type
        
        self.__plot_palette = self.__config.get_palette()
    
    def set_fig(self, figX, figY):
        self.simulation.figX = figX
        self.simulation.figY = figY
        
    def getPopulation(self):
        return self.__population
    
    def getScenario(self):
        return self.__scenario
    
    def getPlot(self):
        return self.__plot_palette

    def getFig(self):
        return self.__figure
   


class Director():
    "The Director builds a complex representation"
      
    @staticmethod
    def construct():
        "Constructs and runs the Simulation Product"
        SIMULATION = SimulationBuilder()
        SIMULATION.setPopulation(45, 105, [0,1], [0,1])
        SIMULATION.setScenario(None)
        SIMULATION.setPlot("dark", False, 'deuteranopia')
        SIMULATION.set_fig(10, 14)
        SIMULATION.simulation.run()
        

   
if __name__ == "__main__":
    #Client
    Director.construct()

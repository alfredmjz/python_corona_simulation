from abc import ABCMeta, abstractstaticmethod
from simulation import Simulation

class IBuilder(metaclass=ABCMeta):
    """The IBuilder Interface"""

    @abstractstaticmethod
    def setPopulation(self): pass
    
    @abstractstaticmethod
    def setPlot(self): pass
    
    @abstractstaticmethod
    def setFig(self): pass
    
    @abstractstaticmethod
    def setLockdown(self): pass
    
    @abstractstaticmethod
    def setSelfIsolation(self): pass
    
    @abstractstaticmethod
    def setReducedInteraction(self): pass
        

class SimulationBuilder(IBuilder):
    """The Concrete Simulation Builder"""

    def __init__(self):
        self.reset()

      
    def reset(self):
        self.simulation = Simulation() #Product is imported from simulation.py
        self.__config = self.simulation.Config
        self.__config.simulation_steps = 10
 
        
    def setPopulation(self, mean_age=45, max_age=105, xbounds=[0,1], ybounds=[0,1]):
        '''Sets population properties of the simulation'''
        
        self.__config.mean_age = mean_age
        self.__config.max_age = max_age
        self.__config.xbounds = xbounds
        self.__config.ybounds = ybounds
        self.simulation.population_init
        
         
    def setPlot(self, plot_style="default", colorblind_mode = False, colorblind_type="deuteranopia"):
        '''Sets plot style, colorblind mode and colors'''
        
        self.__config.plot_style = plot_style
        self.__config.colorblind_mode = colorblind_mode
        self.__config.colorblind_type = colorblind_type
        self.__config.get_palette()

    
    def setFig(self, figX=5, figY=7):
        '''Sets window's size'''
        
        self.simulation.figX = figX
        self.simulation.figY = figY
        
        
    def setLockdown(self, lockdown_percentage, lockdown_compliance):
        '''Implements lockdown in the simulation'''
        
        self.__config.lockdown_percentage = lockdown_percentage
        self.__config.lockdown_compliance = lockdown_compliance
        self.__config.set_lockdown(lockdown_percentage, lockdown_compliance)
        self.simulation.population_init() #reinitialize population to enforce new variables
        

    def setSelfIsolation(self, self_isolate_proportion, isolation_bounds, traveling_infects):
        '''Implements self isolation in the simulation'''  
        
        self.__config.self_isolate_proportion = self_isolate_proportion
        self.__config.isolation_bounds = isolation_bounds
        self.__config.traveling_infects = traveling_infects
        self.__config.set_self_isolation(self_isolate_proportion, isolation_bounds, traveling_infects)
        self.simulation.population_init() #reinitialize population to enforce new roaming bounds
        
        
    def setReducedInteraction(self,speed):
        '''Implements reduced interaction in the simulation'''
        
        self.__config.speed = speed
        self.__config.set_reduced_interaction(speed)
        self.simulation.population_init() #reinitialize population to enforce new speed
        
        
    def getResult(self):
        return self.simulation.run()
    


class Director():
    "The Director builds a complex representation"
    def __init__(self, builder):
        self.__builder = builder
    
    
    def getBuilder(self):
        return self.__builder
    
    
    def constructDefault(self):
        '''Constructs default and runs the Simulation Product'''
        self.__builder.reset()
        self.__builder.setPopulation()
        self.__builder.setPlot()
        self.__builder.setFig()
        self.__builder.getResult()
    
        
    def constructLockdown(self):
        '''Construct lockdown'''
        
        self.__builder.reset()
        self.__builder.setPopulation(25, 60, [0,2], [0,2])
        self.__builder.setLockdown(0.1, 0.95)
        self.__builder.setPlot("dark")
        self.__builder.setFig(10, 14)
        self.__builder.getResult()
    
        
    def constructSelfIsolation(self):
        '''Construct self isolation'''
        
        self.__builder.reset()
        self.__builder.setPopulation(50, 115, [0,2], [0,2])
        self.__builder.setSelfIsolation(0.9, [0.02, 0.02, 0.09, 0.98], False)
        self.__builder.setPlot("dark")
        self.__builder.setFig(10, 14)
        self.__builder.getResult()


    def constructReducedInteraction(self):
        '''Construct reduced interaction'''
        
        self.__builder.reset()
        self.__builder.setPopulation(32, 60, [0,2], [0,2])
        self.__builder.setReducedInteraction(0.01)
        self.__builder.setPlot("default")
        self.__builder.setFig(10, 14)
        self.__builder.getResult()

   
if __name__ == "__main__":
    "Client"
    
    #Run simulation with default configuration
    builder = SimulationBuilder()       #Initialize and resets simulation
    SIMULATION = Director(builder)
    SIMULATION.constructDefault()
    print("Simulation #1 End\n")
    
    #Run simulation with custom configuration
    builder = SimulationBuilder()       
    builder.setPopulation(50,100,[0,1],[0,1])
    builder.setFig(3,5)
    builder.setPlot("dark", True)
    builder.getResult()
    print("Simulation #2 End\n")
    
    #Run simulation with lockdown configuration
    SIMULATION = Director(builder)
    SIMULATION.constructLockdown()
    print("Simulation #3 End\n")
    
    #Run simulation with self-isolation configuration
    SIMULATION = Director(builder)
    SIMULATION.constructSelfIsolation()
    print("Simulation #4 End\n")
    
    #Run simulation with reduced interaction configuration
    SIMULATION = Director(builder)
    SIMULATION.constructReducedInteraction()
    print("\nSimulation #5 End", "All simulation ends", sep="\n")



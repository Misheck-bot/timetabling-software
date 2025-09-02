import random
import copy
from typing import List, Dict, Tuple, Any
from .genetic_algorithm import GeneticAlgorithm
from .simulated_annealing import SimulatedAnnealing

class HybridOptimizer:
    """
    Hybrid optimization approach combining Genetic Algorithm and Simulated Annealing.
    
    This approach uses GA to explore the solution space broadly and then refines
    the best solutions using SA for local optimization.
    """
    
    def __init__(self, courses, rooms, time_slots, constraints):
        self.courses = courses
        self.rooms = rooms
        self.time_slots = time_slots
        self.constraints = constraints
        
        # Initialize individual algorithms
        self.ga = GeneticAlgorithm(courses, rooms, time_slots, constraints)
        self.sa = SimulatedAnnealing(courses, rooms, time_slots, constraints)
        
        self.best_solution = None
        self.best_fitness = float('inf')
        
    def optimize(self, population_size: int = 50, generations: int = 100,
                mutation_rate: float = 0.1, temperature: float = 1000,
                cooling_rate: float = 0.95, hybrid_ratio: float = 0.7) -> Tuple[Dict, List[float]]:
        """
        Main optimization loop combining GA and SA
        
        Args:
            population_size: Size of GA population
            generations: Number of GA generations
            mutation_rate: GA mutation rate
            temperature: SA initial temperature
            cooling_rate: SA cooling rate
            hybrid_ratio: Ratio of GA vs SA iterations (0.7 = 70% GA, 30% SA)
        """
        
        fitness_history = []
        
        # Phase 1: Genetic Algorithm for broad exploration
        ga_generations = int(generations * hybrid_ratio)
        print(f"Phase 1: Running Genetic Algorithm for {ga_generations} generations...")
        
        ga_solution, ga_fitness_history = self.ga.optimize(
            population_size=population_size,
            generations=ga_generations,
            mutation_rate=mutation_rate,
            crossover_rate=0.8,
            tournament_size=3
        )
        
        fitness_history.extend(ga_fitness_history)
        
        # Update best solution from GA
        if ga_solution['fitness'] < self.best_fitness:
            self.best_solution = copy.deepcopy(ga_solution)
            self.best_fitness = ga_solution['fitness']
        
        print(f"GA Phase completed. Best fitness: {self.best_fitness}")
        
        # Phase 2: Simulated Annealing for local refinement
        sa_iterations = int(generations * (1 - hybrid_ratio))
        print(f"Phase 2: Running Simulated Annealing for {sa_iterations} iterations...")
        
        # Use GA solution as starting point for SA
        self.sa.best_solution = copy.deepcopy(ga_solution)
        self.sa.best_fitness = ga_solution['fitness']
        
        sa_solution, sa_fitness_history = self.sa.optimize(
            initial_temperature=temperature,
            cooling_rate=cooling_rate,
            iterations_per_temp=max(1, sa_iterations // 10),
            max_iterations=sa_iterations * 10
        )
        
        fitness_history.extend(sa_fitness_history)
        
        # Update best solution from SA
        if sa_solution['fitness'] < self.best_fitness:
            self.best_solution = copy.deepcopy(sa_solution)
            self.best_fitness = sa_solution['fitness']
        
        print(f"SA Phase completed. Best fitness: {self.best_fitness}")
        
        # Phase 3: Iterative refinement (optional)
        if self.best_fitness > 0:  # If not perfect solution
            print("Phase 3: Running iterative refinement...")
            refined_solution = self._iterative_refinement()
            
            if refined_solution['fitness'] < self.best_fitness:
                self.best_solution = copy.deepcopy(refined_solution)
                self.best_fitness = refined_solution['fitness']
                print(f"Refinement completed. Final fitness: {self.best_fitness}")
        
        return self.best_solution, fitness_history
    
    def _iterative_refinement(self, max_iterations: int = 50) -> Dict:
        """Iterative refinement using both algorithms in alternating fashion"""
        
        current_solution = copy.deepcopy(self.best_solution)
        current_fitness = current_solution['fitness']
        
        for iteration in range(max_iterations):
            # Alternate between small GA and SA improvements
            if iteration % 2 == 0:
                # Small GA improvement
                improved_solution = self._small_ga_improvement(current_solution)
            else:
                # Small SA improvement
                improved_solution = self._small_sa_improvement(current_solution)
            
            if improved_solution['fitness'] < current_fitness:
                current_solution = improved_solution
                current_fitness = improved_solution['fitness']
                
                # Early stopping if perfect solution found
                if current_fitness == 0:
                    break
        
        return current_solution
    
    def _small_ga_improvement(self, base_solution: Dict) -> Dict:
        """Run a small GA to improve the given solution"""
        # Create a small population starting with the base solution
        small_population = [copy.deepcopy(base_solution)]
        
        # Add some random variations
        for _ in range(4):  # Small population size
            variation = self._create_variation(base_solution)
            small_population.append(variation)
        
        # Run a few generations
        for _ in range(5):  # Small number of generations
            # Selection
            parent1, parent2 = self.ga.select_parents(small_population, tournament_size=2)
            
            # Crossover
            child1, child2 = self.ga.crossover(parent1, parent2, crossover_rate=0.9)
            
            # Mutation
            child1 = self.ga.mutate(child1, mutation_rate=0.2)
            child2 = self.ga.mutate(child2, mutation_rate=0.2)
            
            # Update population
            small_population = [parent1, parent2, child1, child2]
            
            # Sort by fitness
            small_population.sort(key=lambda x: x['fitness'])
        
        return small_population[0]  # Return best solution
    
    def _small_sa_improvement(self, base_solution: Dict) -> Dict:
        """Run a small SA to improve the given solution"""
        # Use the base solution as starting point
        self.sa.best_solution = copy.deepcopy(base_solution)
        self.sa.best_fitness = base_solution['fitness']
        
        # Run SA with low temperature for local search
        improved_solution, _ = self.sa.optimize(
            initial_temperature=100,  # Low temperature for local search
            cooling_rate=0.9,
            iterations_per_temp=10,
            max_iterations=100
        )
        
        return improved_solution
    
    def _create_variation(self, base_solution: Dict) -> Dict:
        """Create a variation of the base solution"""
        variation = copy.deepcopy(base_solution)
        
        # Make a few random changes
        num_changes = random.randint(1, 3)
        for _ in range(num_changes):
            assignment_idx = random.randint(0, len(variation['assignments']) - 1)
            assignment = variation['assignments'][assignment_idx]
            
            if random.random() < 0.5:
                # Change room
                new_room = random.choice(self.rooms)
                assignment['room_id'] = new_room.id
                assignment['room_name'] = new_room.name
            else:
                # Change time slot
                new_time_slot = random.choice(self.time_slots)
                assignment['time_slot_id'] = new_time_slot.id
                assignment['day'] = new_time_slot.day
                assignment['start_time'] = str(new_time_slot.start_time)
                assignment['end_time'] = str(new_time_slot.end_time)
        
        # Recalculate fitness
        variation['fitness'] = self.ga._calculate_fitness(variation)
        return variation
    
    def get_algorithm_info(self) -> Dict:
        """Get information about the hybrid approach"""
        return {
            'name': 'Hybrid GA + SA',
            'description': 'Combines Genetic Algorithm for exploration with Simulated Annealing for refinement',
            'advantages': [
                'Broad solution space exploration through GA',
                'Local optimization through SA',
                'Better convergence than individual algorithms',
                'Escape from local optima',
                'Balanced exploration vs exploitation'
            ],
            'parameters': {
                'population_size': 'Size of GA population',
                'generations': 'Total number of iterations',
                'hybrid_ratio': 'Ratio of GA vs SA iterations',
                'mutation_rate': 'GA mutation probability',
                'temperature': 'SA initial temperature',
                'cooling_rate': 'SA temperature reduction rate'
            }
        }

import random
import numpy as np
from typing import List, Dict, Tuple, Any
import copy
import json

class GeneticAlgorithm:
    """
    Genetic Algorithm implementation for examination timetabling optimization.
    
    This algorithm evolves a population of timetables through selection, crossover,
    and mutation operations to find optimal solutions.
    """
    
    def __init__(self, courses, rooms, time_slots, constraints):
        self.courses = courses
        self.rooms = rooms
        self.time_slots = time_slots
        self.constraints = constraints
        self.population = []
        self.best_solution = None
        self.best_fitness = float('inf')
        
    def initialize_population(self, population_size: int) -> List[Dict]:
        """Initialize a random population of timetables"""
        population = []
        
        for _ in range(population_size):
            timetable = self._generate_random_timetable()
            population.append(timetable)
            
        return population
    
    def _generate_random_timetable(self) -> Dict:
        """Generate a random feasible timetable"""
        timetable = {
            'assignments': [],
            'fitness': 0.0,
            'constraint_violations': 0
        }
        
        # Assign each course to a random room and time slot
        for course in self.courses:
            room = random.choice(self.rooms)
            time_slot = random.choice(self.time_slots)
            
            assignment = {
                'course_id': course.id,
                'course_name': course.name,
                'room_id': room.id,
                'room_name': room.name,
                'time_slot_id': time_slot.id,
                'day': time_slot.day,
                'start_time': str(time_slot.start_time),
                'end_time': str(time_slot.end_time),
                'students': course.students,
                'duration': course.duration
            }
            
            timetable['assignments'].append(assignment)
        
        # Calculate initial fitness
        timetable['fitness'] = self._calculate_fitness(timetable)
        return timetable
    
    def _calculate_fitness(self, timetable: Dict) -> float:
        """Calculate fitness score based on constraint violations"""
        fitness = 0.0
        violations = 0
        
        # Hard constraints (must be satisfied)
        hard_constraint_violations = self._check_hard_constraints(timetable)
        violations += hard_constraint_violations
        
        # Soft constraints (preferred but not mandatory)
        soft_constraint_violations = self._check_soft_constraints(timetable)
        
        # Penalty for hard constraint violations (very high)
        fitness += hard_constraint_violations * 10000
        
        # Penalty for soft constraint violations
        fitness += soft_constraint_violations
        
        timetable['constraint_violations'] = violations
        return fitness
    
    def _check_hard_constraints(self, timetable: Dict) -> int:
        """Check hard constraints that must be satisfied"""
        violations = 0
        
        # Check for student conflicts (no student takes multiple exams simultaneously)
        student_conflicts = self._check_student_conflicts(timetable)
        violations += student_conflicts
        
        # Check room capacity constraints
        room_capacity_violations = self._check_room_capacity(timetable)
        violations += room_capacity_violations
        
        # Check time slot conflicts
        time_conflicts = self._check_time_conflicts(timetable)
        violations += time_conflicts
        
        return violations
    
    def _check_soft_constraints(self, timetable: Dict) -> float:
        """Check soft constraints that are preferred but not mandatory"""
        violations = 0.0
        
        # Check for consecutive exams for same student
        consecutive_violations = self._check_consecutive_exams(timetable)
        violations += consecutive_violations * 0.5
        
        # Check for room preference violations
        room_preference_violations = self._check_room_preferences(timetable)
        violations += room_preference_violations * 0.3
        
        # Check for time distribution violations
        time_distribution_violations = self._check_time_distribution(timetable)
        violations += time_distribution_violations * 0.2
        
        return violations
    
    def _check_student_conflicts(self, timetable: Dict) -> int:
        """Check if any student has conflicting exam times"""
        violations = 0
        
        # Group assignments by time slot
        time_groups = {}
        for assignment in timetable['assignments']:
            time_key = (assignment['day'], assignment['start_time'])
            if time_key not in time_groups:
                time_groups[time_key] = []
            time_groups[time_key].append(assignment)
        
        # Check for conflicts in each time slot
        for time_key, assignments in time_groups.items():
            if len(assignments) > 1:
                # Multiple exams at same time - potential student conflict
                # This is a simplified check; in practice, you'd check actual student enrollments
                violations += len(assignments) - 1
        
        return violations
    
    def _check_room_capacity(self, timetable: Dict) -> int:
        """Check if room capacities are respected"""
        violations = 0
        
        # Group assignments by room and time
        room_time_groups = {}
        for assignment in timetable['assignments']:
            key = (assignment['room_id'], assignment['day'], assignment['start_time'])
            if key not in room_time_groups:
                room_time_groups[key] = []
            room_time_groups[key].append(assignment)
        
        # Check capacity for each room-time combination
        for key, assignments in room_time_groups.items():
            if len(assignments) > 1:
                # Multiple exams in same room at same time
                violations += len(assignments) - 1
        
        return violations
    
    def _check_time_conflicts(self, timetable: Dict) -> int:
        """Check for time-related conflicts"""
        violations = 0
        
        # Check for overlapping time slots
        for i, assignment1 in enumerate(timetable['assignments']):
            for j, assignment2 in enumerate(timetable['assignments'][i+1:], i+1):
                if (assignment1['day'] == assignment2['day'] and
                    assignment1['room_id'] == assignment2['room_id']):
                    # Same day and room - check for time overlap
                    if self._times_overlap(assignment1, assignment2):
                        violations += 1
        
        return violations
    
    def _times_overlap(self, assignment1: Dict, assignment2: Dict) -> bool:
        """Check if two time assignments overlap"""
        # Simplified overlap check - in practice, you'd parse actual times
        return (assignment1['start_time'] == assignment2['start_time'] or
                assignment1['end_time'] == assignment2['end_time'])
    
    def _check_consecutive_exams(self, timetable: Dict) -> int:
        """Check for consecutive exams for same student"""
        violations = 0
        
        # This would require student enrollment data
        # For now, return 0 as placeholder
        return violations
    
    def _check_room_preferences(self, timetable: Dict) -> int:
        """Check room preference violations"""
        violations = 0
        
        # This would check if courses are assigned to preferred room types
        # For now, return 0 as placeholder
        return violations
    
    def _check_time_distribution(self, timetable: Dict) -> int:
        """Check for balanced time distribution"""
        violations = 0
        
        # Check if exams are evenly distributed across days
        day_counts = {}
        for assignment in timetable['assignments']:
            day = assignment['day']
            day_counts[day] = day_counts.get(day, 0) + 1
        
        if day_counts:
            avg_exams_per_day = len(timetable['assignments']) / len(day_counts)
            for day, count in day_counts.items():
                if abs(count - avg_exams_per_day) > 2:  # Allow some variance
                    violations += 1
        
        return violations
    
    def select_parents(self, population: List[Dict], tournament_size: int = 3) -> Tuple[Dict, Dict]:
        """Select two parents using tournament selection"""
        parent1 = self._tournament_selection(population, tournament_size)
        parent2 = self._tournament_selection(population, tournament_size)
        
        # Ensure different parents
        while parent1 == parent2 and len(population) > 1:
            parent2 = self._tournament_selection(population, tournament_size)
        
        return parent1, parent2
    
    def _tournament_selection(self, population: List[Dict], tournament_size: int) -> Dict:
        """Select individual using tournament selection"""
        tournament = random.sample(population, min(tournament_size, len(population)))
        return min(tournament, key=lambda x: x['fitness'])
    
    def crossover(self, parent1: Dict, parent2: Dict, crossover_rate: float = 0.8) -> Tuple[Dict, Dict]:
        """Perform crossover between two parents"""
        if random.random() > crossover_rate:
            return copy.deepcopy(parent1), copy.deepcopy(parent2)
        
        # Single-point crossover
        crossover_point = random.randint(1, len(parent1['assignments']) - 1)
        
        child1 = {
            'assignments': parent1['assignments'][:crossover_point] + parent2['assignments'][crossover_point:],
            'fitness': 0.0,
            'constraint_violations': 0
        }
        
        child2 = {
            'assignments': parent2['assignments'][:crossover_point] + parent1['assignments'][crossover_point:],
            'fitness': 0.0,
            'constraint_violations': 0
        }
        
        # Recalculate fitness for children
        child1['fitness'] = self._calculate_fitness(child1)
        child2['fitness'] = self._calculate_fitness(child2)
        
        return child1, child2
    
    def mutate(self, individual: Dict, mutation_rate: float = 0.1) -> Dict:
        """Perform mutation on an individual"""
        mutated = copy.deepcopy(individual)
        
        for assignment in mutated['assignments']:
            if random.random() < mutation_rate:
                # Randomly change room or time slot
                if random.random() < 0.5:
                    assignment['room_id'] = random.choice(self.rooms).id
                    assignment['room_name'] = assignment['room_id']
                else:
                    new_time_slot = random.choice(self.time_slots)
                    assignment['time_slot_id'] = new_time_slot.id
                    assignment['day'] = new_time_slot.day
                    assignment['start_time'] = str(new_time_slot.start_time)
                    assignment['end_time'] = str(new_time_slot.end_time)
        
        # Recalculate fitness
        mutated['fitness'] = self._calculate_fitness(mutated)
        return mutated
    
    def optimize(self, population_size: int = 50, generations: int = 100, 
                mutation_rate: float = 0.1, crossover_rate: float = 0.8,
                tournament_size: int = 3) -> Tuple[Dict, List[float]]:
        """Main optimization loop"""
        
        # Initialize population
        population = self.initialize_population(population_size)
        fitness_history = []
        
        # Evolution loop
        for generation in range(generations):
            # Calculate fitness for all individuals
            for individual in population:
                individual['fitness'] = self._calculate_fitness(individual)
            
            # Sort population by fitness
            population.sort(key=lambda x: x['fitness'])
            
            # Track best solution
            if not self.best_solution or population[0]['fitness'] < self.best_fitness:
                self.best_solution = copy.deepcopy(population[0])
                self.best_fitness = population[0]['fitness']
            
            # Record average fitness
            avg_fitness = sum(ind['fitness'] for ind in population) / len(population)
            fitness_history.append(avg_fitness)
            
            # Create new population
            new_population = []
            
            # Elitism: keep best 10% of individuals
            elite_size = max(1, population_size // 10)
            new_population.extend(population[:elite_size])
            
            # Generate rest of population through selection, crossover, and mutation
            while len(new_population) < population_size:
                parent1, parent2 = self.select_parents(population, tournament_size)
                child1, child2 = self.crossover(parent1, parent2, crossover_rate)
                
                child1 = self.mutate(child1, mutation_rate)
                child2 = self.mutate(child2, mutation_rate)
                
                new_population.extend([child1, child2])
            
            # Trim to exact population size
            population = new_population[:population_size]
            
            # Early stopping if perfect solution found
            if self.best_fitness == 0:
                break
        
        return self.best_solution, fitness_history

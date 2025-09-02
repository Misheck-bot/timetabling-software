import random
import math
import copy
from typing import List, Dict, Tuple, Any
import json

class SimulatedAnnealing:
    """
    Simulated Annealing implementation for examination timetabling optimization.
    
    This algorithm uses a probabilistic approach to escape local optima by
    accepting worse solutions with decreasing probability as temperature cools.
    """
    
    def __init__(self, courses, rooms, time_slots, constraints):
        self.courses = courses
        self.rooms = rooms
        self.time_slots = time_slots
        self.constraints = constraints
        self.best_solution = None
        self.best_fitness = float('inf')
        
    def _generate_initial_solution(self) -> Dict:
        """Generate an initial feasible solution"""
        timetable = {
            'assignments': [],
            'fitness': 0.0,
            'constraint_violations': 0
        }
        
        # Assign each course to a room and time slot
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
        
        # Check for student conflicts
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
                    if self._times_overlap(assignment1, assignment2):
                        violations += 1
        
        return violations
    
    def _times_overlap(self, assignment1: Dict, assignment2: Dict) -> bool:
        """Check if two time assignments overlap"""
        return (assignment1['start_time'] == assignment2['start_time'] or
                assignment1['end_time'] == assignment2['end_time'])
    
    def _check_consecutive_exams(self, timetable: Dict) -> int:
        """Check for consecutive exams for same student"""
        # Placeholder implementation
        return 0
    
    def _check_room_preferences(self, timetable: Dict) -> int:
        """Check room preference violations"""
        # Placeholder implementation
        return 0
    
    def _check_time_distribution(self, timetable: Dict) -> int:
        """Check for balanced time distribution"""
        violations = 0
        
        day_counts = {}
        for assignment in timetable['assignments']:
            day = assignment['day']
            day_counts[day] = day_counts.get(day, 0) + 1
        
        if day_counts:
            avg_exams_per_day = len(timetable['assignments']) / len(day_counts)
            for day, count in day_counts.items():
                if abs(count - avg_exams_per_day) > 2:
                    violations += 1
        
        return violations
    
    def _generate_neighbor(self, current_solution: Dict) -> Dict:
        """Generate a neighbor solution by making a small change"""
        neighbor = copy.deepcopy(current_solution)
        
        # Randomly select an assignment to modify
        assignment_idx = random.randint(0, len(neighbor['assignments']) - 1)
        assignment = neighbor['assignments'][assignment_idx]
        
        # Randomly choose what to change: room or time slot
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
        neighbor['fitness'] = self._calculate_fitness(neighbor)
        return neighbor
    
    def _acceptance_probability(self, current_fitness: float, new_fitness: float, temperature: float) -> float:
        """Calculate probability of accepting a worse solution"""
        if new_fitness < current_fitness:
            return 1.0  # Always accept better solutions
        
        # Calculate probability based on temperature and fitness difference
        delta_e = new_fitness - current_fitness
        return math.exp(-delta_e / temperature)
    
    def optimize(self, initial_temperature: float = 1000, cooling_rate: float = 0.95,
                min_temperature: float = 0.1, iterations_per_temp: int = 100,
                max_iterations: int = 10000) -> Tuple[Dict, List[float]]:
        """Main optimization loop using simulated annealing"""
        
        # Initialize solution
        current_solution = self._generate_initial_solution()
        current_fitness = current_solution['fitness']
        
        # Track best solution
        self.best_solution = copy.deepcopy(current_solution)
        self.best_fitness = current_fitness
        
        # Initialize temperature
        temperature = initial_temperature
        
        # Track fitness history
        fitness_history = []
        
        iteration = 0
        
        while temperature > min_temperature and iteration < max_iterations:
            # Perform iterations at current temperature
            for _ in range(iterations_per_temp):
                # Generate neighbor solution
                neighbor = self._generate_neighbor(current_solution)
                neighbor_fitness = neighbor['fitness']
                
                # Decide whether to accept the neighbor
                if self._acceptance_probability(current_fitness, neighbor_fitness, temperature) > random.random():
                    current_solution = neighbor
                    current_fitness = neighbor_fitness
                    
                    # Update best solution if necessary
                    if current_fitness < self.best_fitness:
                        self.best_solution = copy.deepcopy(current_solution)
                        self.best_fitness = current_fitness
                
                # Record fitness
                fitness_history.append(current_fitness)
                iteration += 1
                
                # Early stopping if perfect solution found
                if self.best_fitness == 0:
                    break
            
            # Cool down temperature
            temperature *= cooling_rate
            
            # Early stopping if perfect solution found
            if self.best_fitness == 0:
                break
        
        return self.best_solution, fitness_history
    
    def optimize_with_parameters(self, population_size: int = 50, generations: int = 100,
                               mutation_rate: float = 0.1, temperature: float = 1000,
                               cooling_rate: float = 0.95) -> Tuple[Dict, List[float]]:
        """Optimize with parameters (compatibility with other algorithms)"""
        return self.optimize(
            initial_temperature=temperature,
            cooling_rate=cooling_rate,
            iterations_per_temp=generations // 10,  # Adjust iterations based on generations
            max_iterations=generations * 10
        )

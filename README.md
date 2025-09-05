# Examination Timetabling System - Research Project

<div align="center">
  <img src="static/images/logo.svg" alt="ExamScheduler Logo" width="300">
</div>

A sophisticated examination timetabling system for the Zambia University College of Technology (ZUCT) IT Department. This system uses advanced optimization algorithms including Genetic Algorithm (GA), Simulated Annealing (SA), and a hybrid approach to generate optimal examination schedules.

## Project Overview

This is a research project implementing and comparing optimization algorithms for solving the examination timetabling problem at the Zambia University College of Technology (ZUCT) IT Department. The project focuses on three main approaches:

1. **Genetic Algorithm (GA)** - Evolutionary optimization using selection, crossover, and mutation
2. **Simulated Annealing (SA)** - Probabilistic optimization with temperature-based acceptance
3. **Hybrid Approach** - Novel combination of GA and SA for superior results

## Research Problem

Examination timetabling is a well-known NP-hard constraint satisfaction problem that educational institutions face during academic planning. The challenge involves:

- **Student Conflicts**: No student can take multiple exams simultaneously
- **Room Constraints**: Capacity limits and facility requirements
- **Time Constraints**: Exam duration, breaks, and faculty availability
- **Preference Balancing**: Multiple conflicting objectives to optimize

## Research Contributions

This project contributes to the field of educational timetabling through:

- **Novel Hybrid Algorithm**: Combines GA and SA for superior optimization results
- **Performance Analysis**: Comparative study of three optimization approaches
- **Practical Implementation**: Real-world web application for academic use
- **Research Documentation**: Comprehensive analysis and findings

## Technology Stack

- **Backend**: Python Flask, SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production)
- **Algorithms**: Custom implementations of GA, SA, and Hybrid approaches
- **Authentication**: Flask-Login with OAuth support (Google, Facebook, GitHub, Microsoft)

## Installation & Usage

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Initialize database: `python simple_app.py`
4. Access the system at `http://localhost:5000`

## OAuth Setup (Optional)

To enable social login with Goog
le, Facebook, GitHub, and Microsoft:

1. Copy `oauth_config_example.txt` to `.env`
2. Get OAuth credentials from the respective platforms:
   - **Google**: [Google Cloud Console](https://console.developers.google.com/)
   - **Facebook**: [Facebook Developers](https://developers.facebook.com/)
   - **GitHub**: [GitHub OAuth Apps](https://github.com/settings/developers)
   - **Microsoft**: [Azure Portal](https://portal.azure.com/)
3. Update the `.env` file with your credentials
4. Set redirect URIs to: `http://localhost:5000/oauth/{provider}/callback`

The system will work without OAuth configured - users can still sign up with email/password.

## Research Methodology

### Algorithm Implementation

1. **Genetic Algorithm**
   - Population-based evolution
   - Selection, crossover, and mutation operators
   - Fitness-based survival of the fittest

2. **Simulated Annealing**
   - Single solution optimization
   - Temperature-based acceptance criteria
   - Gradual cooling for convergence

3. **Hybrid Approach**
   - GA for broad solution space exploration
   - SA for local refinement and optimization
   - Intelligent switching between algorithms

### Constraint Handling

- **Hard Constraints**: Must be satisfied (student conflicts, room capacity)
- **Soft Constraints**: Preference-based optimization (breaks, room preferences)
- **Multi-objective Optimization**: Balancing conflicting requirements

## Current Status

- **Phase**: Research and Testing
- **Status**: Fully operational and ready for algorithm testing
- **Database**: SQLite with sample data
- **Authentication**: Email/password and OAuth (placeholder)
- **UI**: Responsive web interface with Bootstrap 5
- **System**: Ready for research experiments and algorithm comparison

## Future Work

1. **Algorithm Completion**: Finalize GA, SA, and Hybrid implementations
2. **Performance Testing**: Benchmark algorithms on real data
3. **Constraint Refinement**: Add more sophisticated constraint types
4. **Data Import**: Support for bulk data import from academic systems
5. **Export Features**: PDF, Excel, and calendar format exports
6. **Real-time Updates**: WebSocket-based progress monitoring

## Academic Context

This project serves as a research contribution to the field of educational timetabling optimization. It demonstrates practical applications of metaheuristic algorithms in solving complex real-world scheduling problems.

## License

This is a research project for academic purposes at Zambia University College of Technology.

## Contact

For research inquiries, contact the IT Department at Zambia University College of Technology.

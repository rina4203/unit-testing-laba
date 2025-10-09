Cinema Management System
A console-based application for managing a cinema, created as a project for the "Software Development Tools" course. This project demonstrates a complete development cycle using Git, from repository creation and branching to unit testing and finalizing work with a Pull Request.

Features
Interactive Menu: A user-friendly console interface for navigating all features.

Movie Catalog: Manage a list of movies, search by title, and add new entries.

Screening Schedule: Create and view showtimes for any movie in the catalog.

Booking System: Book tickets for specific screenings and cancel existing bookings.

Requirements
Python 3.8+

Run
Clone the repository:

git clone <your-repository-url>

Navigate to the project root directory:

cd <your-repository-name>

Run the application:

python cinema_system/main.py

The application will start, displaying an interactive menu in your console.

Testing
This project uses Python's built-in unittest framework. The tests cover all core functionalities, including movie management, screening creation, and the booking lifecycle.

To run tests:

From the project root, run the following command:

python -m unittest discover tests

Project Structure
.
├── cinema_system/
│   ├── main.py           # Main application entry point and user interface
│   └── movie_manager.py  # Core logic (Movie, Screening, CinemaManager classes)
├── tests/
│   └── test_cinema_manager.py # Unit tests for the core logic
├── .gitignore            # Specifies intentionally untracked files to ignore
├── LICENSE               # MIT License file
└── README.md             # This file

Contributing & Lab Work Notes
This repository is an educational project. The primary goal is to demonstrate a proper Git workflow:

Branching: All new features (like the unit tests) are developed in separate feature branches (e.g., feature/unit-tests).

Committing: Changes are saved through small, logical commits with descriptive messages.

Pull Requests: Completed work is submitted for review and merging via a Pull Request.

Please feel free to open any issues or suggest any suggestions.

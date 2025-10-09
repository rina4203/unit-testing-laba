# Cinema Management System

A console-based application for managing a cinema. This project was created as part of the **"Software Development Tools"** course and demonstrates the full development cycle using Git — from repository creation and branching to writing unit tests and completing work through a Pull Request.

---

## Description

The program provides basic functionality for managing a cinema: handling a movie catalog, creating screening schedules, booking tickets, and canceling bookings. The interface is a user-friendly console menu.

## Features

- **Interactive Menu** — navigate all features through a console interface.
- **Movie Catalog** — view, search by title, and add new movies.
- **Screening Schedule** — create and view showtimes for any movie.
- **Booking System** — book tickets for specific screenings and cancel existing bookings.

## Requirements

- Python 3.8 or newer

## How to Run

1. Clone the repository:

```bash
git clone <https://github.com/rina4203/unit-testing-laba>
```

2. Navigate to the project root:

```bash
cd <unit-testing-laba>
```

3. Run the application:

```bash
python cinema_system/main.py
```

Once launched, the program will display an interactive console menu.

## Testing

The project uses Python’s built-in `unittest` framework. The tests cover core functionality — movie management, screening creation, and the booking lifecycle.

Run tests from the project root:

```bash
python -m unittest discover tests
```

## Project Structure

```
.
├── cinema_system/
│   ├── main.py           # Main entry point and console interface
│   └── movie_manager.py  # Core logic (Movie, Screening, CinemaManager classes)
├── tests/
│   └── test_cinema_manager.py # Unit tests for the core logic
├── .gitignore            # Ignored files and directories
├── LICENSE               # MIT License file
└── README.md             # This file
```

## Contributing & Lab Notes

This repository is an educational project. Its goal is to demonstrate a proper Git workflow:

- **Branching:** all new features (like unit tests) are developed in dedicated feature branches (e.g., `feature/unit-tests`).
- **Committing:** changes are saved through small, logical commits with descriptive messages.
- **Pull Requests:** completed work is reviewed and merged via Pull Request.

Feel free to open issues or suggest improvements.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.




# Cinema Management System

A console-based application for managing a cinema. This project was created as part of the **"Software Development Tools"** course and demonstrates the full development cycle using Git—from repository creation and branching to writing unit tests and completing work through a Pull Request.

-----

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

1.  Clone the repository:

    ```bash
    git clone https://github.com/rina4203/unit-testing-laba
    ```

2.  Navigate to the project root:

    ```bash
    cd unit-testing-laba
    ```

3.  Run the application. (***Note: The main entry point file needs to be specified.***)

## Testing

The project uses Python’s built-in `unittest` framework. The tests cover core functionality—movie management, screening creation, and the booking lifecycle.

Run tests from the project root:

```bash
python -m unittest discover cinema_system/tests
```

## Project Structure

```
.
├── cinema_system/
│   └── tests/
│       ├── movie_manager_update.py # Updated manager logic (for testing)
│       ├── unit tests(discribe).docx # Test descriptions
│       └── unit_test.py          # Unit tests for the core logic
├── movie.py                # Movie data class
├── movie_manager.py          # Core logic (CinemaManager class)
├── .gitignore              # Ignored files and directories
├── LICENSE                 # MIT License file
├── README.md               # This file
└── ЛБ.docx                 # Lab report document
```

## Contributing & Lab Notes

This repository is an educational project. Its goal is to demonstrate a proper Git workflow:

  - **Branching:** All new features (like unit tests) are developed in dedicated feature branches (e.g., `feature/unit-tests`).
  - **Committing:** Changes are saved through small, logical commits with descriptive messages.
  - **Pull Requests:** Completed work is reviewed and merged into the main branch via a Pull Request.

Feel free to open issues or suggest improvements.

## Documentation

This project's documentation is automatically generated from in-code comments using **Doxygen** and **Graphviz**.

### Local Generation

If you wish to generate the documentation on your local machine:

1.  **Install Doxygen and Graphviz:**

      * [Doxygen (doxygen.exe)](https://www.doxygen.nl/download.html)
      * [Graphviz (dot.exe)](https://graphviz.org/download/)

2.  **Configure `Doxyfile`:**
    Ensure the `Doxyfile` correctly points to your Graphviz installation in the `DOT_PATH` variable (e.g., `DOT_PATH = "C:/Program Files/Graphviz/bin"`).

3.  **Run the command** from the project's root directory:

    ```bash
    doxygen
    ```

4.  **Open the result** in your browser:

    ```bash
    # (for Windows)
    start docs/html/index.html
    ```
## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

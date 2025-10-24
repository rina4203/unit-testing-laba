#!/usr/bin/env python3
"""
@file movie_manager.py
@brief Модуль системи управління кінотеатром.
@details Визначає класи даних для фільмів (Movie), сеансів (Screening)
         та бронювань (Booking), а також головний клас управління
         (CinemaManager), який об'єднує всю логіку.
"""

import json
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class Movie:
    """
    @brief Клас-контейнер даних (dataclass) для представлення фільму.
    @details Містить основну інформацію про фільм, таку як назва, рік,
             режисер, жанри, актори, тривалість та рейтинг.
             Виконує валідацію введених даних у методі `__post_init__`.
    """
    title: str
    year: int
    director: str
    genres: List[str] = field(default_factory=list)
    actors: List[str] = field(default_factory=list)
    runtime_minutes: int = 0
    rating: float = 0.0

    def __post_init__(self):
        """
        @brief Виконує валідацію полів після ініціалізації об'єкта.
        @throws ValueError Якщо рейтинг виходить за межі [0, 10].
        @throws ValueError Якщо рік випуску раніше 1888.
        @throws ValueError Якщо тривалість фільму від'ємна.
        """
        if not (0 <= self.rating <= 10):
            raise ValueError("Рейтинг має бути в межах від 0 до 10.")
        if self.year < 1888:
            raise ValueError("Рік випуску фільму не може бути раніше 1888.")
        if self.runtime_minutes < 0:
            raise ValueError("Тривалість фільму не може бути від'ємною.")

@dataclass
class Screening:
    """
    @brief Клас-контейнер даних (dataclass) для представлення кіносеансу.
    @details Зберігає інформацію про назву фільму, час сеансу,
             загальну кількість місць та кількість заброньованих місць.
             Автоматично генерує унікальний `screening_id` при створенні.
    """
    movie_title: str
    screening_time: str  # Наприклад, "2023-10-27 19:00"
    total_seats: int
    screening_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    booked_seats: int = 0

    @property
    def available_seats(self) -> int:
        """
        @brief Обчислювана властивість для отримання кількості вільних місць.
        @return int Кількість вільних місць (total_seats - booked_seats).
        """
        return self.total_seats - self.booked_seats

@dataclass
class Booking:
    """
    @brief Клас-контейнер даних (dataclass) для представлення бронювання.
    @details Зберігає посилання на ID сеансу, назву фільму та
             кількість заброньованих квитків.
             Автоматично генерує унікальний `booking_id` при створенні.
    """
    screening_id: str
    movie_title: str
    num_tickets: int
    booking_id: str = field(default_factory=lambda: str(uuid.uuid4()))


def create_default_movies() -> List[Movie]:
    """
    @brief Створює та повертає початкову колекцію з 10 фільмів.
    @details Використовується для початкового заповнення `CinemaManager`,
             якщо не надано інший список фільмів.
    @return List[Movie] Список об'єктів `Movie`.
    """
    return [
        Movie("Втеча з Шоушенка", 1994, "Френк Дарабонт", ["Драма"], ["Тім Роббінс", "Морган Фрімен"], 142, 9.3),
        Movie("Хрещений батько", 1972, "Френсіс Форд Коппола", ["Кримінал", "Драма"], ["Марлон Брандо", "Аль Пачіно"], 175, 9.2),
        Movie("Темний лицар", 2008, "Крістофер Нолан", ["Екшн", "Кримінал", "Драма"], ["Крістіан Бейл", "Хіт Леджер"], 152, 9.0),
        Movie("Кримінальне чтиво", 1994, "Квентін Тарантіно", ["Кримінал", "Драма"], ["Джон Траволта", "Ума Турман", "Семюел Л. Джексон"], 154, 8.9),
        Movie("Форрест Гамп", 1994, "Роберт Земекіс", ["Драма", "Романтика"], ["Том Хенкс", "Робін Райт"], 142, 8.8),
        Movie("Початок", 2010, "Крістофер Нолан", ["Екшн", "Пригоди", "Фантастика"], ["Леонардо Ді Капріо", "Джозеф Гордон-Левітт"], 148, 8.8),
        Movie("Матриця", 1999, "Лана Вачовскі", ["Екшн", "Фантастика"], ["Кіану Рівз", "Лоуренс Фішберн"], 136, 8.7),
        Movie("Бійцівський клуб", 1999, "Девід Фінчер", ["Драма"], ["Бред Пітт", "Едвард Нортон"], 139, 8.8),
        Movie("Славні хлопці", 1990, "Мартін Скорсезе", ["Біографія", "Кримінал", "Драма"], ["Роберт Де Ніро", "Рей Ліотта", "Джо Пеші"], 146, 8.7),
        Movie("Паразити", 2019, "Пон Джун Хо", ["Комедія", "Драма", "Трилер"], ["Сон Кан Хо", "Лі Сон Гюн"], 132, 8.6)
    ]


class CinemaManager:
    """
    @brief Головний клас для управління кінотеатром.
    @details Агрегує та керує колекціями фільмів (_movies),
             сеансів (screenings) та бронювань (bookings).
             Надає методи для додавання, пошуку та управління
             цими сутностями.
    """

    def __init__(self, movies: Optional[List[Movie]] = None):
        """
        @brief Конструктор класу CinemaManager.
        @param movies Необов'язковий список фільмів для ініціалізації.
                    Якщо `None`, буде використано список за замовчуванням
                    з `create_default_movies()`.
        """
        self._movies: List[Movie] = movies if movies is not None else create_default_movies()
        self.screenings: List[Screening] = []
        self.bookings: List[Booking] = []

    def get_all_movies(self) -> List[Movie]:
        """
        @brief Повертає повний список фільмів.
        @return List[Movie] Список усіх фільмів, що зберігаються в менеджері.
        """
        return self._movies
        
    def add_movie(self, movie: Movie):
        """
        @brief Додає новий фільм до колекції.
        @details Виконує перевірку на дублікати за назвою (без урахування
                 регістру) та роком, перш ніж додати фільм.
        @param movie Об'єкт `Movie`, який потрібно додати.
        @return None
        """
        for m in self._movies:
            if m.title.lower() == movie.title.lower() and m.year == movie.year:
                return
        self._movies.append(movie)

    def find_movie_by_title(self, title_query: str) -> List[Movie]:
        """
        @brief Знаходить фільми за частковою назвою.
        @details Пошук виконується без урахування регістру.
        @param title_query Рядок для пошуку в назвах фільмів.
        @return List[Movie] Список фільмів, що відповідають запиту.
        """
        return [m for m in self._movies if title_query.lower() in m.title.lower()]


    def add_screening(self, movie_title: str, screening_time: str, total_seats: int) -> Optional[Screening]:
        """
        @brief Додає новий сеанс для існуючого фільму.
        @details Шукає фільм за точною назвою (без урахування регістру).
                 Якщо фільм знайдено, створює новий об'єкт `Screening`
                 та додає його до списку сеансів.
        @param movie_title Точна назва фільму.
        @param screening_time Час сеансу у форматі рядка (напр., "2025-10-28 21:00").
        @param total_seats Загальна кількість місць у залі.
        @return Optional[Screening] Створений об'єкт `Screening` у разі успіху,
                                 або `None`, якщо фільм не знайдено.
        """
        found_movies = [m for m in self._movies if m.title.lower() == movie_title.lower()]
        if not found_movies:
            return None
        
        new_screening = Screening(movie_title=found_movies[0].title, screening_time=screening_time, total_seats=total_seats)
        self.screenings.append(new_screening)
        return new_screening

    def get_screenings_for_movie(self, movie_title: str) -> List[Screening]:
        """
        @brief Повертає всі сеанси для вказаного фільму.
        @details Пошук виконується за частковим збігом назви
                 (без урахування регістру).
        @param movie_title Назва фільму (може бути частковою).
        @return List[Screening] Список сеансів для цього фільму.
        """
        return [s for s in self.screenings if movie_title.lower() in s.movie_title.lower()]

    def get_screening_by_id(self, screening_id: str) -> Optional[Screening]:
        """
        @brief Знаходить сеанс за його унікальним ID.
        @param screening_id Унікальний ідентифікатор сеансу.
        @return Optional[Screening] Знайдений об'єкт `Screening` або `None`.
        """
        for screening in self.screenings:
            if screening.screening_id == screening_id:
                return screening
        return None


    def book_tickets(self, screening_id: str, num_tickets: int) -> Optional[Booking]:
        """
        @brief Бронює вказану кількість квитків на сеанс.
        @details Перевіряє, чи існує сеанс, чи `num_tickets` є додатним
                 числом, і чи достатньо вільних місць.
                 Якщо всі умови виконані, оновлює кількість заброньованих
                 місць на сеансі та створює новий об'єкт `Booking`.
        @param screening_id ID сеансу, на який бронюються квитки.
        @param num_tickets Кількість квитків для бронювання.
        @return Optional[Booking] Створений об'єкт `Booking` у разі успіху,
                                 або `None`, якщо бронювання не вдалося
                                 (невірний ID, недостатньо місць,
                                 некоректна кількість квитків).
        """
        screening = self.get_screening_by_id(screening_id)
        if not screening:
            return None
        
        if not (0 < num_tickets <= screening.available_seats):
            return None
        
        screening.booked_seats += num_tickets
        new_booking = Booking(
            screening_id=screening_id, 
            movie_title=screening.movie_title,
            num_tickets=num_tickets
        )
        self.bookings.append(new_booking)
        return new_booking

    def cancel_booking(self, booking_id: str) -> bool:
        """
        @brief Скасовує бронювання за його ID.
        @details Знаходить бронювання за `booking_id`. Якщо знайдено,
                 знаходить відповідний сеанс та повертає
                 заброньовані квитки (зменшує `booked_seats`).
                 Видаляє об'єкт `Booking` зі списку.
        @param booking_id Унікальний ідентифікатор бронювання,
                          яке потрібно скасувати.
        @return bool `True`, якщо бронювання було успішно знайдено
                     та скасовано, `False` в іншому випадку.
        """
        booking_to_cancel = next((b for b in self.bookings if b.booking_id == booking_id), None)
        
        if not booking_to_cancel:
            return False

        screening = self.get_screening_by_id(booking_to_cancel.screening_id)
        if screening:
            # Повертаємо місця, гарантуючи, що кількість не стане від'ємною
            screening.booked_seats = max(0, screening.booked_seats - booking_to_cancel.num_tickets)
        
        self.bookings.remove(booking_to_cancel)
        return True
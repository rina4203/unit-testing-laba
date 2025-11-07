import json
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

@dataclass
class Movie:
    """
    @brief Клас для представлення фільму з розширеними атрибутами.
    
    @details Зберігає основну інформацію про фільм та виконує базову валідацію даних при ініціалізації.
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
        @brief Валідація даних після ініціалізації об'єкта.
        @throws ValueError Якщо рейтинг виходить за межі [0, 10].
        @throws ValueError Якщо рік випуску менший за 1888.
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
    @brief Клас для представлення кіносеансу.
    @details Містить інформацію про час показу, фільм та кількість місць.
    """
    movie_title: str
    screening_time: str  # Наприклад, "2023-10-27 19:00"
    total_seats: int
    screening_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    booked_seats: int = 0

    @property
    def available_seats(self) -> int:
        """
        @brief Розраховує кількість вільних місць.
        @return Кількість доступних для бронювання місць.
        """
        return self.total_seats - self.booked_seats

@dataclass
class Booking:
    """
    @brief Клас для представлення бронювання.
    @details Зв'язує користувача (імпліцитно) з конкретним сеансом та кількістю місць.
    """
    screening_id: str
    movie_title: str
    num_tickets: int
    booking_id: str = field(default_factory=lambda: str(uuid.uuid4()))


def create_default_movies() -> List[Movie]:
    """
    @brief Створює початковий список фільмів.
    @return Список об'єктів Movie з тестовими даними.
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
    
    @details Цей клас відповідає за управління базою фільмів, розкладом сеансів та обробкою бронювань.
    
    @example
    @code
    manager = CinemaManager()
    movies = manager.find_movie_by_title("Матриця")
    if movies:
        screening = manager.add_screening(movies[0].title, "2023-10-31 20:00", 50)
        manager.book_tickets(screening.screening_id, 2)
    @endcode
    """

    def __init__(self, movies: Optional[List[Movie]] = None):
        """
        @brief Ініціалізація менеджера кінотеатру.
        @param movies Початковий список фільмів. Якщо None, завантажується список за замовчуванням.
        """
        self._movies: List[Movie] = movies if movies is not None else create_default_movies()
        self.screenings: List[Screening] = []
        self.bookings: List[Booking] = []

    def get_all_movies(self) -> List[Movie]:
        """
        @brief Отримати список усіх фільмів.
        @return Список об'єктів Movie.
        """
        return self._movies
        
    def add_movie(self, movie: Movie) -> None:
        """
        @brief Додає новий фільм до колекції.
        @details Фільм додається тільки якщо фільм з такою ж назвою та роком випуску ще не існує.
        @param movie Об'єкт Movie для додавання.
        """
        for m in self._movies:
            if m.title.lower() == movie.title.lower() and m.year == movie.year:
                return
        self._movies.append(movie)

    def find_movie_by_title(self, title_query: str) -> List[Movie]:
        """
        @brief Пошук фільмів за назвою.
        @param title_query Рядок для пошуку (може бути частиною назви).
        @return Список знайдених фільмів.
        """
        return [m for m in self._movies if title_query.lower() in m.title.lower()]

    def add_screening(self, movie_title: str, screening_time: str, total_seats: int) -> Optional[Screening]:
        """
        @brief Додає новий сеанс до розкладу.
        @param movie_title Назва фільму (має точно збігатися з існуючим фільмом).
        @param screening_time Час сеансу у рядковому форматі.
        @param total_seats Загальна кількість місць у залі.
        @return Створений об'єкт Screening або None, якщо фільм не знайдено.
        """
        found_movies = [m for m in self._movies if m.title.lower() == movie_title.lower()]
        if not found_movies:
            return None
        
        new_screening = Screening(movie_title=found_movies[0].title, screening_time=screening_time, total_seats=total_seats)
        self.screenings.append(new_screening)
        return new_screening

    def get_screenings_for_movie(self, movie_title: str) -> List[Screening]:
        """
        @brief Отримати всі сеанси для конкретного фільму.
        @param movie_title Назва фільму для пошуку.
        @return Список сеансів для цього фільму.
        """
        return [s for s in self.screenings if movie_title.lower() in s.movie_title.lower()]

    def get_screening_by_id(self, screening_id: str) -> Optional[Screening]:
        """
        @brief Знайти сеанс за його унікальним ID.
        @param screening_id ID сеансу.
        @return Об'єкт Screening або None, якщо сеанс не знайдено.
        """
        for screening in self.screenings:
            if screening.screening_id == screening_id:
                return screening
        return None

    def book_tickets(self, screening_id: str, num_tickets: int) -> Optional[Booking]:
        """
        @brief Бронювання квитків на сеанс.
        @details Перевіряє наявність сеансу та достатню кількість вільних місць перед бронюванням.
        @param screening_id ID сеансу.
        @param num_tickets Кількість квитків для бронювання (має бути > 0).
        @return Створений об'єкт Booking або None у разі помилки.
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
        @brief Скасування існуючого бронювання.
        @details Знаходить бронювання, повертає місця у сеанс та видаляє запис про бронювання.
        @param booking_id Унікальний ID бронювання.
        @return True, якщо бронювання скасовано успішно, інакше False.
        """
        booking_to_cancel = next((b for b in self.bookings if b.booking_id == booking_id), None)
        
        if not booking_to_cancel:
            return False

        screening = self.get_screening_by_id(booking_to_cancel.screening_id)
        if screening:
            screening.booked_seats -= booking_to_cancel.num_tickets
        
        self.bookings.remove(booking_to_cancel)
        return True
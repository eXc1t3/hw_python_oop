from typing import Dict, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""

    # Константа класса
    MESSAGE_TEMPLATE: str = ("Тип тренировки: {training_type}; "
                             "Длительность: {duration:.3f} ч.; "
                             "Дистанция: {distance:.3f} км; "
                             "Ср. скорость: {speed:.3f} км/ч; "
                             "Потрачено ккал: {calories:.3f}.")

    def __init__(
            self, training_type: str,
            duration: float,
            distance: float,
            speed: float,
            calories: float
    ):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть информационное сообщение в виде строки."""
        info = self.MESSAGE_TEMPLATE.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories
        )
        return info


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_H: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Individual_formula')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )
        return info

    def __str__(self) -> str:
        return f'{self.__class__.__name__}'


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed = self.get_mean_speed()
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                     * speed
                     + self.CALORIES_MEAN_SPEED_SHIFT)
                    * self.weight / self.M_IN_KM
                    * self.duration * 60)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_VELOCITY_MULTIPLIER: float = 0.035
    CALORIES_WEIGHT_MULTIPLIER: float = 0.029
    M_PER_SEC: float = 0.278
    HGT_IN_M: int = 100

    def __init__(
            self, action: int,
            duration: float,
            weight: float,
            height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed = self.get_mean_speed() * self.M_PER_SEC
        calories = ((self.CALORIES_VELOCITY_MULTIPLIER * self.weight
                     + (speed ** 2 / (self.height / self.HGT_IN_M))
                     * self.CALORIES_WEIGHT_MULTIPLIER * self.weight)
                    * (self.duration * self.M_IN_H))
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    MEAN_SPEED_SHIFT: float = 1.1
    MEAN_SPEED_MULTIPLIER: int = 2

    def __init__(
            self, action: int,
            duration: float,
            weight: float,
            length_pool: int,
            count_pool: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM / self.duration
        # переводим в км
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.length_pool\
            * self.count_pool\
            / self.M_IN_KM\
            / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed()
                + self.MEAN_SPEED_SHIFT)\
            * self.MEAN_SPEED_MULTIPLIER\
            * self.weight\
            * self.duration


def read_package(training_type: str, data: list) -> Training:
    """Прочитать данные, полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }

    if ValueError in training_types:
        raise ValueError(f"Unknown workout type: {training_type}")

    training_class = training_types[training_type]
    return training_class(*data)


def main(main_training: Training) -> None:
    """Главная функция."""
    message = main_training.show_training_info()
    print(message.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

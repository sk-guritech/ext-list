from __future__ import annotations


class Person:
    def __init__(self, name: str, age: int):
        self.__name: str = name
        self.__age: int = age

    def introduce(self) -> str:
        return f'{self.name} is {self.age} years old.'

    def get_age_n_years_ago(self, n: int) -> int:
        return self.age - n

    @property
    def name(self) -> str:
        return self.__name

    @property
    def age(self) -> int:
        return self.__age

    def __repr__(self) -> str:
        return f"Person('{self.name}', {self.age})"

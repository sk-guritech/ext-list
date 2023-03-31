# ExtList
This library was created to improve the quality of code through list operations. It allows commonly written list comprehension operations to be called as methods and enables lists to be treated more abstractly than the built-in `list`.

Using this library reduces the number of times list comprehensions need to be written, resulting in improved overall code readability and searchability.

Additionally, `ExtList` ensures that it is an `Iterable` object of a **single type**, which imposes a constraint to only use lists of a single type. This constraint ultimately leads to a simpler program structure.

Note: This library currently supports Python3.10+

## Installation
```
pip install ext-list
```

## Examples
Below are some examples of features of this library.

_Note: In the following examples, the `Person` class is defined as follows._

<details>
    <summary>(class Person)</summary>

    >>> class Person:
    ...     def __init__(self, name, age):
    ...         self.__name = name
    ...         self.__age = age
    ...
    ...     def introduce(self):
    ...         return f'{self.name} is {self.age} years old.'
    ...
    ...     def get_age_n_years_ago(self, n: int) -> int:
    ...        return self.age - n
    ...
    ...     @property
    ...     def name(self):
    ...         return self.__name
    ...
    ...     @property
    ...     def age(self):
    ...         return self.__age
    ...
    ...     def __repr__(self):
    ...         return f'Person(\'{self.name}\', {self.age})'
    ...
</details>

- Extract values
    ```
    >>> person_dicts = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}])
    >>> person_dicts.extract('name')
    ['Alice', 'Bob']

    >>> persons = ExtList(Person('Alice', 25), Person('Bob', 30))
    >>> persons.extract(Person.name)
    ['Alice', 'Bob']

    >>> persons.extract('name')
    ['Alice', 'Bob']

    >>> persons.extract(Person.introduce)
    ['Alice is 25 years old.', 'Bob is 30 years old.']

    >>> persons.extract(Person.get_age_n_years_ago, 5)
    [20, 25]
    ```

- Get matched objects
    ```
    >>> persons = ExtList([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}])
    >>> persons.equals('name', 'Alice')
    [{'name': 'Alice', 'age': 25}]

    >>> persons = ExtList(Person('Alice', 25), Person('Bob', 30))
    >>> persons.equals(Person.name, 'Alice')
    [Person('Alice', 25)]

    >>> persons.equals(Person.introduce, 'Bob is 30 years old.')
    [Person('Bob', 30)]
    ```

- Convert list to dict
    ```
    >>> persons = ExtList([Person('Alice', 25), Person('Bob', 30)])
    >>> persons.to_dict(Person.name)
    {'Alice': Person('Alice', 25), 'Bob': Person('Bob', 30)}
    ```

- Convert list to dict with complex keys
    ```
    >>> persons = ExtList([Person('Alice', 25), Person('Bob', 30)])
    >>> persons.to_dict_with_complex_keys([Person.name, Person.age])
    {('Alice', 25): Person('Alice', 30),
    ('Bob', 30): Person('Bob', 25)}
    ```

See the docs for more examples. (under constructed ...)

_**If you want to see more examples immediately, please check out the Examples section in each method docstring.**_

## requirements
```
typing_extensions
```

## License
[MIT license](https://github.com/sk-guritech/ex-list/blob/master/LICENSE)

## Author
Sakaguchi Ryo ([@GuriTech](https://twitter.com/GuriTech))

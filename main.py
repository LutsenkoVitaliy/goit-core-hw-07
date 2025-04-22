from collections import UserDict
from datetime import datetime, timedelta
import re

class Field:
  def __init__(self, value):
    self.value = value
        
  def __str__(self):
    return str(self.value)

class Name(Field):
  def __init__(self, value):
    if not value:
      raise ValueError('Empty value')
    super().__init__(value)

class Phone(Field):
  def __init__(self, value):
    self._validate(value)
    super().__init__(value)

  @staticmethod
  def _validate(value):
    if not re.fullmatch(r'\d{10}', value):
      raise ValueError("No more than 10 cgaracters")

class Birthday(Field):
  def __init__(self, value):
    try:
      obj_datetime = datetime.strptime(value, "%d.%m.%Y").date()
    except:
      raise ValueError("Invalid date format. Use DD.MM.YYYY")
    super().__init__(obj_datetime)


class Record:
  def __init__(self, name):
    self.name = Name(name)
    self.phones = []
    self.birthday = None

  def add_phone(self, phone: str):
    self.phones.append(Phone(phone))
    
  def remove_phone(self, phone: str): 
    self.phones = [p for p in self.phones if p.value != phone]

  def find_phone(self, find_phone: str): 
    return next(filter(lambda phone: phone.value == find_phone, self.phones), None)

  def edit_phone(self, old_phone_str: str, new_phone_str: str):
    old_phone = self.find_phone(old_phone_str)
    if old_phone:
      new_phone = Phone(new_phone_str)
      index = self.phones.index(old_phone)
      self.phones[index] = new_phone
    else:
      raise ValueError(f'Phone {old_phone} not found')
    
  def add_birthday(self, birthday_str: str):
    self.birthday = Birthday(birthday_str)

  def __str__(self):
    return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict): 
  def add_record(self, contact):
    self.data[contact.name.value] = contact

  def find(self, name):
    if name in self.data:
      return self.data.get(name)
    return None

  def delete(self, name):
    del self.data[name]

  def get_upcoming_birthdays(self):
    current_year = datetime.now().year

    for contact in self.data.values():
      current_birthday = datetime(current_year, contact.birthday.value.month, contact.birthday.value.day) 
      if current_birthday.weekday() >= 5: #if Saturday or Sunday
        current_birthday += timedelta(days=(7-current_birthday.weekday()))
        greeting_date_str = current_birthday.strftime('%Y.%m.%d')
        return f"{greeting_date_str}" 
      else:
        return f"В точку, привітати"


      # greeting_date_str = current_birthday.strftime('%Y.%m.%d')
      # print(greeting_date_str)


  def __str__(self):
    return "\n".join(str(contact) for contact in self.data.values())


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record('John')
john_record.add_phone("1234567890")
john_record.add_birthday("26.4.1996")
book.add_record(john_record) 

# Створення запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday("24.4.1997")
book.add_record(jane_record)

# Виведення всіх записів у книзі
print(book.get_upcoming_birthdays())
# print(book)

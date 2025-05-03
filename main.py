from collections import UserDict
from datetime import datetime, timedelta
from functools import wraps
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
    
  # def remove_phone(self, phone: str): 
  #   self.phones = [p for p in self.phones if p.value != phone]

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
    return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)},\
    birthday: {self.birthday.value.strftime('%d.%m.%Y') if self.birthday else 'Birthday not for this contact.'}"


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
    birthday_list = []

    for contact in self.data.values():
      current_birthday = datetime(current_year, contact.birthday.value.month, contact.birthday.value.day)
      data = current_birthday - datetime.now()
      if data.days <= 7:
        if current_birthday.weekday() >= 5:
          current_birthday += timedelta(days=(7-current_birthday.weekday())) 
          birthday_list.append({"name": contact.name.value, "birthday": current_birthday.strftime('%d.%m.%Y')})
        else:
          birthday_list.append({"name": contact.name.value, "birthday": current_birthday.strftime('%d.%m.%Y')})
    return birthday_list

  def __str__(self):
    return "\n".join(str(contact) for contact in self.data.values())


def input_error(func):
  @wraps(func)
  def inner(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except ValueError:
      return "Give me name and phone number please."
    except KeyError:
      return "Contact not exist."
    except IndexError:
      return "Enter the argument for the command."
  return inner

@input_error
def parse_input(user_input):
  cmd, *args = user_input.split()
  cmd = cmd.strip().lower()
  return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
  name, old_number, new_number = args
  contact = book.find(name)
  if contact:
    contact.edit_phone(old_number, new_number)
    return "Contact phone number update."
  return "Contact not found."

@input_error
def show_phone(args, book: AddressBook):
  name = args[0]
  contact = book.find(name)
  if contact:
    return str(contact)
  return "Contact not found."

@input_error
def show_all_contacts(book: AddressBook):
  return str(book) if book.data else "There are no contacts in phone book."

@input_error
def add_birthday(args, book: AddressBook):
  name, birthday = args
  contact = book.find(name)
  if contact:
    contact.add_birthday(birthday)
    return "Birthday added."
  else:
    return "Contact not found."
  
@input_error
def show_birthday(args, book: AddressBook):
  name = args[0]
  contact = book.find(name)
  if contact and contact.birthday:
    return f"Contact {name}'s birthday is {contact.birthday.value.strftime('%d.%m.%Y')}"
  elif contact:
    return "Birthday not set for this contact."
  else:
    return "Contact not found."
  
@input_error
def birthdays(book: AddressBook):
  all_birthdays = book.get_upcoming_birthdays()
  if not all_birthdays:
    return "The birthday book is empty."
  return '\n'.join(f"Contact {contact['name']}'s birthday is {contact['birthday']}" for contact in all_birthdays)


def main():
  book = AddressBook()
  print("Welcome to the assistant bot!")

  while True:
    user_input = input("Enter a command: ").strip()
    command, *args = parse_input(user_input)

    if command in ["close", "exit"]:
      print("Good bye!")
      break
    elif command == "hello":
      print("How can I help you?")
    elif command == "add":
      print(add_contact(args, book))
    elif command == "change":
      print(change_contact(args, book))
    elif command == "phone":
      print(show_phone(args, book))
    elif command == "all":
      print(show_all_contacts(book))
    elif command == "add-birthday":
      print(add_birthday(args, book))
    elif command == "show-birthday":
      print(show_birthday(args, book))
    elif command == "birthdays":
      print(birthdays(book))
    else:
      print("Invalid command.")


if __name__ == "__main__":
  main()

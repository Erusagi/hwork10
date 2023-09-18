class Field:
    def __init__(self, value=None):
        self.value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        return len(phone) == 10 and phone.isdigit()


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if Phone.validate_phone(new_phone):
            for phone in self.phones:
                if phone.value == old_phone:
                    phone.value = new_phone
                    return
            raise ValueError("Phone not found")
        else:
            raise ValueError("Invalid phone number format")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None


from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]


def main():
    address_book = AddressBook()

    while True:
        user_input = input("Enter a command: ").strip().lower()

        if user_input == "hello":
            print("How can I help you?")
        elif user_input.startswith("add"):
            _, name, phone = user_input.split()
            if name in address_book:
                record = address_book[name]
                record.add_phone(phone)
            else:
                record = Record(name)
                record.add_phone(phone)
                address_book.add_record(record)
            print(f"Phone {phone} added to {name}'s record.")
        elif user_input.startswith("change"):
            _, name, old_phone, new_phone = user_input.split()
            if name in address_book:
                record = address_book[name]
                if record.find_phone(old_phone):
                    record.edit_phone(old_phone, new_phone)
                    print(f"Phone number for {name} changed to {new_phone}")
                else:
                    print(f"Phone number {old_phone} not found in {name}'s record.")
            else:
                print(f"Record for {name} not found.")
        elif user_input.startswith("phone"):
            _, name = user_input.split()
            if name in address_book:
                record = address_book[name]
                if record.phones:
                    print(f"The phone numbers for {name} are:")
                    for phone in record.phones:
                        print(phone.value)
                else:
                    print(f"No phone numbers found for {name}.")
            else:
                print(f"Record for {name} not found.")
        elif user_input == "show all":
            if address_book:
                print("All contacts:")
                for name, record in address_book.items():
                    print(f"{name}:")
                    if record.phones:
                        for phone in record.phones:
                            print(f"  {phone.value}")
            else:
                print("The contact book is empty.")
        elif user_input.startswith("delete"):
            _, name = user_input.split()
            if name in address_book:
                address_book.delete(name)
                print(f"Record for {name} deleted.")
            else:
                print(f"Record for {name} not found.")
        elif user_input in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
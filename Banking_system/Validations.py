import Database
import Bank
import Menus
import hashlib
import re


class Validations:

    @classmethod
    def validation_password(cls, password):
        """
        Hash string twice with SHA512 and return uppercase hex digest, prepended with an asterisk.
        """
        return "*" + hashlib.sha512(hashlib.sha512(password).digest()).hexdigest().upper()

    @classmethod
    def validation_amount_transaction(cls, message):
        """
        Checks whether the information given is a positive integer and limits it at certain amount
        """
        amount = 0
        is_number = False
        get_amount = True
        while not is_number:
            try:
                amount = int(input(message))
            except ValueError:
                print('\nOnly numbers are accepted\n'.upper())
            else:
                if get_amount:
                    if amount > 10000:
                        print('Unfortunately you can not make a transaction over £10,000 at once. '
                              '\nPlease choose another amount.')
                    elif amount <= 0:
                        print('\nPlease enter a valid amount\n'.upper())
                    else:
                        get_amount = True
                        is_number = True
        return amount

    @classmethod
    def validation_user_input(cls, message, possible_inputs, case_sensitive):
        """
        Checks the information given according to the established validation criteria
        """
        user_input = input(message).lower()
        if case_sensitive:
            while user_input not in possible_inputs:
                print('Please enter a valid option')
                user_input = input(message).lower()
        else:
            while user_input not in [choice for choice in possible_inputs]:
                print('Please enter a valid option')
                user_input = input(message)
        return user_input

    @classmethod
    def validation_integer(cls, message):
        """
        Checks whether a given number is a positive integer,looping the function otherwise
        """
        is_valid_amount = False
        amount = 0
        while not is_valid_amount:
            try:
                amount = int(input(message))
                if amount > 0:
                    is_valid_amount = True
                else:
                    print('\nPlease enter a valid information.\n'.upper())
            except ValueError:
                print('\nOnly numbers are accepted\n'.upper())
        return amount

    @classmethod
    def validation_string(cls, message):
        """
        Checks whether the given string contains only letters, looping the function otherwise
        """
        is_valid = False
        string = ''
        while not is_valid:
            string = str(input(message))
            pattern = re.compile(r'[^a-zA-Z]')
            matches = pattern.findall(string)
            if matches or string == '':
                print('\nPlease enter a valid information!\n'.upper())
            else:
                is_valid = True
        return string

    @classmethod
    def validation_account_for_transaction(cls):
        """
        Validates the account whose is going to receive a deposit from the third part without
        being logged, showing to the user the name of the client and asking to confirm
        """
        ask_account = ''
        should_try_again = True
        while should_try_again:
            ask_account = Bank.get_account_number()
            client_info = Database.client_full_introduction(ask_account)
            print('\nThe name of the receiving client is: \n', client_info)
            confirm_deposit = Bank.get_confirmed_transaction()
            if confirm_deposit == 'y' or confirm_deposit == 'yes':
                Validations.validation_amount_for_deposit(ask_account)
                should_try_again = False
            else:
                select_again = Bank.ask_to_try_again()
                if select_again == 'n' or select_again == 'no':
                    Menus.display_initial_menu()
                    should_try_again = False
        return ask_account

    @classmethod
    def validation_amount_for_deposit(cls, account_number):
        """
        Confirms with the client the amount selected for the deposit to be approved or not
        """
        should_try_again = True
        while should_try_again:
            chosen_amount = Bank.get_transaction_amount()
            print('\nThe chosen amount is: £', Bank.set_format(float(chosen_amount)))
            confirmation_amount = Bank.get_confirmed_transaction()
            if confirmation_amount == 'y' or confirmation_amount == 'yes':
                Bank.get_deposit_done(account_number, chosen_amount)
                should_try_again = False
            else:
                ask_another_amount = Bank.ask_to_try_again()
                if ask_another_amount == 'n' or ask_another_amount == 'no':
                    Menus.display_initial_menu()
                    should_try_again = False

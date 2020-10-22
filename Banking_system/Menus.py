import Database
import Bank
import Loans
import Validations
import NewAccount
import time

class Menus:

    @staticmethod
    def string():
        """
        Prints a dashed string
        """
        return print('---------------------------------------------------------------------------------------------')

    @staticmethod
    def n_string():
        """
        Prints a dashed string jumping a line at the beginning
        """
        return print('\n---------------------------------------------------------------------------------------------')

    @staticmethod
    def string_n():
        """
        Prints a dashed string jumping a line at the end
        """
        return print('---------------------------------------------------------------------------------------------\n')

    @classmethod
    def display_initial_menu(cls):
        """
        Displays the initial menu
        """
        Menus.string()
        print('PLEASE CHOOSE ONE OF THE FOLLOWING OPTIONS:')
        Menus.string()
        print('1) OPEN A NEW ACCOUNT')
        print('2) LOGIN INTO YOUR ACCOUNT')
        print('3) DEPOSIT FOR OTHERS')
        print('4) EXIT')
        Menus.string()
        cls.get_user_option()

    @classmethod
    def get_user_option(cls):
        """
        Gets the option from the client
        """
        return cls.user_options(Validations.validation_user_input('OPTION NUMBER: ', ['1', '2', '3', '4'], True))

    @classmethod
    def user_options(cls, chose_option):
        """
        Directs the client according to the requested option
        """
        if chose_option == '1':
            NewAccount.open_new_account()
        elif chose_option == '2':
            Bank.check_account_exists()
        elif chose_option == '3':
            Validations.validation_account_for_transaction()
        elif chose_option == '4':
            Bank.display_goodbye_message()

    @staticmethod
    def holding_time():
        """
        Creates a realistic sensation when the client logs into their account
        """
        return  # print('.'), time.sleep(0.2), print('..'), time.sleep(0.2), print('...'),
        time.sleep(0.2), print('....'), time.sleep(0.2), print('.....'), time.sleep(0.2)

    @classmethod
    def display_main_menu_options(cls, account_number):
        """
        Displays the main menu
        """
        Menus.holding_time()
        print('\n\n' + Database.get_user_introduction(account_number) + ', ACCOUNT: ' + str(account_number))
        Menus.string()
        print('1) CHECK BALANCE')
        print('2) WITHDRAW')
        print('3) DEPOSIT')
        print('4) LOANS')
        print('5) TRANSFER')
        print('6) CLOSE ACCOUNT')
        print('7) EXIT')
        Menus.string_n()
        cls.get_user_choice(account_number)

    @classmethod
    def get_user_choice(cls, account_number):
        """
        Gets the option from the client
        """
        user_choice = Validations.validation_user_input('OPTION NUMBER: ', ['1', '2', '3', '4', '5', '6', '7'], True)
        return cls._get_main_menu_choice(account_number, user_choice)

    @classmethod
    def _get_main_menu_choice(cls, account_number: str, user_choice):
        """
        Directs the client according to the requested option
        """
        if user_choice == '1':
            Bank.display_account(account_number)
        elif user_choice == '2':
            Bank.get_amount_to_withdraw(account_number)
            cls.display_main_menu_options(account_number)
        elif user_choice == '3':
            Bank.deposit(account_number, Bank.get_transaction_amount())
            cls.display_main_menu_options(account_number)
        elif user_choice == '4':
            cls.display_loan_menu(account_number)
        elif user_choice == '5':
            Bank.get_amount_transfer_between_accounts(account_number)
        elif user_choice == '6':
            Bank.account_closure_request(account_number)
        elif user_choice == '7':
            Bank.display_goodbye_message()

    @classmethod
    def display_loan_menu(cls, account_number):
        """
        Displays the loan menu
        """
        Menus.string_n()
        print('<<< DISCLAIMER >>> \n If you choose a loan, you will be subject to an annual interest rate of 2%.')
        Menus.string_n()
        time.sleep(0.7)
        print('\nPLEASE INFORM WHAT YOU WANT TO DO NEXT:\n')
        print('\t' + Database.get_user_introduction(account_number))
        print('\t---------------------------------')
        print('\t1) APPLY FOR A LOAN')
        print('\t2) LOANS STATEMENT')
        print('\t3) LOAN PAYMENT')
        print('\t4) MAIN MENU')
        print('\t---------------------------------')
        cls.get_loan_option(account_number)

    @classmethod
    def get_loan_option(cls, account_number):
        """
        Gets the option from the client
        """
        ask_option = Validations.validation_user_input('\tOPTION NUMBER: ', ['1', '2', '3', '4'], True)
        return cls.loan_options(account_number, ask_option)

    @classmethod
    def loan_options(cls, account_number, ask_option):
        """
        Directs the client according to the requested option
        """
        if ask_option == '1':
            Loans.loan_conditional_factor(account_number, Database.get_income(account_number))
        elif ask_option == '2':
            Loans.display_loan_statement(account_number)
        elif ask_option == '3':
            Loans.loan_payment_check(account_number)
        else:
            Menus.display_main_menu_options(account_number)

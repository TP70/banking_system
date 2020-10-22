import Database
import Menus
import Validations
import time
import NewAccount


class Bank:

    @classmethod
    def account_closure_request(cls, account_number):
        """
        Confirms the client's request and sends it to be analyzed whether it is possible or not
        """
        balance = int(Database.get_balance(account_number))
        get_loans = int(Database.get_loan_amount(account_number))
        want_to_delete_account = Validations.validation_user_input(
            '\nAre you sure you want to delete your account? (y/n) \n', ['y', 'yes', 'n', 'no'], True)
        if want_to_delete_account == 'y':
            if balance == 0 and get_loans == 0:
                cls.delete_bank_account(account_number)
            else:
                cls.account_closure_request_denied(account_number, balance, get_loans)
        else:
            Menus.display_main_menu_options(account_number)

    @classmethod
    def account_closure_request_denied(cls, account_number, balance, get_loans):
        """
        Does not allow the client to close the account while pending debts
        """
        time.sleep(0.8)
        available_overdraft = Database.get_available_overdraft(account_number)
        overdraft_limit = Database.get_overdraft_limit(account_number)
        if balance != 0:
            print('\nYour balance must be ZERO to make this transaction. Your balance is : £ ', cls.set_format(balance))
        elif available_overdraft != overdraft_limit:
            print('\nYour overdraft limit must be unused, so you will need to make a deposit of: £ \n',
                  cls.set_format(abs(overdraft_limit - available_overdraft)))
        elif float(get_loans) > 0:
            print('\nYou have an active loan, to close your account you must need to pay off debts. '
                  'Your current borrowed amount is : £ \n', cls.set_format(get_loans))
        return Menus.display_main_menu_options(account_number)

    @classmethod
    def delete_bank_account(cls, account_number: str):
        """
        Deletes the bank account and erases it's data
        """
        if cls.authenticate_user_password(account_number):
            time.sleep(2)
            print('\n\nThe account was deleted successfully\n\n')
            time.sleep(1)
            print('Thank you for using our services, we hope to see you back, have a good day.\n')
            Database.delete_account(account_number)

    @classmethod
    def get_account_number(cls):
        """
        Asks for the user the account number and validates it via checking in the database
        """
        return Database.get_account_id('Please inform the account: ')

    @classmethod
    def check_account_exists(cls):
        """
        Gets the account number and validates it via checking in the
        database as the first step to login into their account
        """
        account_id = cls.get_account_number()
        if Bank.authenticate_user_password(account_id):
            Database.get_user_introduction(account_id)
            Menus.display_main_menu_options(account_id)

    @classmethod
    def get_existing_password(cls):
        """
        Gets the password from the user and sends it to be hashed
        """
        return Validations.validation_password(input('Please enter your password: ').encode("utf-8"))

    @classmethod
    def authenticate_user_password(cls, account_number):
        """
        Validates the client's password, allowing or not to perform the transaction
        """
        checking_password, should_try_again = False, True
        counter = 4
        while should_try_again:
            Menus.string()
            password_confirmation = cls.get_existing_password()
            if password_confirmation == Database._get_password(account_number):
                checking_password, should_try_again = True, False
            else:
                counter -= 1
                if counter > 1:
                    print('\nWrong Password, try again.', counter, ' Attempts left.\n'.upper())
                elif counter == 1:
                    print('\nWrong Password, try again!', 'This is your last attempt!\n'.upper())
                elif counter == 0:
                    time.sleep(1)
                    print('\n\nYou have reached the maximum number of attempts. \n'
                          'YOUR ACCOUNT IS BLOCKED!, try again later.\n')
                    cls.display_goodbye_message()
                    should_try_again = False
        return checking_password

    @classmethod
    def get_amount_to_withdraw(cls, account_number):
        """
        Validates the amount to withdraw
        """
        return cls.withdraw(
            account_number,
            Validations.validation_amount_transaction('\nPlease inform the amount to withdraw: £ \n')
        )

    @classmethod
    def get_transaction_amount(cls):
        """
        Validates the amount for deposit
        """
        return Validations.validation_amount_transaction('\nPlease inform the transaction amount: £ \n')

    @classmethod
    def withdraw(cls, account_number: str, amount):
        """
        Deduce from the balance, the amount requested from the user
        """
        balance = Database.get_balance(account_number)
        available_overdraft = Database.get_available_overdraft(account_number)
        overdraft_limit = Database.get_overdraft_limit(account_number)
        if amount <= balance:
            balance -= amount
            Database.update_account_balance(balance, account_number)
            print('\nTransaction realised successfully!\n')
        else:
            if balance >= 0 and amount <= (balance + available_overdraft):
                balance -= amount
                Database.update_account_balance(balance, account_number)
                Database.update_available_overdraft(overdraft_limit - abs(balance), account_number)
                print('\nTransaction realised successfully!\n')
            elif balance < 0 and amount <= available_overdraft:
                balance -= amount
                Database.update_account_balance(balance, account_number)
                Database.update_available_overdraft(overdraft_limit - abs(balance), account_number)
                print('\nTransaction realised successfully!\n')
            else:
                cls.withdraw_denied(account_number, balance, available_overdraft)

    @classmethod
    def withdraw_denied(cls, account_number, balance, available_overdraft):
        """"""
        print('\nYour balance is,                   £', cls.set_format(balance))
        print('Your overdraft available is,       £', cls.set_format(available_overdraft))
        print('\nThere is no enough funds!\n'.upper())
        Menus.display_main_menu_options(account_number)

    @classmethod
    def deposit(cls, account_number, amount):
        """
        Allows the user to deposit and update the balance
        """
        balance, overdraft = Database.get_balance(account_number), Database.get_overdraft_limit(account_number)
        available_overdraft = Database.get_available_overdraft(account_number)
        overdraft_difference = abs(overdraft - available_overdraft)
        Database.update_account_balance((balance + amount), account_number)
        print('\nTransaction realised successfully!\n')
        if balance < 0:
            if amount <= overdraft_difference:
                available_overdraft += amount
                Database.update_available_overdraft(available_overdraft, account_number)
            else:
                available_overdraft += overdraft_difference
                Database.update_available_overdraft(available_overdraft, account_number)

    @classmethod
    def get_deposit_done(cls, account_number, chosen_amount):
        """
        Executes the deposit request sending the balance to be updated into the database
        and gives an unique protocol id to the client
        """
        updated_balance = chosen_amount + Database.get_balance(account_number)
        Database.anonymous_deposit(account_number, chosen_amount)
        time.sleep(0.5)
        print('\nTransaction realized successfully!\n')
        print('|------- Protocol transaction: BL', my_cursor.lastrowid, '-------|\n')
        Database.update_account_balance(updated_balance, account_number)
        Menus.display_initial_menu()

    @classmethod
    def display_account(cls, account_number):
        """
        Displays the client's account balance, limits and loans if it has
        """
        loans = float(Database.get_loan_amount(account_number))
        loans_installment = float(Database.get_loan_monthly_payment(account_number))
        balance = Database.get_balance(account_number)
        overdraft_limit = Database.get_overdraft_limit(account_number)
        available_overdraft = Database.get_available_overdraft(account_number)
        print('\nCurrent balance:         £ ', cls.set_format(balance))
        print('Overdraft limit:         £ ', cls.set_format(overdraft_limit))
        if balance >= 0:
            print('Overdraft available:     £ ', cls.set_format(overdraft_limit))
            print('Available amount:        £'.upper(), cls.set_format((balance + overdraft_limit)))
        else:
            print('Overdraft available:     £ ', cls.set_format(available_overdraft))
            print('Available amount:        £ '.upper(), cls.set_format(available_overdraft))
        if loans > 0:
            print('\nLoans:                   £ ', cls.set_format(loans))
            print('Loans installments:      £ ', cls.set_format(loans_installment))
        Menus.display_main_menu_options(account_number)

    @classmethod
    def get_amount_transfer_between_accounts(cls, account_number):
        """
        Gets the validated amount to be transferred between accounts denies it whether is no funds
        """
        should_try_again = True
        while should_try_again:
            amount = cls.get_transaction_amount()
            print('\nThe selected amount is: ', cls.set_format(amount))
            amount_confirmation = cls.get_confirmed_transaction()
            if amount_confirmation == 'y' or amount_confirmation == 'yes':
                balance = Database.get_balance(account_number)
                available_overdraft = Database.get_available_overdraft(account_number)
                if amount < (abs(balance) + available_overdraft):
                    cls.get_account_transfer_between_accounts(account_number, amount)
                    should_try_again = False
                else:
                    cls.withdraw_denied(account_number, balance, available_overdraft)
            else:
                want_to_try_again = cls.ask_to_try_again()
                if want_to_try_again == 'n' or want_to_try_again == 'no':
                    Menus.display_main_menu_options(account_number)
                    should_try_again = False

    @classmethod
    def get_account_transfer_between_accounts(cls, account_number, amount):
        """
        Gets the validated account which is going to receive the money and asks the user to confirm
        """
        should_try_again = True
        while should_try_again:
            receiving_account = cls.get_account_number()
            if receiving_account == account_number:
                print('\nYou can not transfer to the same account you are logged!\n'.upper())
            else:
                client_info = Database.client_full_introduction(receiving_account)
                print('\nThe name of the receiving client is: \n', client_info)
                confirm_transaction = cls.get_confirmed_transaction()
                if confirm_transaction == 'y' or confirm_transaction == 'yes':
                    cls.get_transfer_between_accounts_done(account_number, receiving_account, amount)
                    should_try_again = False
                else:
                    want_to_try_again = cls.ask_to_try_again()
                    if want_to_try_again == 'n' or want_to_try_again == 'no':
                        Menus.display_main_menu_options(account_number)
                        should_try_again = False

    @classmethod
    def transfer_comments(cls):
        """"""
        try_again = True
        get_comment = ''
        while try_again:
            get_comment = input('Comments related to this transaction: ')
            get_length = len(get_comment)
            if get_length > 20:
                print('Your comment must have a maximum of 20 characters. Please try again.')
            else:
                try_again = False
        return get_comment

    @classmethod
    def get_timestamp(cls):
        """"""
        get_date = time.localtime(time.time())
        return '%d-%d-%d %d:%d:%d' % (
            get_date.tm_year, get_date.tm_mday, get_date.tm_mon, get_date.tm_hour, get_date.tm_min, get_date.tm_sec)

    @classmethod
    def get_transfer_between_accounts_done(cls, account_number, receiving_account, amount):
        """
        Executes the transfer according to the given information and sends it to be insert into database
        """
        password_confirmation = cls.authenticate_user_password(account_number)
        transfer_comments = cls.transfer_comments()
        transactions_log = cls.get_timestamp()
        if password_confirmation:
            cls.withdraw(account_number, amount)
            cls.deposit(receiving_account, amount)
            Database.transactions_between_accounts(account_number, receiving_account, transactions_log,
                                                   amount, transfer_comments)
            print('|------- Protocol transaction: TCL', my_cursor.lastrowid, '-------|\n')
            print(transactions_log)
            Menus.display_main_menu_options(account_number)

    @classmethod
    def display_goodbye_message(cls):
        """
        Log off the user
        """
        print('\n£ £ £ THANK YOU FOR USING OUR SERVICES, GOOD BYE. £ £ £\n')
        quit()

    @classmethod
    def set_format(cls, message):
        """
        Defines the number with two decimals
        """
        return format(message, '.2f')

    @classmethod
    def get_confirmed_transaction(cls):
        """
        Validates the client's input through the options listed
        """
        return Validations.validation_user_input('Do you confirm? Y(yes) N(no)\n', ['y', 'yes', 'n', 'no'], True)

    @classmethod
    def ask_to_try_again(cls):
        """
        Validates the client's input through the options listed
        """
        return Validations.validation_user_input('Would you like to try again? Y(yes) N(no)\n',
                                                 ['y', 'yes', 'n', 'no'], True)



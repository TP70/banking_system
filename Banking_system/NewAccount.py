import Database
import Bank
import Menus
import Validations
import math
import re
import time


class NewAccount:

    @classmethod
    def display_welcome_message(cls):
        """
        Displays the welcome message
        """
        print('\n\n     --------£ £ £  Welcome to the Bank of Liberty (BL)  £ £ £--------\n\n'.upper())
        time.sleep(1)

    @classmethod
    def get_first_name(cls):
        """
        Gets the client's first name
        """
        return Validations.validation_string('What is your first name? ')

    @classmethod
    def get_last_name(cls):
        """
        Gets the client's last name
        """
        return Validations.validation_string('What is your surname? ')

    @classmethod
    def password_requirements(cls):
        """
        Displays the requirements to create a new password to the client
        """
        print('\n__________________________________________________')
        print('| CREATING PASSWORD                              |')
        print('| - - - - - - - - - - - - - - - - - - - - - - -  |')
        print('| NOTE: Your password must have at least:        |')
        print('|    > One special character:                    |')
        print('|    > One capital letter                        |')
        print('|    > One lower case                            |')
        print('|    > One number                                |')
        print('|    > 8 characters                              |')
        print('--------------------------------------------------')

    @classmethod
    def get_new_password(cls):
        """
        Creates the password
        """
        cls.password_requirements()
        checking_new_pw = False
        matched_pw = False
        repeat_new_pw = ''
        if repeat_new_pw == '':
            while not checking_new_pw:
                new_pw = input('\nPlease create a new password: ')
                if len(new_pw) < 8:
                    print("The password has less than 8 characters!")
                elif re.search('[0-9]', new_pw) is None:
                    print("Number is missing!")
                elif re.search('[a-z]', new_pw) is None:
                    print("Lower case is missing!")
                elif re.search('[A-Z]', new_pw) is None:
                    print("Capital letter is missing!")
                elif re.search('[-`!#$%&()*+,.:;<=>?@^_{|}~]', new_pw) is None:
                    print("Special character is missing!")
                elif (len(set(new_pw).intersection({'[', ']', '\\', "'", '"'}))) != 0:
                    print("\nSpecial character not allowed for security reasons!".upper())
                else:
                    checking_new_pw = True
                    while not matched_pw:
                        repeat_new_pw = input('Please repeat the password: ')
                        if new_pw != repeat_new_pw:
                            time.sleep(1)
                            print('We are processing your information, please wait...\n')
                            time.sleep(1.5)
                            print(' Sorry, passwords do not match please try again')
                        else:
                            repeat_new_pw = Validations.validation_password(repeat_new_pw.encode("utf-8"))
                            matched_pw = True
                            time.sleep(1.5)
                            print('\nYour password has been defined!\n')
            return repeat_new_pw

    @classmethod
    def get_title(cls):
        """
        Gets the client's title
        """
        user_gender = Validations.validation_user_input('What is gender? F(Female) M(Male): ',
                                                        ['f', 'female', 'm', 'male'], True)
        if user_gender == 'f' or user_gender == 'female':
            user_gender = 'Ms.'
        else:
            user_gender = 'Mr.'
        return user_gender

    @classmethod
    def ask_income(cls):
        """
        Gets the client's income
        """
        return Validations.validation_integer('What is your annual income? £ ')

    @classmethod
    def income_validation(cls):
        """
        Checks if the income meets the bank's necessary requirements
        """
        should_try_again = True
        income = 0
        while should_try_again:
            income = cls.ask_income()
            if income > 1000000:
                print('\n\t\t\t"As we are a retail bank, we aim for client with income of up to £ 1M.'
                      '\n\t\t\tSo we ask you to check with our management team '
                      '\n\t\t\tHow we can best serve you via our exclusive channels. Have a nice day."\n\n')
                choose_again = Bank.ask_to_try_again()
                if choose_again == 'n' or choose_again == 'no':
                    Menus.display_initial_menu()
                    should_try_again = False
            else:
                should_try_again = False
        return income

    @classmethod
    def overdraft_suggestion(cls, income):
        """
        Calculates an overdraft according to the informed income and offers it to the client
        """
        conditional_factor = 25
        get_overdraft = format(int(math.ceil((income / conditional_factor) / 100)) * 100, '.2f')
        Menus.n_string()
        print('We would like to offer you an', ' overdraft limit of: £'.upper(), str(get_overdraft))
        print('FREE of Interest Rate for one month. (*After this period, the IR will be 5% per month)\n\n')
        accept_overdraft = Bank.get_confirmed_transaction()
        if accept_overdraft == 'n' or accept_overdraft == 'no':
            get_overdraft = 0
        return get_overdraft

    @classmethod
    def get_new_balance(cls):
        """
        Gets the first deposit to activate the new account
        """
        print('\nAs it is a new account,\nYou have to make your first deposit to activate your account.\n')
        time.sleep(0.7)
        return Bank.get_transaction_amount()

    @classmethod
    def get_mobile_number(cls):
        """
        Verifies whether the number has eleven digits to be validated
        """
        try_again = True
        mobile_number = 0
        while try_again:
            mobile_number = input('Please inform your mobile number: ')
            if re.search('[^0-9]', mobile_number):
                print('\nOnly numbers are accepted\n'.upper())
            else:
                if len(str(mobile_number)) != 11:
                    print('\nThe mobile number must have 11 digits.\n'.upper())
                else:
                    try_again = False
        return mobile_number

    @classmethod
    def new_account_message(cls, account_number):
        """
        Displays the new account number to the client
        """
        time.sleep(1)
        print('\nSorry to keep you waiting, we are sorting out everything for you...\n')
        time.sleep(1.5)
        print('All set!\n\n')
        time.sleep(0.7)
        print(Database.get_user_introduction(account_number) + ' your account was created successfully!\n')
        print('ACCOUNT NUMBER: ' + str(account_number))
        time.sleep(0.7)
        Menus.display_initial_menu()

    @classmethod
    def open_new_account(cls):
        """
        Gathers all user's information and inputs it into the SQL database
        """
        print('\nThat is great news, welcome!\n')
        my_cursor.execute(
            "INSERT INTO client_info(forename, surname, title, mobile_number, password, income) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                NewAccount.get_first_name(),
                NewAccount.get_last_name(),
                NewAccount.get_title(),
                NewAccount.get_mobile_number(),
                NewAccount.get_new_password(),
                NewAccount.income_validation()
            )
        )
        my_cursor.execute("SELECT income FROM client_info WHERE client_id = %s", (str(my_cursor.lastrowid),))
        income = my_cursor.fetchone()[0]
        my_cursor.execute(
            "INSERT INTO account(client_id, balance, overdraft_limit, available_overdraft) VALUES (%s, %s, %s, %s)",
            (
                my_cursor.lastrowid,
                NewAccount.get_new_balance(),
                NewAccount.overdraft_suggestion(income),
                0
            )
        )
        account_number = my_cursor.lastrowid
        available_overdraft = Database.get_overdraft_limit(account_number)
        Database.update_available_overdraft(available_overdraft, account_number)
        NewAccount.new_account_message(account_number)
        db.commit()

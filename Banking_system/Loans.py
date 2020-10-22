import Bank
import math
import Validations
import Database
import Menus
import time


class Loans:

    @classmethod
    def loan_conditional_factor(cls, account_number, income):
        """
        Calculates the maximum loan amount that the account can have according to the reported income
        """
        conditional_factor = 15
        get_loan_amount = Bank.set_format(int(math.ceil((income / conditional_factor) / 100)) * 100)
        leverage_limiter = int(float(get_loan_amount)) * 1.5
        return cls.ask_loan_amount(account_number, get_loan_amount, leverage_limiter)

    @classmethod
    def ask_loan_amount(cls, account_number, get_loan_amount, leverage_limiter):
        """
        Asks the loan amount the client needs
        """
        ask_loan_amount = Validations.validation_integer('\nHow much would you like to borrow? £ ')
        return cls.get_loans_months_quantity(account_number, get_loan_amount, leverage_limiter, ask_loan_amount)

    @classmethod
    def get_loans_months_quantity(cls, account_number, get_loan_amount, leverage_limiter, ask_loan_amount):
        """
        Asks how many months the customer would like to pay the loan
        """
        months_quantity = Validations.validation_integer('How many months are ideal for you? (1 - 60) ')
        return cls.get_loan_info(account_number, get_loan_amount, leverage_limiter, ask_loan_amount, months_quantity)

    @classmethod
    def get_loan_info(cls, account_number, get_loan_amount, leverage_limiter, ask_loan_amount, loans_months_quantity):
        """
        Calculates the value of each installment of the loan, adding the interest rate
        """
        monthly_payment = Bank.set_format(((ask_loan_amount * 1.02) / loans_months_quantity))
        get_loan_amount = int(float(get_loan_amount)) * 1.02
        available_monthly_payment = Bank.set_format(get_loan_amount / loans_months_quantity)
        return cls.loan_verification(account_number, get_loan_amount, leverage_limiter, ask_loan_amount,
                                     loans_months_quantity, monthly_payment, available_monthly_payment)

    @classmethod
    def loan_verification(cls, account_number, get_loan_amount, leverage_limiter, ask_loan_amount,
                          loans_months_quantity, monthly_payment, available_monthly_payment):
        """
        Checks the loan conditions to inform whether it is approved or not
        """
        get_loans = int(Database.get_loan_amount(account_number))
        if 1 <= loans_months_quantity <= 60:
            if ask_loan_amount <= get_loan_amount:
                if (get_loans + ask_loan_amount) <= leverage_limiter:
                    Loans.loan_holding_verification()
                    print('Your loan request was APPROVED! your monthly payment will be: £', monthly_payment)
                    loan_confirmation = Bank.get_confirmed_transaction()
                    if loan_confirmation == 'y':
                        cls.get_loan_confirmation(account_number, ask_loan_amount, monthly_payment,
                                                  loans_months_quantity)
                    else:
                        Menus.display_loan_menu(account_number)
                else:
                    print('\n\nYou already have a loan, the amount available for a new one is: £\n\n',
                          (Bank.set_format((leverage_limiter - get_loans))))
            else:
                if get_loan_amount < (leverage_limiter - get_loans):
                    cls.loan_suggestion(account_number, get_loan_amount,
                                        loans_months_quantity, available_monthly_payment)
                else:
                    Loans.loan_holding_verification()
                    print('\n\nUnfortunately we are unable to offer you a loan at the moment.\n\n')
        else:
            print('Please enter a an option between 1 and 60.')
        Menus.display_loan_menu(account_number)

    @staticmethod
    def loan_holding_verification():
        """
        Creates a realistic sensation of verification
        """
        return  time.sleep(0.4), print('\nWait a moment please...'), \
        time.sleep(1), print('\n\nChecking...\n\n'), time.sleep(1)

    @classmethod
    def loan_suggestion(cls, account_number, get_loan_amount, loans_months_quantity, available_monthly_payment):
        """
        offers another loan's option, lower than requested whether the client is leveraged
        """
        Loans.loan_holding_verification()
        print('Unfortunately we are unable to offer you the exactly amount you request\n\n')
        print('But we are glad to offer you another loan option in the amount of: £', Bank.set_format(get_loan_amount))
        print('And the monthly payment would be of: £\n', available_monthly_payment)
        available_loan_confirmation = Bank.get_confirmed_transaction()
        if available_loan_confirmation == 'y':
            cls.get_loan_confirmation(account_number, get_loan_amount, available_monthly_payment, loans_months_quantity)
        else:
            Menus.display_loan_menu(account_number)

    @classmethod
    def get_loan_confirmation(cls, account_number, ask_loan_amount, monthly_payment, loans_months_quantity):
        """
        Validates the password, inserts the new loan into database and uses the Deposit function to update the balance
        """
        if Bank.authenticate_user_password(account_number):
            time.sleep(1)
            Database.insert_new_loan(ask_loan_amount, monthly_payment, loans_months_quantity, account_number)
            Bank.deposit(account_number, ask_loan_amount)
        Menus.display_main_menu_options(account_number)

    @classmethod
    def display_loan_statement(cls, account_number):
        """
        Displays the loan statement to the client
        """
        Menus.n_string()
        cls.display_loans(account_number)
        Menus.string_n()
        print('AMOUNT BORROWED ......... £', Bank.set_format(float(Database.get_loan_amount(account_number))))
        print('LOAN INSTALLMENTS ....... £', Bank.set_format(float(Database.get_loan_monthly_payment(account_number))))
        Menus.string_n()
        Menus.display_loan_menu(account_number)

    @classmethod
    def loan_amount_to_be_paid(cls):
        """
        Gets the loan amount from the client to be paid
        """
        return Validations.validation_integer('\nHow much would you like to pay? £ ')

    @classmethod
    def loan_payment_check(cls, account_number):
        """
        Checks with the database the feasibility of payment and denies according to criteria such as:
        non-existent loan, amount informed above the loan or insufficient funds for payment. Allowing
        to execute the payment otherwise.
        """
        balance = Database.get_balance(account_number)
        available_overdraft = Database.get_available_overdraft(account_number)
        get_loans = int(Database.get_loan_amount(account_number))
        loans_quantity = (int(Database.get_how_many_loans(account_number)) - 1)
        print('\n\nYour current amount borrowed is: £', Bank.set_format(get_loans))
        if get_loans == 0:
            print('\nYou have no loans to pay.\n'.upper())
        else:
            if loans_quantity == 0:
                loan_id = Database.get_single_loan_id(account_number)
                cls.choose_loan_payment_amount(account_number, loan_id, balance, available_overdraft, get_loans)
            else:
                cls.get_chosen_loan(account_number, balance, available_overdraft)
        return Menus.display_loan_menu(account_number)

    @classmethod
    def choose_loan_payment_amount(cls, account_number, loan_id, balance, available_overdraft, loan_amount):
        """"""
        want_to_pay = cls.loan_amount_to_be_paid()
        if loan_amount < want_to_pay:
            print('\nThe amount chosen is over your debts, please inform a valid amount.\n')
            Menus.display_loan_menu(account_number)
        else:
            if balance >= 0:
                if want_to_pay > (balance + available_overdraft):
                    print('\nYou do not have enough funds to complete this transaction.\n')
                    Menus.display_loan_menu(account_number)
                else:
                    cls.get_loan_payment_done(account_number, loan_id, loan_amount, want_to_pay)
            else:
                if want_to_pay > available_overdraft:
                    print('\nYou do not have enough funds to complete this transaction.\n')
                    Menus.display_loan_menu(account_number)
                else:
                    cls.get_loan_payment_done(account_number, loan_id, loan_amount, want_to_pay)

    @classmethod
    def get_chosen_loan(cls, account_number, balance, available_overdraft):
        """"""
        print('\nAs you have more than one loan, please inform the Loan Number you want to pay.\n')
        cls.display_loans(account_number)
        should_try_again = True
        loan_id = ''
        loan_amount = ''
        while should_try_again:
            loan_id = cls.get_loan_id()
            loan_amount = Database.get_specific_loan(account_number, loan_id)
            print('\nThe chosen Loan is: ', loan_id)
            get_confirmation = Bank.get_confirmed_transaction()
            if get_confirmation == 'y' or get_confirmation == 'yes':
                should_try_again = False
        return cls.choose_loan_payment_amount(account_number, loan_id, balance, available_overdraft, loan_amount)

    @classmethod
    def get_loan_id(cls):
        """"""
        return Validations.validation_integer('\nPlease inform the the Loan Number: '.upper())

    @classmethod
    def display_loans(cls, account_number):
        """"""
        counter = (int(Database.get_how_many_loans(account_number)) - 1)
        loan_detailed = Database.get_each_loan_from_client(account_number)
        is_all_loans = False
        print('LOAN NUMBER'.ljust(20), 'MONTHLY PAYMENT'.ljust(20), 'LOAN AMOUNT'.ljust(20))
        while not is_all_loans:
            if loan_detailed == [] and counter == -1:
                counter = 0
                print('0'.ljust(20), '0.00'.ljust(20), '0.00'.ljust(10))
                is_all_loans = True
            else:
                get_split = (loan_detailed[counter])
                if (counter + 1) > 0:
                    print((str(get_split[0])).ljust(20), (Bank.set_format(get_split[1])).ljust(20),
                          (Bank.set_format(get_split[2])).ljust(10))
                    counter -= 1
                else:
                    is_all_loans = True

    @classmethod
    def get_loan_payment_done(cls, account_number, loan_id, get_loans, how_much_to_pay):
        """
        executes the total or partial payment of the loan according to the amount requested by the client
        """
        Menus.string()
        print('<<< DISCLAIMER >>> \n "The amortization of the total value of the loan does not necessarily \n'
              'imply a reduction in the value of the installments, but rather in the \n'
              'number of months remaining for the total settlement of the loan."\n')
        Menus.string()
        updated_loan_amount = get_loans - how_much_to_pay
        if Bank.authenticate_user_password(account_number):
            Bank.withdraw(account_number, how_much_to_pay)
            if Database.get_single_loan_monthly_payment(account_number, loan_id) > updated_loan_amount:
                Database.update_loan_monthly_payment(account_number, loan_id, updated_loan_amount)
                Database.update_loan_amount(updated_loan_amount, loan_id)
            else:
                Database.update_loan_amount(updated_loan_amount, loan_id)
        return cls.check_to_delete_loan(account_number, loan_id)

    @classmethod
    def check_to_delete_loan(cls, account_number, loan_id):
        """"""
        if int(Database.get_specific_loan(account_number, loan_id)) == 0:
            Database.delete_loan(account_number, loan_id)
        return Menus.display_loan_menu(account_number)

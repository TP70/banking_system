import Bank
import Menus
import Validations
import pymysql
import mysql.connector


class Database:

    db = mysql.connector.connect()

    db = mysql.connector.connect(host="localhost", user="root", passwd="", database="banking_db")
    my_cursor = db.cursor()

    @classmethod
    def get_income(cls, account_number):
        """
        Selects the income according to the account given
        """
        my_cursor.execute(
            "SELECT client_info.income FROM client_info, account WHERE account.client_id = "
            "client_info.client_id AND account.account_id = %s", (str(account_number),))
        return my_cursor.fetchone()[0]

    @classmethod
    def get_available_overdraft(cls, account_number):
        """
        Selects the client's available overdraft according to the account number given
        """
        my_cursor.execute("SELECT available_overdraft FROM account WHERE account_id = %s", (str(account_number),))
        return my_cursor.fetchone()[0]

    @classmethod
    def insert_new_loan(cls, loan_amount, monthly_payment, loans_months_quantity, account_number):
        """
        Inserts the new loan in the database
        """
        my_cursor.execute(
            "INSERT INTO loans(loan_amount, loan_monthly_payment, loans_months_quantity, account_id) "
            "VALUES (%s, %s, %s, %s)", (loan_amount, monthly_payment, loans_months_quantity, account_number))
        db.commit()

    @classmethod
    def update_loan_amount(cls, new_loan_amount, loan_id):
        """
        Updates the client's loan amount
        """
        my_cursor.execute("UPDATE loans SET loan_amount = %s WHERE loan_id = %s",
                          (str(new_loan_amount), str(loan_id),))
        db.commit()

    @classmethod
    def get_loan_monthly_payment(cls, account_number):
        """
        Returns the client's loan monthly payment if they have one, more or zero otherwise
        """
        my_cursor.execute("SELECT SUM(loan_monthly_payment) FROM loans WHERE account_id = %s", (str(account_number),))
        monthly_payment = my_cursor.fetchone()[0]
        if monthly_payment is None:
            monthly_payment = 0
        return monthly_payment

    @classmethod
    def _get_password(cls, account_number):
        """
        Selects the specific password in the database, according to the account number informed
        """
        my_cursor.execute(
            "SELECT password FROM client_info WHERE client_id = "
            "(SELECT client_id FROM account WHERE account_id = %s)", (str(account_number),))
        return my_cursor.fetchone()[0]

    @classmethod
    def get_user_introduction(cls, account_number):
        """
        Displays the client's title and the surname
        """
        my_cursor.execute(
            "SELECT title, surname FROM client_info WHERE client_id = "
            "(SELECT client_id FROM account WHERE account_id = %s)", (str(account_number),))
        get_client_info = my_cursor.fetchone()
        return ((get_client_info[0]) + ' ' + (get_client_info[1])).upper()

    @classmethod
    def client_full_introduction(cls, account_number):
        """
        Displays the client's title, forename and surname
        """
        my_cursor.execute(
            "SELECT title, forename, surname FROM client_info WHERE client_id = "
            "(SELECT client_id FROM account WHERE account_id = %s)", (str(account_number),))
        get_client_info = my_cursor.fetchone()
        return get_client_info[0].upper() + ' ' + get_client_info[1].upper() + ' ' + get_client_info[2].upper()

    @classmethod
    def get_balance(cls, account_number):
        """
        Returns the client's balance
        """
        my_cursor.execute("SELECT balance FROM account WHERE account_id = %s", (str(account_number),))
        return my_cursor.fetchone()[0]

    @classmethod
    def transactions_between_accounts(cls, account_id, receiving_account, transactions_log, amount, transfer_comments):
        """"""
        my_cursor.execute("INSERT INTO transactions"
                          "(account_id, receiving_account, transactions_log, amount, transfer_comments) "
                          "VALUES (%s, %s, %s, %s, %s)", (str(account_id), str(receiving_account), str(transactions_log)
                                                          , str(amount), str(transfer_comments)))
        db.commit()

    @classmethod
    def delete_account(cls, account_number):
        """
        Deletes the account from the database
        """
        my_cursor.execute(
            "DELETE FROM client_info WHERE client_id = (SELECT client_id FROM account WHERE account_id = %s)",
            (str(account_number),))
        db.commit()

    @classmethod
    def anonymous_deposit(cls, account_number, amount):
        """
        inserts the new deposit into the database
        """
        my_cursor.execute(
            "INSERT INTO deposit_for_others(account_id, amount) VALUES (%s, %s)", (str(account_number), str(amount)))
        db.commit()

    @classmethod
    def get_account_id(cls, message):
        """
        verifies whether the account given belongs to the database returning its number if positive
        """
        should_try_again = True
        ask_account = ''
        while should_try_again:
            ask_account = Validations.validation_integer(message)
            my_cursor.execute("SELECT account_id FROM account WHERE account_id = %s", (str(ask_account),))
            get_account = my_cursor.fetchone()
            if get_account is not None:
                ask_account = get_account[0]
                should_try_again = False
            else:
                print('\nThe selected account does not match with our records, please verify.\n')
                ask_to_try_again = Bank.ask_to_try_again()
                if ask_to_try_again == 'n' or ask_to_try_again == 'no':
                    Menus.display_initial_menu()
                    should_try_again = False
        return ask_account

    @classmethod
    def update_account_balance(cls, new_balance, account_number):
        """
        Updates the client's balance
        """
        my_cursor.execute("UPDATE account SET balance = %s WHERE account_id = %s",
                          (str(new_balance), str(account_number),))
        db.commit()

    @classmethod
    def update_available_overdraft(cls, new_available_overdraft, account_number):
        """
        Updates the client's available overdraft
        """
        my_cursor.execute("UPDATE account SET available_overdraft = %s WHERE account_id = %s",
                          (str(new_available_overdraft), str(account_number),))
        db.commit()

    @classmethod
    def get_overdraft_limit(cls, account_number):
        """
        Selects the client's overdraft limit according to the account number given
        """
        my_cursor.execute("SELECT overdraft_limit FROM account WHERE account_id = %s", (str(account_number),))
        return my_cursor.fetchone()[0]

    @classmethod
    def get_loan_amount(cls, account_number):
        """
        Returns the client's loan amount if they have one, more or zero otherwise
        """
        my_cursor.execute("SELECT SUM(loan_amount) FROM loans WHERE account_id = %s", (str(account_number),))
        loan_amount = my_cursor.fetchone()[0]
        if loan_amount is None:
            loan_amount = 0
        return loan_amount

    @classmethod
    def get_how_many_loans(cls, account_number):
        """"""
        my_cursor.execute("SELECT COUNT(*) loan_id FROM loans WHERE account_id = %s", (str(account_number),))
        return my_cursor.fetchone()[0]

    @classmethod
    def get_each_loan_from_client(cls, account_number):
        """"""
        my_cursor.execute("SELECT loan_id, loan_monthly_payment, loan_amount FROM loans "
                          "WHERE account_id = %s ORDER BY loan_id ", (str(account_number),))
        return my_cursor.fetchall()

    @classmethod
    def get_single_loan_id(cls, account_number):
        """"""
        my_cursor.execute("SELECT loan_id FROM loans WHERE account_id = %s", (str(account_number),))
        return my_cursor.fetchone()[0]

    @classmethod
    def get_specific_loan(cls, account_number, loan_id):
        """"""
        my_cursor.execute("SELECT loan_amount FROM loans WHERE loan_id = %s AND account_id = %s",
                          (str(loan_id), str(account_number),))
        get_loan = my_cursor.fetchone()
        should_try_again = True
        loan_amount = ''
        while should_try_again:
            if get_loan is not None:
                loan_amount = get_loan[0]
                should_try_again = False
            else:
                print('\nThe selected Loan Number does not match with our records, please verify.\n')
                Menus.display_loan_menu(account_number)
                should_try_again = False
        return loan_amount

    @classmethod
    def delete_loan(cls, account_number, loan_id):
        """"""
        my_cursor.execute(
            "DELETE FROM loans WHERE loan_id = %s AND account_id = %s", (str(loan_id), str(account_number),))
        db.commit()

    @classmethod
    def get_single_loan_monthly_payment(cls, account_number, loan_id):
        """"""
        my_cursor.execute("SELECT loan_monthly_payment FROM loans WHERE loan_id = %s AND account_id = %s",
                          (str(loan_id), str(account_number),))
        return my_cursor.fetchone()[0]

    @classmethod
    def update_loan_monthly_payment(cls, account_number, loan_id, updated_loan_amount):
        """"""
        my_cursor.execute("UPDATE loans SET loan_monthly_payment = %s WHERE loan_id = %s AND account_id = %s",
                          (str(updated_loan_amount), str(loan_id), str(account_number),))
        db.commit()

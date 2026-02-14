from datetime import datetime
import pandas
import random
import smtplib

my_email = "your@email.com"
password = "yourpassword"

today = datetime.now()
today_tuple = (today.month, today.day)

pandas_data = pandas.read_csv("birthdays.csv")

birthdays_dict = {(row.month, row.day): row for (index, row) in pandas_data.iterrows()}


def write_error(message):
    """Will write  message to error file"""
    with open("./log/error.txt", 'a') as error_file:
        error_file.write(f"{message}\n")


# Try except block for both letter and smtp connection
# If the letter template is missing it will write to the error log and exit
# If there is an authentication error when trying to connect to SMTP
# Will write to the error log
if today_tuple in birthdays_dict:
    birthday_person_name = birthdays_dict[today_tuple]["name"]
    birthday_person_email = birthdays_dict[today_tuple]["email"]
    try:
        with open(f"./letter_templates/letter_{random.randint(1, 3)}.txt", 'r') as letter:
            letter = letter.read()
            letter = letter.replace("[NAME]", birthday_person_name)
    except FileNotFoundError:
        write_error("Letter template not found.\n")
        exit()

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=birthday_person_email,
                msg=f"Subject: Happy Birthday\n\n {letter}"
            )
    except smtplib.SMTPAuthenticationError:
        write_error("Authentication Error Check Username and Password\n")

import json
import os
import smtplib
from email.message import EmailMessage
from getpass import getpass
from colorama import Fore, Back, Style

import click

home = os.path.expanduser('~')
credfile = os.path.join(home, '.credentials', 'emailme.json')


@click.group()
def cli():
    pass


@cli.command()
@click.option('--subject', help='The subject of the email.')
@click.option('--message', help='The email message to send.')
def send(subject, message):
    # If credential file doesn't exist, create it and prompt for username and
    # app password.
    if not credentials_exist():
        create_credentials()
    else:
        usr, pw, host, port = read_credentials()
        smtp = login(usr, pw, host, port)
        message = make_email(usr, subject, message)
        smtp.send_message(message)


def make_email(username, subject, message):
    """
    Creates the email message to be sent.
    """
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['To'] = username
    msg['From'] = username
    return msg


def login(username, password, host, port):
    s = smtplib.SMTP(host, port)
    s.starttls()
    s.login(username, password)
    return s


def read_credentials():
    with open(credfile, 'r+') as f:
        credentials = json.load(f)
    user = credentials['username']
    pw = credentials['password']
    host = credentials['host']
    port = credentials['port']
    return user, pw, host, port


@cli.command()
def create_credentials():
    credentials = dict()
    print(Fore.YELLOW + "Credential file not found. Let's create one.")
    credentials['email'] = input(Fore.GREEN + 'What is your email address?\n')
    username, host = parse_host(credentials['email'])
    print(Fore.RESET + "Awesome. Now, make sure you have an app-specific password.")
    print(Fore.RESET + "This provides an extra layer of security for your account.")
    credentials['password'] = getpass(Fore.GREEN + 'What is your app-specific password?')
    print(Fore.CYAN + 'Creating credentials file...')
    with open(credfile, 'w+') as f:
        json.dump(credentials, f)
    print(Fore.RESET + "You're good to go!")


def check_host(host):
    """
    Returns SMTP host name and port
    """
    if 'gmail' in host:
        return 'smtp.gmail.com', 587
    elif 'yahoo' in host:
        return 'smtp.mail.yahoo.com', 465
    elif 'hotmail' in host or 'outlook' in host:
        return 'smtp.live.com', 25


def parse_host(email):
    username, host = email.split('@')
    return username, host


def credentials_exist():
    """
    Returns a boolean of whether the 'emailme.json' credentials file exists.
    """
    if os.path.exists(credfile) and os.path.isfile(credfile):
        return True
    else:
        return False


if __name__ == '__main__':
    cli()

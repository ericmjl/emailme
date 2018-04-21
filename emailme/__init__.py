import json
import os
import smtplib
from email.message import EmailMessage
from getpass import getpass
from colorama import Fore

import click
import subprocess


__version__ = 0.1.2

home = os.path.expanduser('~')
credfile = os.path.join(home, '.credentials', 'emailme.json')

@click.group()
def sendmail():
    pass

@sendmail.command()
@click.option('--subject', help="The email subject.")
@click.option('--message', help="The message to be sent.")
def send(subject, message):
    # If credential file doesn't exist, create it and prompt for username and
    # app password.
    if not credentials_exist():
        create_credentials()
    else:
        usr, pw, hostname, host, port = read_credentials()
        smtp = login(usr, pw, hostname, port)
        msg = make_email(usr, host, subject, message)
        smtp.send_message(msg)


def make_email(username, host, subject, message):
    """
    Creates the email message to be sent.
    """
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['To'] = f'{username}@{host}'
    msg['From'] = f'{username}@{host}'
    return msg


def login(username, password, host, port):
    print(username, host, password, port)
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
    hostname = credentials['hostname']
    port = credentials['port']
    return user, pw, hostname, host, port


@click.group()
def init():
    pass


@init.command()
def start():
    credentials = dict()
    print(Fore.YELLOW + "Credential file not found. Let's create one.")
    credentials['email'] = input(Fore.GREEN + 'What is your email address?\n')
    username, host = parse_host(credentials['email'])
    credentials['username'] = username
    credentials['host'] = host
    hostname, port = check_host(host)
    credentials['hostname'] = hostname
    credentials['port'] = port
    print(Fore.RESET + "Awesome. Now, make sure you have an app-specific password.")  # noqa: E501
    print(Fore.RESET + "This provides an extra layer of security for your account.")  # noqa: E501
    credentials['password'] = getpass(Fore.GREEN + 'What is your app-specific password?')  # noqa: E501
    print(Fore.CYAN + 'Creating credentials file...')
    with open(credfile, 'w+') as f:
        json.dump(credentials, f)
    subprocess.call(['chmod', '600', credfile])
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



cli = click.CommandCollection(sources=[sendmail, init])


if __name__ == '__main__':
    cli()

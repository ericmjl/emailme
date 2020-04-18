import json
import os
from pathlib import Path
import smtplib
from email.message import EmailMessage
from getpass import getpass
from colorama import Fore
from dotenv import load_dotenv

import click
import subprocess


__version__ = '0.2.0'

load_dotenv()

creddir = Path.home() / ".credentials"
credfile = creddir / "emailme.json"

# @click.group()
# def sendmail():
#     pass

# @sendmail.command()
# @click.option('--subject', help="The email subject.")
# @click.option('--message', help="The message to be sent.")
# @click.option('--to_email', help="Email address of person you're sending email to.")
def send(subject, message, to_email=None, from_email=None):
    """Send email!"""
    usr, pw, hostname, host, port = read_credentials()
    smtp = login(usr, pw, hostname, port)
    msg = make_email(usr, host, subject, message, to_email, from_email)
    smtp.send_message(msg)


def make_email(username, host, subject, message, to_email=None, from_email=None):
    """
    Creates the email message to be sent.

    :param username: Email prefix (before @)
    :param host: Email suffix (after @)
    :param subject: Email subject.
    :param message: Email message.
    :param to_email: (optional) who to send email to.
    :param from_email: (optional) the "from" field in the email.
    """
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    # Set "to" field
    msg['To'] = to_email if to_email else f'{username}@{host}'
    # Set "from" field.
    msg['From'] = from_email if from_email else f'{username}@{host}'
    return msg


def login(username, password, host, port):
    s = smtplib.SMTP(host, port)
    s.starttls()
    s.login(username, password)
    return s


def read_credentials():
    """
    Read credentials.

    The order of priority for credentials is as follows:

    1. Read environment for EMAILME_CONFIG string.
    EMAILME_CONFIG should be of the form username:::password:::hostname:::host:::port.
    Triple colons are used as a precaution,
    in case there are colons inside the password.
    1. Read in the credentials file from ~/.credentials/emailme.json
    1. Raise an exception.
    """
    creds = read_environment()
    if creds is not None:
        return creds

    creds = read_config()
    if creds is not None:
        return creds

    raise Exception("Credential config not found! Please run init or set environment variables.")


def read_environment():
    """Load credentials from environment configuration."""
    email_config = os.getenv("EMAILME_CONFIG", None)
    if email_config is None:
        return None
    user, pw, hostname, host, port = email_config.split(":::")
    return user, pw, hostname, host, port


def read_config():
    """Load credentials from config file."""
    with open(credfile, 'r+') as f:
        credentials = json.load(f)
    user = credentials['username']
    pw = credentials['password']
    host = credentials['host']
    hostname = credentials['hostname']
    port = credentials['port']
    return user, pw, hostname, host, port

# @click.group()
def init():
    pass


# @init.command()
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
    # Make credentials directory.
    if not os.path.exists(creddir):
        os.makedirs(creddir)
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
    Returns whether credentials exist or not.
    """
    if os.path.exists(credfile) and os.path.isfile(credfile):
        return True
    else:
        return False



# cli = click.CommandCollection(sources=[sendmail, init])


# if __name__ == '__main__':
#     cli()

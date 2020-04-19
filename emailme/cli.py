"""
Command-line interface.
"""

import click
import subprocess
from colorama import Fore


from .functions import send as sendfunc

@click.group()
def sendmail():
    pass

@sendmail.command()
@click.option('--subject', help="The email subject.")
@click.option('--message', help="The message to be sent.")
@click.option('--to_email', help="Email address of person you're sending email to.")
def send(subject, message, to_email=None, from_email=None):
    """Send email!"""
    sendfunc(subject, message, to_email, from_email)

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
    # Make credentials directory.
    if not os.path.exists(creddir):
        os.makedirs(creddir)
    with open(credfile, 'w+') as f:
        json.dump(credentials, f)
    subprocess.call(['chmod', '600', credfile])
    print(Fore.RESET + "You're good to go!")


cli = click.CommandCollection(sources=[sendmail, init])


if __name__ == '__main__':
    cli()

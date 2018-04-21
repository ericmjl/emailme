# emailme

A Python module to email myself from Python scripts and the command line.

# installation

```bash
$ pip install emailme
```

# intended usage

`emailme` is intended to be used to quick-fire send an email to oneself from Python scripts and from the command line.

## initial setup

Sending email requires you to login to an SMTP server. This often means a password is required.

To get started, you will need to store your username and password in a file that is read-write only by you. `emailme` provides a convenience way to get setup.

```bash
$ emailme start
```

You will be asked for your email address and passwrod there.

**note about password:** I strongly suggest NOT storing your regular email password. Instead, you should be using an app-specific password that you rotate regularly. Gmail offers such a functionality, and is highly recommended. Check with your email host provider for more detail.

Upon entering your credentials, a file will be written to disk at `~/.credentials/emailme.json`. This email is only read/write-able by you; other users of the computer are unable to read or write it.

Upon this initial setup, you will now be able to use `emailme` to send emails to yourself.


## command line usage

Usage at the command line is super simple.

```bash
$ emailme sendmail --subject "hey" --message "what's up?"
```

(be sure to escape your exclamation marks!)

## script usage

You can also import emailme and use it from a Python script.

```python
from emailme import sendmail

sendmail(subject='hey', message="What's up? How are you doing?")
```

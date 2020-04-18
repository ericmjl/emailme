import streamlit as st
from emailme import send
from dotenv import load_dotenv
import os

load_dotenv()

"""
# Send Email to Eric J. Ma

Hey, thanks for stopping by.

I get a ton of email in my inbox,
so I created this form to help me triage.

It was inspired by the awesome [Shortwhale](https://shortwhale.com).
That said, Shortwhale sometimes goes down,
so I created this app.
"""

subject = st.selectbox(
    "What is this about?",
    [
        "Tutorial: Network Analysis Made Simple",
        "Tutorial: Demystifying Deep Learning for Data Scientists",
        "Tutorial: Bayesian Data Science",
        "Package: pyjanitor",
        "Package: nxviz",
        "Package: jax-unirep",
        "Consulting",
        "Other",
    ]
)

urgency_sh = {
    "Next month is fine": "NEXT MONTH",
    "Next week is ok": "NEXT WEEK",
    "Next day please": "NEXT DAY",
}
urgency = st.selectbox(
    "How urgent is this?",
    list(urgency_sh.keys()),
)


reply_sh = {
    "Yes please": "RN",
    "No, this is just to let you know": "NRN"
}
reply_requested = st.radio(
    "Do you need a reply?",
    sorted(reply_sh.keys())
)

subject_text = st.text_input("Subject", value="Please be as specific as possible.")

subject = f"{subject} {subject_text} [{urgency_sh[urgency]}/{reply_sh[reply_requested]}]"

message_text = st.text_area("Message")
f"""You have used {len(message_text)}/500 characters."""

if len(message_text) > 500:
    st.error("You have exceeded the maximum message length, 500 characters. Please shorten your message.")

message = ""
message += message_text
message += "\n\n"

your_name = st.text_input("Your name")

from_email = st.text_input("Your email")

add_website = st.checkbox("Add website")
if add_website:
    your_website = st.text_input("Your website")
    message += f"```\nSender website: {your_website}\n```\n\n"

add_bio = st.checkbox("Add bio")
if add_bio:
    your_bio = st.text_area("Your bio")
    message += f"```\nSender Bio: {your_bio}\n```\n\n"


reviewed = st.checkbox("I have followed Eric's requests and I believe my email is valuable to him.")
if reviewed:
    """Here's a preview of the message you'll be sending."""

    f"""
## Email Header

From: {your_name}, {from_email}

Subject: {subject}

## Message

{message}
"""

if len(message_text) <= 500:
    if st.button("Send email"):
        send(subject, message, to_email=os.getenv("EMAILME_TO_EMAIL"), from_email=from_email)
        st.success("Your message has been sent! Feel free to close this window.")
        st.balloons()

else:
    st.error("You have exceeded the maximum message length, 500 characters. Please shorten your message.")

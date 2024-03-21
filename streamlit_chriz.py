import streamlit as st
import snowflake.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Snowflake Verbindungsinformationen
snowflake_user = 'your_snowflake_user'
snowflake_password = 'your_snowflake_password'
snowflake_account = 'your_snowflake_account'
snowflake_database = 'your_snowflake_database'
snowflake_schema = 'your_snowflake_schema'
snowflake_warehouse = 'your_snowflake_warehouse'

# SMTP Einstellungen für die E-Mail
smtp_server = 'your_smtp_server'
smtp_port = 587
smtp_username = 'your_smtp_username'
smtp_password = 'your_smtp_password'
sender_email = 'your_sender_email'
recipient_email = 'snowflake@in-factory.com'

# Snowflake Verbindung herstellen
conn = snowflake.connector.connect(
    user=snowflake_user,
    password=snowflake_password,
    account=snowflake_account,
    database=snowflake_database,
    schema=snowflake_schema,
    warehouse=snowflake_warehouse
)

def submit():
    # Hier kannst du den Insert-Befehl für deine Snowflake-Tabelle definieren
    # Zum Beispiel: cursor.execute("INSERT INTO events (name, email) VALUES (%s, %s)", (name, email))

    # E-Mail senden
    subject = "Anmeldung für Event"
    body = f"Name: {name}\nEmail: {email}"
    send_email(subject, body)
    
    st.success("Anmeldung erfolgreich!")

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)

# Streamlit App definieren
st.title("Event Anmeldung")

# Widgets erstellen
name = st.text_input("Name:")
email = st.text_input("Email:")

if st.button("Anmelden"):
    submit()

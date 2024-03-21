import streamlit as st

# Funktion zur Anmeldung für ein Event
def submit_event(event, username, password):
    # Hier könntest du den Code für die Anmeldung zu einem bestimmten Event einfügen
    st.success(f"Erfolgreich für {event} angemeldet mit Benutzername {username} und Passwort {password}")

# Seite mit Streamlit erstellen
def main():
    st.title("Event Anmeldung")

    # Auswahlliste für Events
    event = st.selectbox("Wähle ein Event aus:", ["Event 1", "Event 2"])

    # Felder für Benutzername und Passwort
    username = st.text_input("Benutzername:")
    password = st.text_input("Passwort:", type="password")

    # Button zur Anmeldung
    if st.button("Anmelden"):
        if username and password:
            submit_event(event, username, password)
        else:
            st.warning("Bitte gib Benutzername und Passwort ein")

    # Schöne Grafik hinzufügen
    st.image("beautiful_image.jpg", caption="Schöne Grafik")

if __name__ == "__main__":
    main()

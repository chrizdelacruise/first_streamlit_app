import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach and Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free Ranged Egg')
streamlit.text('🥑🍞 Avocado Toast')
  
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
def get_fruityvice_data (this_fruit_coice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit")
    else:
      back_from_func=get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_func)
      
except URLError as e:
    streamlit.error("Error: " + str(e))


# Streamlit-Überschrift
streamlit.header("The fruit load list contains:")

# Funktion zur Abfrage der Datenbank
def get_fruit_load_list(connection):
    with connection.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall()

# Verbindung zur Snowflake-Datenbank herstellen
try:
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
except Exception as e:
    streamlit.error("Error connecting to Snowflake: " + str(e))
else:
    # Button, um die Daten aus der Datenbank abzurufen
    if streamlit.button('Get fruit load list'):
        my_data_rows = get_fruit_load_list(my_cnx)

        # Streamlit-Überschrift für die angezeigten Daten
        streamlit.header("The List contains:")

        # Daten in einem DataFrame anzeigen
        if my_data_rows:
            streamlit.dataframe(my_data_rows)
        else:
            streamlit.warning("No data found in the fruit load list.")

# Verbindung zur Datenbank schließen
if 'my_cnx' in locals():
    my_cnx.close()



def insert_row_snowflake (new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit +"')")
    return  "Thanks for adding " + new_fruit

add_my_fruit  = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_func = insert_row_snowflake(add_my_fruit)
streamlit.text(back_from_func)



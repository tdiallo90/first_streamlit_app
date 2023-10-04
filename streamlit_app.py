import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parent New Healthy Diner!')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#Let's read the CSV
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruit_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Apple'])
fruit_to_show = my_fruit_list.loc[fruit_selected]
#Let's display the table on the page
streamlit.dataframe(fruit_to_show)

streamlit.header('Fruitvice Advice')
def get_fruitvice_data(this_fruit_choice):
  fruitvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information')
  else:
    back_from_function = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLERROR as e:
  streamlit.error()


streamlit.stop()
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("Hello from Snowflake")
streamlit.header("The fruit load list contains")
streamlit.dataframe(my_data_row)

add_my_fruit = streamlit.text_input("What fruit would you like to add ?")
streamlit.write("You have written ", add_my_fruit)
my_cur.execute("INSERT INTO fruit_load_list values ('from streamlit')")



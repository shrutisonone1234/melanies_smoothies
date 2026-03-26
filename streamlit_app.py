# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Title
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# Get session
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit data
my_dataframe = session.table("smoothies.public.fruit_options") \
                      .select(col("FRUIT_NAME"))

# Multiselect with LIMIT 
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5   #THIS IS THE NEW LINE
)

# Submit button
submit_button = st.button("Submit Order")

# Convert list → string
ingredients_string = ''

if ingredients_list:
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write("Your smoothie will have:")
    st.write(ingredients_string)

# SQL insert
my_insert_stmt = "insert into smoothies.public.orders(ingredients, name_on_order) values ('" + ingredients_string + "','" + name_on_order + "')"

# Debug (optional)
st.write(my_insert_stmt)

# Insert into Snowflake
if submit_button:
    if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
    else:
        st.warning("Please select at least one ingredient.")

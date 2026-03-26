import streamlit as st
import requests
import pandas as pd

# Title
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit data
query = "SELECT FRUIT_NAME FROM smoothies.public.fruit_options"
rows = session.sql(query).collect()

fruit_list = [row["FRUIT_NAME"] for row in rows]

# Multiselect
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Submit button
submit_button = st.button("Submit Order")

# Convert list → string
ingredients_string = ''

# ✅ MAIN LOGIC (UPDATED)
if ingredients_list:
    st.write("Your smoothie will have:")

    for fruit in ingredients_list:
        ingredients_string += fruit + ' '

        # 🔥 API CALL FOR EACH FRUIT
        st.subheader(f"{fruit} Nutrition Info")

        response = requests.get(
            f"https://my.smoothiefroot.com/api/fruit/{fruit}"
        )

        # Convert JSON → DataFrame
        data = response.json()
        df = pd.json_normalize(data)

        # Show Data
        st.dataframe(df, use_container_width=True)

# Insert query
my_insert_stmt = (
    "insert into smoothies.public.orders(ingredients, name_on_order) "
    f"values ('{ingredients_string}','{name_on_order}')"
)

# Debug (optional)
st.write(my_insert_stmt)

# Insert into Snowflake
if submit_button:
    if ingredients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
    else:
        st.warning("Please select at least one ingredient.")

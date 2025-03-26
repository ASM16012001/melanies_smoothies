# Import required packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Streamlit UI
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your smoothie!")

# Get user input for smoothie name
name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

# Ensure Snowflake session is active
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options from Snowflake table
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Convert Snowflake DataFrame to a list for Streamlit multiselect
fruit_options = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

# User selects ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:', fruit_options, max_selections=5)

# Proceed only if ingredients are selected
if ingredients_list and name_on_order:
    # Convert list to a comma-separated string
    ingredients_string = ', '.join(ingredients_list)

    # Corrected SQL insert statement
    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Display SQL query for debugging
    st.write(my_insert_stmt)

    # Button to submit order
    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


# New section to display smoothiefroot nutriton infirmation
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

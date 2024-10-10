from pickle import TRUE
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as db

st.set_page_config(page_title="Redbus Data", layout='wide')

# Function to establish a database connection
def get_db_connection():
    return db.connect(
        host="localhost",
        user="root",
        password="iamveryhappy123@",
        database="redbus_data"
    )

# Function to fetch data from the database
def get_data_from_db(query, params=None):
    con = get_db_connection()
    with con.cursor() as curr:
        curr.execute(query, params)
        data = curr.fetchall()
        column_names = [desc[0] for desc in curr.description]
    con.close()
    return pd.DataFrame(data, columns=column_names)

# Sidebar menu
with st.sidebar:
    st.write("# RedBus Details")
    menu = option_menu(
        menu_title="Select Any",
        options=[ "Bus Selection","States"],
        styles={
            "nav-link-selected": {"background-color": "#D84E55"}
        }
    )

# States Section
if menu == 'States':
    st.header("States")
    st.image('C:\\Users\\GS0864\\Downloads\\image redbus.jpg', use_column_width=True)
    query = "SELECT DISTINCT States FROM redbus_data.bus_routes"
    df = get_data_from_db(query)
    if not df.empty:
        for state in df['States']:
            st.write(state)
    else:
        st.write("No states available.")

# Bus Selection Section
elif menu == 'Bus Selection':
    st.header("Bus Routes")

    c1, c2, c3 = st.columns(3)

    with c1:
        route_query = "SELECT DISTINCT Routes_Name FROM redbus_data.bus_routes"
        route_df = get_data_from_db(route_query)
        select_routes = st.selectbox("Select the Route", route_df['Routes_Name'])

    with c2:
        # Bus Types
        select_type = st.selectbox("Select the Type", ['Sleeper', 'Seater', 'All'])

    with c3:
        # Bus fare
        select_fare = st.selectbox("Select the Fare", ['0-500', '500-1000', '1000+'])

    c4, c5 = st.columns(2)

    with c4:
        # Bus rating
        select_rating = st.selectbox("Rating", ['0-3', '3-4', '4-5', 'All'])

    with c5:
        # Bus AC Types
        ac_type = st.radio("A/C Type", ['A/C', 'NON A/C', 'All'])

    sql_query = "SELECT * FROM redbus_data.bus_routes WHERE Routes_Name = %s"
    params = (select_routes,)

    # Bus Types
    if select_type != 'All':
        if select_type == 'Sleeper':
            sql_query += " AND Bus_Type LIKE '%Sleeper%'"
        elif select_type == 'Seater':
            sql_query += " AND (Bus_Type LIKE '%Seater%' OR Bus_Type LIKE '%PUSH BACK%')"

    # Bus fare
    if select_fare == '0-500':
        sql_query += " AND Price BETWEEN 0 AND 500"
    elif select_fare == '500-1000':
        sql_query += " AND Price BETWEEN 500 AND 1000"
    elif select_fare == '1000+':
        sql_query += " AND Price > 1000"

    # Bus rating
    if select_rating != 'All':
        if select_rating == '0-3':
            sql_query += " AND Star_Rating BETWEEN 0 AND 3"
        elif select_rating == '3-4':
            sql_query += " AND Star_Rating BETWEEN 3 AND 4"
        elif select_rating == '4-5':
            sql_query += " AND Star_Rating BETWEEN 4 AND 5"

    # Bus AC Types
    if ac_type != 'All':
        if ac_type == 'A/C':
            sql_query += " AND (Bus_Type LIKE '%A/C%' OR Bus_Type LIKE '%A.C%') AND Bus_Type NOT LIKE '%Non%' AND Bus_Type NOT LIKE '%NON%'"
        elif ac_type == 'NON A/C':
            sql_query += " AND (Bus_Type LIKE '%Non A/C%' OR Bus_Type LIKE '%NON A/C%' OR Bus_Type LIKE '%NON-AC%' OR Bus_Type LIKE '%Non AC%')"

    try:
        # Execute the final query and get the data
        filtered_data = get_data_from_db(sql_query, params)

        if filtered_data.empty:
            st.write("No results found for the selected filters.")
        else:
            st.write(filtered_data[['Routes_Name', 'Bus_Name', 'Bus_Type', 'Price', 'Star_Rating', 'Seat_Availability', 'Duration']])
    except Exception as e:
        st.error(f"An error occurred while fetching data: {e}")

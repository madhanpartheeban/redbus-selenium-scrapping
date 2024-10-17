import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as db

# Set page configuration
st.set_page_config(page_title="Redbus Data", layout='wide')

# Function to establish a database connection
def get_db_connection():
    return db.connect(
        host="localhost",
        user="root",
        password="fill",
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
        options=["States", "Bus Selection"],
        styles={
            "nav-link-selected": {"background-color": "#ff9999"}
        }
    )

# States Section
if menu == 'States':
    st.header("States")
    query = "SELECT DISTINCT States FROM redbus_data.bus_routes"
    df = get_data_from_db(query)
    if not df.empty:
        st.write("## Available States")
        st.dataframe(df)  # Display in a scrollable table
    else:
        st.write("No states available.")

# Bus Selection Section
elif menu == 'Bus Selection':
    st.header("Bus Routes Filter")

    # Filter Section
    st.subheader("Select Filters")

    # First row: State and Route
    c1, c2, c3 = st.columns(3)
    
    with c1:
        state_query = "SELECT DISTINCT States FROM redbus_data.bus_routes"
        state_df = get_data_from_db(state_query)
        select_state = st.selectbox("Select State", state_df['States'])
    
    with c2:
        if select_state:
            route_query = "SELECT DISTINCT Routes_Name FROM redbus_data.bus_routes WHERE States = %s"
            route_df = get_data_from_db(route_query, (select_state,))
            select_routes = st.selectbox("Select Route", route_df['Routes_Name'])
        else:
            st.warning("Please select a state to view routes.")

    # Bus Type Selection
    with c3:
        select_type = st.multiselect("Select Bus Type", ['Sleeper', 'Seater', 'All'], default='All')

    # Second row: Fare and Rating
    c4, c5 = st.columns(2)
    with c4:
        select_fare = st.slider("Select Fare Range", min_value=0, max_value=2000, value=(0, 1000), step=100)
    
    with c5:
        select_rating = st.slider("Select Rating Range", min_value=0.0, max_value=5.0, value=(3.0, 5.0), step=0.1)

    # Third row: A/C Type
    ac_type = st.radio("A/C Type", ['A/C', 'NON A/C', 'All'], index=2)

    # Search Button
    if st.button("Search Buses"):
        # Ensure both state and route are selected before executing the query
        if select_state and select_routes:
            sql_query = "SELECT * FROM redbus_data.bus_routes WHERE States = %s AND Routes_Name = %s"
            params = (select_state, select_routes)

            # Bus Types
            if 'All' not in select_type:
                type_filter = " OR ".join([f"Bus_Type LIKE '%{t}%'" for t in select_type])
                sql_query += f" AND ({type_filter})"

            # Bus fare
            sql_query += f" AND Price BETWEEN {select_fare[0]} AND {select_fare[1]}"

            # Bus rating
            sql_query += f" AND Star_Rating BETWEEN {select_rating[0]} AND {select_rating[1]}"

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
                    # Remove the 'Routes_Name' column from the results
                    if 'Routes_Name' in filtered_data.columns:
                        filtered_data = filtered_data.drop(columns=['Routes_Name'])

                    # Display results in a tabular format
                    st.subheader("Available Buses")
                    st.dataframe(filtered_data)  # Display in a scrollable table
            except Exception as e:
                st.error(f"An error occurred while fetching data: {e}")
        else:
            st.warning("Please select both a state and a route.")

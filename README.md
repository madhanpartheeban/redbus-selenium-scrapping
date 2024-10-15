# redbus-selenium-scrapping
By using the above program, you can collect data on 15,000+ buses across India. The collected data can be automatically cleaned and collated into a single data frame and saved into a SQL database. This data can be accessed using a multi-purpose Streamlit application, where you can filter the bus data based on your requirements.

How to Use the Application: Step 1: Create a folder and save project 1 REDBUS.ipynb in that folder.

Step 2: Open the project 1 REDBUS.ipynb in a Python console. Provide values for the variables state_path and state with the respective link to the state buses website in Redbus and the name of the state. Run the entire program.

Step 3: You can repeat this process for all required states. The output will be the entire bus data of all the routes within that state, saved in CSV format separately for each state.

Note: You can run three or four states in parallel, depending on your system specifications, by duplicating the same file. This can save up to 75% of the time.

Step 4: After finishing the data collection for all the required states, open the Data_Collation.ipynb notebook to clean, consolidate, and save the data into a SQL database.

Step 5: To use the file, just enter the CSV file name in the file list and run the program.

Step 6: Using mysql, create engine to push to SQL, forming the database.

Step 7: Using mysql_connector, fetch the data from the SQL database.

Step 8: Using this data from the database, Streamlit will read and deploy the data by setting the page configuration.

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import json
import random
import streamlit_shadcn_ui as ui
from streamlit_shadcn_ui import textarea
import summariser
import transcriptor


# Function to highlight maximum values in a DataFrame
def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: #C91A46' if v else '' for v in is_max]


# Set the layout of the page to wide
st.set_page_config(layout="wide")

# Title of the application
st.write("##")
st.title("Quizify")
st.write('')

# Container for the navigation menu
with st.container():
    # Display the navigation menu using the option_menu widget
    selected = option_menu(
        menu_title=None,
        options=['Home', 'progress', 'Summaries', 'Quizzes', 'Contact'],
        icons=['house', 'progress', 'book', 'code-slash', 'chat-left-text-fill'],
        orientation='horizontal'
    )

link = ''
pressed = False

# Home page
if selected == 'Home':
    with st.container():
        st.title("Home Page")
        st.write("Paste your link here ")
        link = textarea(default_value=" ", placeholder="Enter longer text", key="textarea1")

        # add a button that will take the user to the sumaaries page
        if st.button("Get Summary"):
            with st.spinner("Brewing your Summary and Quiz!"):
                summariser.get_summary(transcriptor.get_transcript(link))
                pressed = True
            st.write("please go to the summary and quiz page to view the generated summary and quiz respectively.")

# Progress tracker page
if selected == 'progress':
    with st.container():
        st.header("📈 Progress Tracker")
        st.markdown("*")

        # Sample data for progress tracker
        data = [
            {"Username": "INV001", "Youtube link": "xxxx", "Correct": 5, "incorrect": 10, "Total": 15},
            {"Username": "INV002", "Youtube link": "xxxx", "Correct": 7, "incorrect": 8, "Total": 20},
            {"Username": "INV003", "Youtube link": "xxxx", "Correct": 3, "incorrect": 12, "Total": 15},
            {"Username": "INV004", "Youtube link": "xxxx", "Correct": 5, "incorrect": 10, "Total": 10},
            {"Username": "INV005", "Youtube link": "xxxx", "Correct": 13, "incorrect": 2, "Total": 15},
        ]

        # Create a DataFrame from the data
        df = pd.DataFrame(data)

        # Apply the highlight_max function to style the DataFrame
        styled_df = df.style.apply(highlight_max, subset=["Correct", "incorrect", "Total"])

        # Display the styled DataFrame and a line chart
        st.dataframe(styled_df, width=800)
        st.line_chart(df[['Correct', 'incorrect', 'Total']])

# Summaries page
if selected == "Summaries":
    with st.container():
        # Function to read and display the text file
        # def view_text_file(file):
        #    text = file.read()  # Read the uploaded file
        #    return text

        # Display the summary text
        st.markdown("# Summary of the video:")

        # a = summariser.get_summary(transcriptor.get_transcript(link))
        # st.write(a)

        # Read the content of the summary.txt file
        with open("sum.txt", "r") as f:
            summary_text = f.read()
        st.write(summary_text)
        with open("sum.txt", "w") as f:
            f.write("")
        st.write("")

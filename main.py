import json
import random

import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_shadcn_ui import textarea

import jsonification
import prompt
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
        options=['Home',  'Summary', 'Quizzes','progress', 'Chatbot'],
        icons=['house',  'book', 'code-slash', 'check','robot'],
        orientation='horizontal'
    )

link = ''
pressed = False

# Home page
if selected == 'Home':
    with st.container():
        st.title("Home Page")
        # add a text box for the user to input the youtube link
        link = st.text_input("Enter the youtube link here", placeholder="Paste the link here")

        # add a button that will take the user to the summaries page
        if st.button("Get Summary"):
            with st.spinner("Brewing your Summary and Quiz!"):
                t = transcriptor.get_transcript(link)
                summariser.get_summary(t)
                with open("quiz.json", "w") as f:
                    f.write("")
                jsonification.lists_of_lists_to_json(prompt.get_quiz(t), 'quiz.json')
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
        #add a barchart to show the progress of the user
        st.bar_chart(df[["Correct", "incorrect", "Total"]])

# Summaries page
if selected == "Summary":
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

# Quizzes page
if selected == "Quizzes":
    with st.container():
        st.title("Quiz Time!")
        with open('quiz.json', 'r') as file:
            questions = json.load(file)

        # Initialize score
        score = 0
        correct_answers = 0

        # Initialize quiz_answers if not already set
        if 'quiz_answers' not in st.session_state:
            st.session_state.quiz_answers = {i: None for i in range(len(questions))}

        # Initialize shuffled_options if not already set
        if 'shuffled_options' not in st.session_state:
            st.session_state.shuffled_options = {}
            for i, question in enumerate(questions):
                options = [question['answer'], question['wrong_answer1'], question['wrong_answer2']]
                random.shuffle(options)
                st.session_state.shuffled_options[i] = options

        # Display each question and get user input
        for i, question in enumerate(questions, 1):
            st.subheader(f"Question {i}: {question['question']}")

            # Get previously selected answer (if any)
            selected_option = st.session_state.quiz_answers.get(i - 1, None)

            # Use the stored shuffled options
            options = st.session_state.shuffled_options[i - 1]

            # Check if selected_option is in the options list before trying to find its index
            if selected_option is not None and selected_option in options:
                selected_index = options.index(selected_option)
            else:
                # Set a default index or handle the situation differently
                selected_index = 0  # or any other default index

            # Always render the radio button widget and set the state unconditionally
            selected_option = st.radio("Choose an option", options, key=f"question_{i}", index=selected_index)
            # Update answers dictionary
            st.session_state.quiz_answers[i - 1] = selected_option

        for i, question in enumerate(questions, 1):
            if st.session_state.quiz_answers.get(i - 1) == question['answer']:
                correct_answers += 1

        # Display the score
        score = correct_answers
        st.write(f"Your final score is: {score}/{len(questions)}")



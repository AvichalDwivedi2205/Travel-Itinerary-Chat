import streamlit as st
from streamlit_chat import message as st_message
import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY"))

def generate_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("\U0001F30D Personalized Travel Itinerary Generator")

    # Initializing the state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_step" not in st.session_state:
        st.session_state.current_step = -1
    if "user_responses" not in st.session_state:
        st.session_state.user_responses = {}

    # Basic trip details before the chat interface starts
    with st.expander("\U0001F4DD Enter Basic Trip Details"):
        destination = st.text_input("Destination")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=date.today())
        with col2:
            end_date = st.date_input("End Date", min_value=start_date, value=start_date)
        duration = (end_date - start_date).days + 1
        no_of_people = st.number_input("Number of People", min_value=1, max_value=20, value=1)
        budget = st.selectbox("Budget Level", [
            "Low Budget", "Low To Moderate",
            "Moderate", "Moderate To High", "Luxury"
        ])

    # List of questions that is needed to be asked
    questions = [
        "What's the primary purpose of your trip? (relaxation and personal time, family retreat, couple's retreat, adventure, etc.)",
        "What activities interest you? (sightseeing, trekking, cultural experiences, etc.)",
        "Any dietary preferences we should consider?",
        "Preferred accommodation type? (hotel, hostel, air-bnb, resort, etc.)",
        "Do you want any specific thing in your accomodation? (swimming pool, gym, spa, etc.)",
        "Preferred accommodation location? (city center, quiet area, next to nature, specific landmark, etc.)"
    ]

    # Starting the conversation button
    if st.button("\u2728 Start Interactive Planning") and destination:
        st.session_state.current_step = 0
        st.session_state.user_responses = {
            "Destination": destination,
            "Dates": f"{start_date.strftime('%b %d')} to {end_date.strftime('%b %d')}",
            "Duration": f"{duration} days",
            "Budget": budget,
            "Number of People": no_of_people
        }
        st.session_state.messages = [{
            "role": "assistant", 
            "content": f"Hello! Let's plan your {duration}-day trip to {destination}!\n{questions[0]}"
        }]

    # Display chat history with unique keys (Error Fix)
    for i, msg in enumerate(st.session_state.messages):
        st_message(**{
            "key": str(i),  # Unique key for each message to avoid any errors
            "message": msg["content"],
            "is_user": msg["role"] == "user"
        })

    if st.session_state.current_step >= 0 and st.session_state.current_step < len(questions):
        user_input = st.text_input("Your answer:", key=f"input_{st.session_state.current_step}")
        
        if user_input:
            # Storing the user's response for the end prompt
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.user_responses[questions[st.session_state.current_step]] = user_input
            
            # Moving to the next question in the list above
            st.session_state.current_step += 1
            
            if st.session_state.current_step < len(questions):
                # Asing the next question in the list of question above
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": questions[st.session_state.current_step]
                })
            else:
                # Generating the final itinerary for the user
                prompt_lines = [f"{k}: {v}" for k, v in st.session_state.user_responses.items()]
                prompt_lines += [
                    "I want the following things to be included in the itinerary:",
                    "Include for each day:",
                    "- Morning, Afternoon, and Evening activities",
                    "- 2-3 dining options with dietary accommodations",
                    "- Transportation options between locations",
                    "- Cost estimates for each activity mentioned above",
                    "- Local insider tips and hidden gems",
                    "",
                    "Structure this itinerary:",
                    "1. Group nearby attractions to minimize travel time",
                    "2. Balance popular spots with unique local experiences",
                    "3. Include time buffers for meals and transit",
                    "4. Add safety tips and cultural notes",
                    "5. Format with clear daily headings and emojis",
                    "6. Give me answer only in english"
                ]

                prompt = "Create a detailed travel itinerary with:\n" + "\n".join(prompt_lines)
                with st.spinner("Creating your perfect itinerary..."):
                    itinerary = generate_response(prompt)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": itinerary
                })
                st.session_state.current_step = -1  # Reset conversation

            # Rerun to update the UI
            st.rerun()

if __name__ == "__main__":
    main()
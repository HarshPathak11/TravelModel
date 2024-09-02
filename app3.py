from flask import Flask, request, jsonify
import re
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

from langchain_huggingface import HuggingFaceEndpoint

from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
import os
sec_key=os.getenv('TOKEN')
# print(sec_key)

from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import BaseMessage, AIMessage
callbacks = [StreamingStdOutCallbackHandler()]

llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.6,
    repetition_penalty=1.03,
    callbacks=callbacks,
    streaming=True,
    huggingfacehub_api_token=sec_key,
)

# dictionary to store the chat message history with its session ID
store = {}



def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Set up session ID and initial message
session_id =int(input("Session id:"))
history = get_by_session_id(session_id)
history.add_message(AIMessage(content="Hello! I'm your travel guide assistant. Let's start planning your trip."))

# # Define prompt templates for different stages of trip planning
# initial_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a helpful travel planning assistant."),
#     MessagesPlaceholder(variable_name="history"),
#     ("human", "{query}"),
# ])

# places_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are an expert travel guide for suggesting places to visit."),
#     MessagesPlaceholder(variable_name="history"),
#     ("human", "Based on the destination {destination} and interests {interests}, suggest popular places to visit."),
# ])

# eateries_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a local expert in finding the best eateries."),
#     MessagesPlaceholder(variable_name="history"),
#     ("human", "For the selected places {selected_places}, suggest popular eateries nearby."),
# ])

# trip_plan_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are an experienced travel planner."),
#     MessagesPlaceholder(variable_name="history"),
#     ("human", "Create a detailed trip plan for {duration} days in {destination} including visits to {selected_places} and meals at {selected_eateries}."),
# ])


# Initial prompt to gather all required data from the user
initial_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful travel planning assistant.You will help me plan a trip."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "What is your destination, number of people, budget, duration of the trip, and interests?"),
])

# Prompt for suggesting places to visit
places_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert travel guide for suggesting places to visit."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "Based on the destination '{destination}', interests '{interests}', and a budget of '{budget}' for {number_of_people} people, suggest popular places to visit. Provide a brief about the places as well. Do not give too much emphasis on budget. Also give the activities that can be done on those places."),
])





# Prompt for suggesting eateries
# eateries_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a local expert in finding the best eateries."),
#     MessagesPlaceholder(variable_name="history"),
#     ("human", "suggest popular eateries that serve {cuisine}.Ensure the eateries are numbered. Keep the eateries in the vicinity of the selected places '{selected_places}'.Also, ensure that the places fit within the budget type "),
# ])
eateries_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a local expert in finding the best eateries."),
    MessagesPlaceholder(variable_name="history"),
    ("human", """
    Suggest popular eateries that serve {cuisine}. 
    Ensure the eateries are numbered and listed under budget categories: 
    1. Budget
    2. Mid-range
    3. Upscale
    Each eatery should include:
    - Name of the eatery
    - A brief description
    - Address (if available)
    Ensure the eateries are in the vicinity of the selected places '{selected_places}' and fit within the budget type.
    The response format should be:
    
    1. Budget:
    * [Name of Eatery]: [Description] [Address (if available)]
    2. Mid-range:
    * [Name of Eatery]: [Description] [Address (if available)]
    3. Upscale:
    * [Name of Eatery]: [Description] [Address (if available)]
    """)
])

# eateries_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are an expert travel guide for suggesting places to visit"),
#     MessagesPlaceholder(variable_name="history"),
#     ("human", "Suggest popular eateries that serve {cuisine}. Ensure the eateries are numbered and within the vicinity of the selected places '{selected_places}'. Also, ensure that the places fit within the budget type.")
# ])



import re

# Prompt for creating a detailed trip plan
trip_plan_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an experienced travel planner."),
    MessagesPlaceholder(variable_name="history"),
    ("human", """Create a detailed trip plan for {duration} days in the specified destination including visits to the selected places and meals at {selected_eateries}.  - A specific itinerary for each day in the following format:
    
    Day X:

    * Morning: [Activity and/or location]. 
    * Afternoon: [Activity and/or location].
    * Evening: [Activity and/or location].
    * Dinner: [Restaurant and location].
    
    - Ensure that the plan includes popular attractions, activities, and eateries, fitting within the mentioned budget"""),
])

def extract_places(response_text):
        # Split the text based on the numbering (1., 2., 3., etc.)
        place_entries = re.split(r'\d+\.\s+', response_text.strip())
        
        places = []
        for entry in place_entries:
            if entry:  # Check if the entry is not empty
                # Split by the first occurrence of ':' to separate name and description
                parts = entry.split(":", 1)
                if len(parts) == 2:  # Ensure there are both name and description
                    place = {
                        "name": parts[0].strip(),
                        "description": parts[1].strip()
                    }
                    places.append(place)

        return places
def extract_restaurant_recommendations(text):
        recommendations = {}

        # Define the categories in the response
        categories = ['Budget', 'Mid-range', 'Upscale']
        
        # Split the text into blocks by categories
        category_blocks = re.split(r'(\d+\.\s+(?:Budget|Mid-range|Upscale):)', text)
        
        for i in range(1, len(category_blocks), 2):
            # Extract the category name
            category_name = category_blocks[i].strip().replace(":", "").strip()
            recommendations[category_name] = []
            
            # Extract restaurant entries within the category block
            restaurant_entries = re.findall(r'\*\s*(.+?):\s*(.+?)(?=\s*\*|$)', category_blocks[i + 1])
            
            for entry in restaurant_entries:
                # Separate the name, description, and optional address
                name, details = entry[0].strip(), entry[1].strip()
                
                if ' - ' in details:
                    description, address = details.rsplit(' - ', 1)
                else:
                    description, address = details, None
                    
                # Append the restaurant information
                recommendations[category_name].append({
                    "name": name,
                    "description": description.strip(),
                    "address": address.strip() if address else None
                })
        
        return recommendations

def extract_itinerary(itinerary_text):
        itinerary = {}
        
        # Split the text into days using "Day X:" as the delimiter
        day_blocks = re.split(r'Day \d+:\n', itinerary_text.strip())
        
        for day_num, day_block in enumerate(day_blocks[1:], start=1):
            day_dict = {}
            
            # Extract morning, afternoon, evening, and dinner plans
            times = re.findall(r'\* ([\w\s]+): (.+)', day_block)
            
            for time_slot, activity in times:
                day_dict[time_slot.lower()] = activity
            
            itinerary[f"Day {day_num}"] = day_dict
        
        return itinerary



# Create LLM chains with history
initial_chain = initial_prompt | llm | StrOutputParser()
places_chain = places_prompt | llm | StrOutputParser()
eateries_chain = eateries_prompt | llm | StrOutputParser()
trip_plan_chain = trip_plan_prompt | llm | StrOutputParser()

initial_chain_with_history = RunnableWithMessageHistory(
    initial_chain,
    get_by_session_id,
    input_messages_key="query",
    history_messages_key="history",
)
places_chain_with_history = RunnableWithMessageHistory(
    places_chain,
    get_by_session_id,
    input_messages_key="query",
    history_messages_key="history",
)
eateries_chain_with_history = RunnableWithMessageHistory(
    eateries_chain,
    get_by_session_id,
    input_messages_key="query",
    history_messages_key="history",
)
trip_plan_chain_with_history = RunnableWithMessageHistory(
    trip_plan_chain,
    get_by_session_id,
    input_messages_key="query",
    history_messages_key="history",
)

config = {"configurable": {"session_id": session_id}}

# Start of the Trip Planning Process


@app.route('/send-places', methods=['GET'])
def send_data():

    # Get user input for basic trip information
    destination = input("Enter your desired destination: ")
    number_of_people = int(input("Enter the number of people on the trip: "))
    duration = int(input("Enter the duration of the trip (in days): "))
    budget = int(input("Enter your budget (e.g., Type in a number): "))
    interests = input("Enter your interests (e.g., temples, museums, hiking): ")

    # Get places to visit# Get places to visit
    places_response = places_chain_with_history.invoke(
        {
            "destination": destination,
            "interests": interests,
            "budget": budget,
            "number_of_people": number_of_people,
            "query": f"Suggest places to visit based on the provided data."
        },
        config=config
    )
    print("Places to visit:", places_response)
    places_dict = extract_places(places_response)
    return jsonify(places_dict)
    # print(places_prompt.messages[2].content)


@app.route('/send-eateries', methods=['GET'])
def send_data2():
    # Get user input for cuisine
    cuisines = ["Italian", "Mexican", "Indian", "Thai", "French"]
    print("Available cuisines:", cuisines)
    selected_cuisine = input("Select your preferred cuisine from the list: ")

    # Get popular eateries
    selected_places = input("Enter the places you selected from the list above (comma-separated): ")
    eateries_response = eateries_chain_with_history.invoke(
        {
            "selected_places": selected_places,
            "cuisine": selected_cuisine,
            "query": f"Suggest popular eateries near the selected places."
        },
        config=config
    )
    print("Eateries:", eateries_response)
    result = extract_restaurant_recommendations(eateries_response)
    return jsonify(result)

    
@app.route('/send-plan', methods=['GET'])
def send_data3():
     # Generate trip plan
    selected_eateries = input("Enter the eateries you selected from the list above (comma-separated): ")
    duration = int(input("Enter the duration of the trip (in days): "))
    
    trip_plan_response = trip_plan_chain_with_history.invoke(
        {
            "selected_eateries": selected_eateries,
            "duration":duration,
            "query": f"Create a detailed trip plan."
        },
        config=config
    )
    print("Trip plan:", trip_plan_response)
    itinerary_dict = extract_itinerary(trip_plan_response)
    # print(itinerary_dict)
    return jsonify(itinerary_dict)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
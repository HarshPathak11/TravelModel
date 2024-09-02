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
print(sec_key)

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
session_id = "2"
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





# Prompt for creating a detailed trip plan
trip_plan_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an experienced travel planner."),
    MessagesPlaceholder(variable_name="history"),
    ("human", """Create a detailed trip plan for {duration} days in {destination} including visits to {selected_places} and meals at {selected_eateries}.  - A specific itinerary for each day in the following format:
    
    Day X:

    * Morning: [Activity and/or location]. 
    * Afternoon: [Activity and/or location].
    * Evening: [Activity and/or location].
    * Dinner: [Restaurant and location].
    
    - Ensure that the plan includes popular attractions, activities, and eateries, fitting within the mentioned budget"""),
])


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


@app.route('/send-data', methods=['GET'])
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
    # print(places_prompt.messages[2].content)

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

    # Generate trip plan
    selected_eateries = input("Enter the eateries you selected from the list above (comma-separated): ")
    trip_plan_response = trip_plan_chain_with_history.invoke(
        {
            "duration": duration,
            "destination": destination,
            "selected_places": selected_places,
            "selected_eateries": selected_eateries,
            "query": f"Create a detailed trip plan."
        },
        config=config
    )
    print("Trip plan:", trip_plan_response)

    import re

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

    # Example usage with the AI response
    response_text = """
    1. Phoenix United Mall: This is one of the largest malls in Lucknow, offering a wide range of luxury shopping options, restaurants, and a multiplex cinema. It's located in Gomti Nagar, a bustling area with many other attractions.

    2. Sahara Ganj Mall: This high-end mall, located in Hazratganj, offers a mix of luxury shopping, dining, and entertainment options. It's known for its spacious layout and variety of stores.

    3. Ambience Mall: Situated in the posh Vipin Khand area, Ambience Mall offers a premium shopping experience with high-end brands, restaurants, and a multiplex cinema.

    4. The Grand Mall: Located in the heart of the city, The Grand Mall is another high-end shopping destination that offers a mix of luxury brands, restaurants, and a multiplex cinema.

    5. Central Mall: Central Mall, situated in the upscale area of Sushant Golf City, offers a mix of luxury shopping, dining, and entertainment options. It's a relatively new addition to the city's mall scene.
    """

    places_dict = extract_places(places_response)
    # eat_dict=extract_places(selected_cuisine)
    print(places_dict)
    # print(eat_dict)
    # import re

    # def extract_restaurant_recommendations(text):
    #     recommendations = {}
        
    #     # Split the text into categories using numbers followed by periods (e.g., "1. Budget:")
    #     category_blocks = re.split(r'(\d+\.\s+[A-Za-z-]+:)', text)
        
    #     current_category = None
        
    #     for i in range(1, len(category_blocks), 2):
    #         # Get the category name (e.g., "Budget", "Mid-range", "Upscale")
    #         current_category = category_blocks[i].strip().replace(":", "")
    #         recommendations[current_category] = []
            
    #         # Extract individual restaurant entries
    #         restaurant_entries = re.findall(r'\*\s*(.+?):\s*(.+)', category_blocks[i + 1])
            
    #         for name, description in restaurant_entries:
    #             recommendations[current_category].append({
    #                 "name": name.strip(),
    #                 "description": description.strip()
    #             })
        
    #     return recommendations

    import re

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



    # Example usage
    text = """
    1. Budget:

    * Bhojoholi, Bhubaneswar (near Lingaraj Temple): A popular budget restaurant serving authentic Oriya cuisine, South Indian dishes, and Chinese food.   
    * Hotel Mahodadhi, Puri (near Puri Jagannath Temple): A budget hotel with a multi-cuisine restaurant serving North Indian, South Indian, Oriya, and Chinese dishes.

    2. Mid-range:

    * Cafe Coffee Day, Bhubaneswar (near Lingaraj Temple): A popular coffee shop chain offering a variety of Indian and international dishes, including sandwiches, pasta, and burgers.
    * The Art Cafe, Puri (near Puri Jagannath Temple): A mid-range cafe serving a variety of Indian and international dishes, including pizzas, pastas, and salads. They also offer a beautiful view of the sea.

    3. Upscale:

    * Mayfair Lagoon, Puri (near Puri Jagannath Temple): An upscale hotel with a multi-cuisine restaurant serving a variety of Indian, Oriya, and international dishes. They also offer a beautiful view of the Chilika Lake.
    * The Toshali Sands, Puri (near Puri Jagannath Temple): An upscale resort with a multi-cuisine restaurant serving a variety of Indian, Oriya, and international dishes. They also offer a beautiful view of the sea.
    """

    result = extract_restaurant_recommendations(eateries_response)
    print(result)


    import re

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

    # Example usage with the AI response
    itinerary_text = """
    Day 1:

    * Morning: Arrival in Lucknow. Check-in at your hotel and freshen up.
    * Afternoon: Visit Phoenix United Mall for shopping and lunch at The Mughal Sarai (Gomti Nagar).
    * Evening: Explore the local markets and landmarks around Chowk, such as the Chhota Imambara, Bada Imambara, and Rumi Darwaza.
    * Dinner: Head to Tunday Kababi for their famous kababs.

    Day 2:

    * Morning: Visit Sahara Ganj Mall for shopping and lunch at Wah-Gam-Wah (Hazratganj).
    * Afternoon: Take a rickshaw ride around the city to see local attractions like the British Residency, Dilkusha Kothi, and Lucknow Zoo.
    * Evening: Visit Ambience Mall for more shopping and dinner at Royal Cafe (Vipin Khand).

    Day 3:

    * Morning: Head to Fun Republic Mall for shopping and lunch at Idris Biryani (Sushant Golf City).
    * Afternoon: Visit the State Museum of Uttar Pradesh to learn about the region's history and culture.
    * Evening: Take a leisurely stroll along the Gomti River or visit the Indian Institute of Management (IIM) for its beautiful architecture.
    * Dinner: Return to Gomti Nagar for dinner at Awadh Food Plaza.

    Day 4:

    * Morning: Departure from Lucknow.
    """

    itinerary_dict = extract_itinerary(trip_plan_response)
    print(itinerary_dict)
    return jsonify(places_dict)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
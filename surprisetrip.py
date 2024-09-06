from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import re

# Initialize Flask app
app = Flask(__name__)

# Load the .env file
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')

from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage

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
    huggingfacehub_api_token=api_key,
)

store = {}

def getsessionid(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

session_id = "2"
history = getsessionid(session_id)
history.add_message(AIMessage(content="Hello! I'm your travel guide assistant. Let's start planning your trip."))

initial_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert travel guide for suggesting places to visit."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "Based on the traveller type '{traveller_type}', trip duration '{duration}', and a travel mode of '{travel_mode}' for {num_people} people interested in {interests}, suggest popular places to visit in India. Provide the response in the following structured format:"),
    ("human", "1. **Place Name:**\n   - **Brief:** [Brief description]\n   - **Budget:** [Estimated budget]\n   - **Activities:** [List of activities]\n")
])

detailed_plan_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert travel planner providing a detailed itinerary for a selected destination."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "Based on the place '{place_name}', generate a detailed plan including daily activities, recommended places to stay, and dining options. Provide the response in the following structured format:"),
    ("human", "1. **Day 1:**\n   - **Activities:** [List of activities]\n   - **Places to Stay:** [Recommended hotels or accommodations]\n   - **Dining Options:** [Recommended restaurants]\n")
])

initial_chain = initial_prompt | llm | StrOutputParser()
recommendation_chain = detailed_plan_prompt | llm | StrOutputParser()

initial_chain_with_history = RunnableWithMessageHistory(
    initial_chain,
    getsessionid,
    input_messages_key="query",
    history_messages_key="history",
)

recommendation_with_history = RunnableWithMessageHistory(
    recommendation_chain,
    getsessionid,
    history_messages_key="history",
)

config = {"configurable": {"session_id": session_id}}

def extract_travel_info(response_text):
    pattern = re.compile(
        r'\*\*Place Name:\*\*\s*(.*?)\s*\n\s*-\s*\*\*Brief:\*\*\s*(.*?)\s*\n\s*-\s*\*\*Budget:\*\*\s*(.*?)\s*\n\s*-\s*\*\*Activities:\*\*\s*(.*?)\n',
        re.DOTALL
    )
    matches = pattern.findall(response_text)
    places_info = []
    for match in matches:
        place_name, brief, budget, activities = match
        activities_list = [activity.strip() for activity in activities.split(',')]
        places_info.append({
            'Place Name': place_name.strip(),
            'Brief': brief.strip(),
            'Budget': budget.strip(),
            'Activities': activities_list
        })
    return places_info
# EXTRA VARIABLE

extracted_info = []


@app.route('/get-info', methods=['POST','GET'])  # Changed to POST for data submission
def send_places():
    if request.method == 'POST':
        data = request.get_json()  
        traveller_type = data['traveller_type']
        num_people = int(data['num_people'])
        duration = int(data['duration'])
        interests = data['interests']
        travel_mode = data['travel_mode']

        response = initial_chain_with_history.invoke(  # Assuming this exists elsewhere
            {
                "traveller_type": traveller_type,
                "interests": interests,
                "duration": duration,
                "num_people": num_people,
                "travel_mode": travel_mode,
                "query": f"Suggest places to visit based on the provided data."
            },
            config=config
        )
        global extracted_info  # Accessing temporary storage (avoid global vars)
        extracted_info = extract_travel_info(response)
        # temp = extract_travel_info(response)
        return jsonify({'message': 'Places processed successfully.'})  # Success message
        # return jsonify(temp)
    # elif  request.method == 'GET':
        # extracted_info 
        # return jsonify(extracted_info)
    # else:
        # return jsonify({'error': 'Invalid request method. Use POST.'})  # Error message
    # if request.method == 'GET':
@app.route('/send-places', methods=['GET'])

    # Get user choice from frontend (simulate for now)
def send_data():
    # global varaible to store data 
    global extracted_info  # Declare the global variable
    traveller_type = input("which type of traveller are you [Domestic/International]: ")
    num_people = int(input("Enter the number of people on the trip: "))
    duration = int(input("Enter the duration of the trip (in days): "))
    interests = input("Enter your interests (e.g., temples, museums, hiking): ")
    travel_mode = input("Enter your preferred travel mode (Flight/Train/Car/Other): ")
    # history = ""
    response = initial_chain_with_history.invoke(
        {
            "traveller_type": traveller_type,
            "interests": interests,
            "duration": duration,
            "num_people": num_people,
            "travel_mode":travel_mode,
            # "history": history  # Provide an empty history
            "query": f"Suggest places to visit based on the provided data."
        },
        config=config
    )
    # print("Places to visit:", response)
    # extracted_info = extract_travel_info(response)
    extracted_info = extract_travel_info(response)
    temp = extract_travel_info(response)
    # Store the extracted info in the global variable
    for info in extracted_info:
       print(info)
    extracted_info = extract_travel_info(response)

    print("Here are the suggested places to visit:")
    for idx, info in enumerate(extracted_info, start=1):
        print(f"{idx}. {info['Place Name']}: {info['Brief']}, Budget: {info['Budget']}, Activities: {', '.join(info['Activities'])}")
    return extracted_info
    return jsonify(extracted_info)


@app.route('/send-plan', methods=['GET'])
def send_data2():
     # Generate trip plan
    global extracted_info  # Access the global variable
    
    # Generate trip plan
    if not extracted_info:
        return "No places extracted yet. Please first run 'send-places'."
     
    choice = int(input(f"Select a place by entering the number (1-{len(extracted_info)}): "))
    selected_place = extracted_info[choice - 1]['Place Name']
    full_plan = generate_full_trip_plan(selected_place)
    print(f"Here is the detailed plan for {selected_place}:\n{full_plan}")
    result = selected_place
    print(jsonify(result))
   


def generate_full_trip_plan(place_name):
    response = recommendation_with_history.invoke(
        {
            "place_name": place_name,
        },
        config=config
    )
    return response

if __name__ == '__main__':
    app.run(debug=True)

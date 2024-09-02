import express from 'express'
import axios from 'axios';
const app=express()

app.use(express.json())

// const axios = require('axios');

// axios.get('http://localhost:5000/send-places')
//     .then(response => {
//         const data = response.data;
//         console.log(data); // Use the data as needed
//     })
//     .catch(error => {
//         console.error('Error fetching data:', error);
//     });
// axios.get('http://localhost:5000/send-eateries')
//     .then(response => {
//         const data = response.data;
//         console.log(data); // Use the data as needed
//     })
//     .catch(error => {
//         console.error('Error fetching data:', error);
//     });
// axios.get('http://localhost:5000/send-plan')
//     .then(response => {
//         const data = response.data;
//         console.log(data); // Use the data as needed
//     })
//     .catch(error => {
//         console.error('Error fetching data:', error);
//     });

const fetchData = async () => {
    try {
        // First API call
        const placesResponse = await axios.get('http://localhost:5000/send-places');
        const placesData = placesResponse.data;
        console.log(placesData); // Use the data as needed

        // Second API call (only after the first is completed)
        const eateriesResponse = await axios.get('http://localhost:5000/send-eateries');
        const eateriesData = eateriesResponse.data;
        console.log(eateriesData); // Use the data as needed

        // Third API call (only after the second is completed)
        const planResponse = await axios.get('http://localhost:5000/send-plan');
        const planData = planResponse.data;
        console.log(planData); // Use the data as needed
    } catch (error) {
        console.error('Error fetching data:', error);
    }
};

// Call the function to execute the API calls in sequence
fetchData();

app.listen(8000,()=>{
    console.log(`server running on port 8000`)
})
import express from 'express'
import axios from 'axios';
// const bodyParser = require('body-parser');
const app = express();
import cors from 'cors'
app.use(cors())
// Middleware to parse JSON bodies
// app.use(bodyParser.json());
app.use(express.json())
// Route to receive data from Flask

const fetchData = async () => {
    try {
const Response = await axios.get('http://localhost:5000/send-places');
const placesData = Response.data;
console.log(placesData); // Use the data as needed
const topics = extractTopics(placesData);
app.get('/places',(req,res)=>{
   res.json(topics)
})

console.log(topics)
}
    catch(error){(console.log(error))}

// Backend (Node.js)

};


// app.get('/places', (req, res) => {
//     const placesData = [
//         {
//             Activities: [
//                 'Trekking',
//                 'camping',
//                 'wildlife spotting',
//                 'river rafting',
//                 'and visiting temples.'
//             ],
//             Brief: 'The Himalayas offer a variety of stunning landscapes, diverse wildlife, and numerous trekking routes.',
//             Budget: 'INR 10,000-20,000 per person (depending on the trek and accommodation choices)',
//             'Place Name': 'Himalayas (Uttarakhand)',
//             Image: 'https://example.com/himalayas.jpg'
//         },
//         {
//             Activities: [
//                 'Hiking',
//                 'camping',
//                 'visiting forts',
//                 'and enjoying local cuisine.'
//             ],
//             Brief: 'Lonavala and Khandala are hill stations located near Mumbai, known for their scenic beauty, waterfalls, and forts.',
//             Budget: 'INR 5,000-10,000 per person (including accommodation, meals, and local transportation)',
//             'Place Name': 'Lonavala & Khandala (Maharashtra)',
//             Image: 'https://example.com/lonavala.jpg'
//         }
//     ]
//     res.json(placesData);
// });
// Function to extract specific topics from the data
function extractTopics(data) {
    return data.map(place => {
        return {
            placeName: place['Place Name'],
            brief: place.Brief,
            activities: place.Activities
        };
    });
}


// app.post('/receive-data', (req, res) => {
//     const receivedData = req.body;
    
//     // Print the received data to the console
//     console.log('Received data from Flask:', receivedData);
    
//     // Send a response back to Flask
//     res.json({ message: 'Data received successfully', receivedData: receivedData });
// });

// Start the server
fetchData()
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

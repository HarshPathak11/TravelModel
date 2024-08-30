import express from 'express'
import axios from 'axios';
const app=express()

app.use(express.json())

// const axios = require('axios');

axios.get('http://localhost:5000/send-data')
    .then(response => {
        const data = response.data;
        console.log(data); // Use the data as needed
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });

app.listen(8000,()=>{
    console.log(`server running on port 8000`)
})
import React from "react";
import { useState,useEffect } from "react";
import './PlaceCard.css';
import axios from "axios";
const Placecard = ()=>{
    const[places,setPlaces]=useState([])
    // useEffect(()=>{
    //     fetch('http://localhost:3000/places')
    //     .then((response)=>{response.json})
    //     .then((data)=>{setPlaces(data)})
    //     .catch((error)=>{
    //         console.log(error)
    //     })
    // },[])
    useEffect(() => {
        fetch('http://localhost:3000/places')
        .then(response => response.json()) // Make sure to call the .json() method
        .then(data => setPlaces(data))
        .catch(error => {
            console.log(error);
        });
    }, []);
    // useEffect(() => {
    //     axios.get('http://localhost:3000/places')
    //         .then(response => {
    //             console.log(response.data)
    //             setPlaces(response.data); // Use the response data
    //         })
    //         .catch(error => {
    //             console.error('Error fetching the data:', error);
    //         });
    // }, []);
     
    return (
        <div className="cards-container">
          {places.map((place, index) => (
            <div className="card" key={index}>
              {/* <img src={place.Image} alt={place['Place Name']} className="card-img" /> */}
              <div className="card-content">
                <h2>{place.placeName}</h2>
                <p className="brief">{place.brief}</p>
                {/* <p className="budget">Budget: {place.Budget}</p> */}
                <ul className="activities">
                  {place.activities.map((activity, idx) => (
                    <li key={idx}>{activity}</li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      );




};
export default Placecard;
// {
//     "placeName": "Varanasi, Uttar Pradesh",
//     "brief": "Varanasi is one of the oldest cities in the world, famous for its spiritual significance and the Ganges River. It offers a unique cultural experience and numerous temples.",
//     "activities": [
//       "Boat ride on the Ganges",
//       "exploring the old city",
//       "visiting local markets",
//       "and attending evening aarti at the ghats."
//     ]
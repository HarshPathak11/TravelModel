import React, { useState } from 'react';
import axios from 'axios';

const LocationSearch = () => {
    const [query, setQuery] = useState('');
    const [locationData, setLocationData] = useState(null);

    const handleSearch = async () => {
        // const apiKey = process.env.REACT_APP_LOCATIONIQ_API_KEY;
        const url = `https://us1.locationiq.com/v1/search?key=${'pk.732b29695cfe8582f37c73ff55244ebf'}&q=${encodeURIComponent(query)}&format=json`;

        try {
            const response = await axios.get(url);
            setLocationData(response.data);
        } catch (error) {
            console.error('Error fetching location data:', error);
        }
    };


    
    return (
        <div>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter location"
            />
            <button onClick={handleSearch}>Search</button>

            {locationData && (
                <div>
                    <h3>Location Results:</h3>
                    {/* <pre>{JSON.stringify(locationData, null, 2)}</pre> */}
                   <pre>  {JSON.stringify(locationData[1].lat)}</pre>
                   <pre>  {JSON.stringify(locationData[1].lon)}</pre>

                   
                </div>
                // console.log(JSON.stringify(locationData, null, 2))
            )}
   
        </div>
    );
};

export default LocationSearch;

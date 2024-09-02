// src/components/Map.js
import React,{useState,useEffect} from 'react';
import { MapContainer, TileLayer ,Marker,Popup} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios'



const Map = () => {
  const [coordinates,setCoordinates] = useState([])
  // const coordinates = [
  //   { lat: 30.6129332, lon: 77.2294928, display_name: 'Location 1' },
  //   { lat: 28.6139, lon: 77.2090, display_name: 'Location 2' },
  //   // Add more coordinates here
  // ];
  
 
  function handler() {
   const data=  [
      // {
      //   description: 'This is a historical church built in 1921, which houses a museum within its premises. The museum offers a glimpse into the history of the city, including the 1857 Sepoy Mutiny, and displays artifacts from the British era.\n' +
      //     '\n' +
      //     'Activities: Visit the museum, explore the historical church, and learn about the rich history of Kanpur.',
      //   name: 'Kanpur Memorial Church and Kanpur Museum'
      // },
      {
        description: 'This unique museum showcases an extensive collection of glass bottles, glassware, and other items made from glass. It is a must-visit for those interested in glass art and craft.\n' +
          '\n' +
          'Activities: Browse through the vast collection of glass items, learn about the art of glassmaking, and appreciate the intricate designs and patterns.',
        name: 'J.N. Mandal Tankeeya Udyan (J.N. Mandal Glass and Bottle House)'
      },
      {
        description: 'Although not a museum, Moti Jheel is a popular tourist spot in Kanpur. It is a beautiful lake surrounded by lush greenery and offers a peaceful environment for relaxation and picnicking.\n' +
          '\n' +
          'Activities: Enjoy a boat ride, take a leisurely walk around the lake, and spend quality time with family and friends.',
        name: 'Moti Jheel'
      },
      {
        description: 'While not a museum, the Allen Forest Zoo is another popular attraction in Kanpur. It houses a variety of wildlife species, including tigers, lions, elephants, and reptiles.\n' +
          '\n' +
          'Activities: Observe the diverse range of wildlife, learn about different species through infor informative signage, and enjoy the scenic surroundings.</s>',
        name: 'Allen Forest Zoo'
      }
    ]
    // axios.get('http://localhost:5000/send-data')
    // .then(response => {
    //     const data = response.data;
    //     console.log(data); // Use the data as needed
    // })
    // .catch(error => {
    //     console.error('Error fetching data:', error);
    // });
    
    const fetchCoordinates = async () => {
      const urls = data.map((item) => {
        
        return `https://us1.locationiq.com/v1/search?key=${'pk.732b29695cfe8582f37c73ff55244ebf'}&q=${encodeURIComponent(item.name)}&format=json`;
      });
      

      try {
        
        const responses=[]
        for(let i=0;i<urls.length;++i){
          console.log(urls[i])
          const r=await axios.get(urls[i]);
          // console.log(r)
          // const data=await r.json();
          responses.push(r.data)
          setInterval(()=>{},1000);
        }
        console.log(responses, "Ho")
        // const cordi = responses.map(response => {
        //   // if(!response.data[0])
            
        //   const location = response[0];
        //   console.log(location)
          
        // });
        setCoordinates([...responses])
      } catch (error) {
        console.error('Error fetching location data:', error);
      }
    };
    fetchCoordinates()
  };
  return (
   
   <>
  
    <MapContainer 
      center={[20.5937, 78.9629]} 
      zoom={5} 
      style={{ height: '100vh', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />

      {/* <Marker position={[30.6129332,77.22949282049879]}>
      <Popup>
        India Gate <br /> New Delhi.
      </Popup>
    </Marker> */}
    
    {coordinates.map((item) => (
  <Marker position={[item[0].lat, item[0].lon]}>
    <Popup>{item[0].display_name}</Popup>
  </Marker>
))}

    </MapContainer>
    <button onClick={handler}>search</button>
    </>
  );
  
};

export default Map;

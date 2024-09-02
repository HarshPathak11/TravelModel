// src/components/Map.js
import React from 'react';
import { MapContainer, TileLayer ,Marker,Popup} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const Map = () => {
  return (
    <MapContainer 
      center={[20.5937, 78.9629]} 
      zoom={5} 
      style={{ height: '100vh', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      <Marker position={[28.6129332,77.22949282049879]}>
      <Popup>
        India Gate <br /> New Delhi.
      </Popup>
    </Marker>
    </MapContainer>
  );
};

export default Map;

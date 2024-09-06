import React, { useState } from 'react';
import axios from 'axios'; // Assuming axios is installed
function InputForm() {
  const [formData, setFormData] = useState({
    traveller_type: '',
    num_people: '',
    duration: '',
    interests: '',
    travel_mode: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/get-info', formData); 
      console.log(response.data);  // Log response for debugging (optional)
    } catch (error) {
      console.error(error);  // Handle errors appropriately
    } finally {
      
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="traveller_type">Traveller Type:</label>
      <select id="traveller_type" name="traveller_type" value={formData.traveller_type} onChange={handleChange}>
        <option value="">Select</option>
        <option value="Domestic">Domestic</option>
        <option value="International">International</option>
      </select>
      <label htmlFor="num_people">Number of People:</label>
      <input type="number" id="num_people" name="num_people" value={formData.num_people} onChange={handleChange} />
      <label htmlFor="duration">Duration:</label>
      <input type="number" id="duration" name="duration" value={formData.duration} onChange={handleChange} />
      <label htmlFor="interests">Interests:</label>
      <input type="text" id="interests" name="interests" value={formData.interests} onChange={handleChange} />
      <label htmlFor="travel_mode">Travel Mode:</label>
      <input type="text" id="travel_mode" name="travel_mode" value={formData.travel_mode} onChange={handleChange} />
      <button type="submit">Submit</button>
    </form>
  );
}

export default InputForm;
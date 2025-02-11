import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function App() {
  const [data, setData] = useState(null);
  const [selectedCity, setSelectedCity] = useState('oslo');

  useEffect(() => {
    // Load the latest analysis file
    fetch('/data/latest.json')
      .then(response => response.json())
      .then(data => setData(data))
      .catch(error => console.error('Error loading data:', error));
  }, []);

  if (!data) return <div className="p-4">Loading...</div>;

  const cityData = data.analysis[selectedCity];

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Food Delivery Analysis Dashboard</h1>
      
      <select
        value={selectedCity}
        onChange={(e) => setSelectedCity(e.target.value)}
        className="mb-4 p-2 border rounded"
      >
        {Object.keys(data.analysis).map(city => (
          <option key={city} value={city}>
            {city.charAt(0).toUpperCase() + city.slice(1)}
          </option>
        ))}
      </select>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">Vendor Comparison</h2>
          <BarChart width={400} height={300} data={[
            { name: 'Foodora', vendors: cityData.vendor_counts.foodora },
            { name: 'Wolt', vendors: cityData.vendor_counts.wolt }
          ]}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="vendors" fill="#8884d8" />
          </BarChart>
        </div>

        <div className="bg-white p-4 rounded shadow">
          <h2 className="text-xl font-semibold mb-4">Price Distribution</h2>
          <BarChart width={400} height={300} data={[
            { name: '$', foodora: cityData.price_distribution.foodora['$'], wolt: cityData.price_distribution.wolt['$'] },
            { name: '$$', foodora: cityData.price_distribution.foodora['$$'], wolt: cityData.price_distribution.wolt['$$'] },
            { name: '$$$', foodora: cityData.price_distribution.foodora['$$$'], wolt: cityData.price_distribution.wolt['$$$'] }
          ]}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="foodora" fill="#8884d8" />
            <Bar dataKey="wolt" fill="#82ca9d" />
          </BarChart>
        </div>
      </div>
    </div>
  );
}

export default App;
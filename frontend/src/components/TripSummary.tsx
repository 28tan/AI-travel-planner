"use client";

import React from 'react';
import WeatherView from './WeatherView';
import TransportView from './TransportView';
import POIView from './POIView';
import ItineraryView from './ItineraryView';

interface TripSummaryProps {
  summary: any; // Type properly
  onGenerateItinerary: () => void;
  isGenerating: boolean;
}

export default function TripSummary({ summary, onGenerateItinerary, isGenerating }: TripSummaryProps) {
  if (!summary) return null;
  
  console.log("TripSummary summary object:", summary);
  console.log("Return flights:", summary.return_flight_options);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Trip Summary</h2>
        <button
          onClick={onGenerateItinerary}
          disabled={isGenerating}
          className="bg-green-600 text-white px-6 py-2 rounded-md font-medium hover:bg-green-700 disabled:opacity-50"
        >
          {isGenerating ? 'Generating Itinerary...' : 'Generate AI Itinerary'}
        </button>
      </div>

      <WeatherView data={summary.weather_summary} />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TransportView 
            flights={summary.flight_options} 
            returnFlights={summary.return_flight_options}
            drivingOptions={summary.driving_options} 
        />
        <POIView pois={summary.poi_highlights} />
      </div>
      
      <div className="bg-blue-50 p-4 rounded-md border border-blue-100">
        <p className="text-sm text-blue-800">
          <strong>Currency Rate:</strong> {summary.currency_rate}
        </p>
      </div>

      {summary.itinerary && <ItineraryView itinerary={summary.itinerary} weather={summary.weather_summary} />}
    </div>
  );
}

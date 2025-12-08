"use client";

import React, { useState } from 'react';
import Modal from './ui/Modal';

interface TransportViewProps {
  flights: any[];
  returnFlights?: any[];
  drivingOptions?: any;
}

export default function TransportView({ flights, returnFlights, drivingOptions }: TransportViewProps) {
  const [selectedFlight, setSelectedFlight] = useState<any>(null);

  const hasFlights = flights && flights.length > 0;
  const hasReturnFlights = returnFlights && returnFlights.length > 0;
  const hasDriving = drivingOptions && drivingOptions.possible;

  if (!hasFlights && !hasDriving) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-4">Transportation</h3>
        <p className="text-gray-500">No available transportation options found for your preference.</p>
        
        {flights && flights.length === 0 && (
            <p className="text-sm text-red-500 mt-2">No flights found for this route.</p>
        )}

        {drivingOptions && !drivingOptions.possible && (
             <p className="text-sm text-red-500 mt-2">Driving is not possible: {drivingOptions.reason || "No route found"}</p>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Driving Section */}
      {drivingOptions && (
        <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                🚗 Driving Option
            </h3>
            {drivingOptions.possible ? (
                <div className="p-4 border rounded-md bg-blue-50 border-blue-100">
                    <div className="flex justify-between items-center">
                        <div>
                            <p className="font-medium text-gray-900">Drive from {drivingOptions.origin} to {drivingOptions.destination}</p>
                            <p className="text-sm text-gray-600 mt-1">
                                Distance: <span className="font-semibold">{drivingOptions.distance_km} km</span>
                            </p>
                            <a 
                                href={`https://www.google.com/maps/dir/?api=1&origin=${encodeURIComponent(drivingOptions.origin)}&destination=${encodeURIComponent(drivingOptions.destination)}&travelmode=driving`}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-indigo-600 hover:text-indigo-800 text-sm underline mt-2 inline-block"
                            >
                                View Route on Google Maps 🗺️
                            </a>
                        </div>
                        <div className="text-right">
                             <p className="text-lg font-bold text-blue-700">
                                {Math.floor(drivingOptions.duration_min / 60)}h {drivingOptions.duration_min % 60}m
                             </p>
                             <p className="text-xs text-gray-500">Estimated Duration</p>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="p-4 border rounded-md bg-red-50 border-red-100 text-red-700">
                    <p className="font-medium">Driving not available</p>
                    <p className="text-sm">{drivingOptions.reason || "Route could not be calculated."}</p>
                </div>
            )}
        </div>
      )}

      {/* Flight Section */}
      {hasFlights ? (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-4">✈️ Outbound Flights</h3>
        <div className="space-y-4">
          {flights.map((flight: any, index: number) => (
            <div 
              key={index} 
              className="flex justify-between items-center p-4 border rounded-md hover:bg-gray-50 cursor-pointer transition-colors"
              onClick={() => setSelectedFlight(flight)}
            >
              <div>
                <p className="font-medium text-gray-900">{flight.airline?.name || 'Airline'}</p>
                <p className="text-sm text-gray-500">
                  {flight.departure?.iata} → {flight.arrival?.iata}
                </p>
                <p className="text-xs text-gray-400">
                  {new Date(flight.departure?.scheduled).toLocaleTimeString()} - {new Date(flight.arrival?.scheduled).toLocaleTimeString()}
                </p>
              </div>
              <div className="text-right">
                {flight.price ? (
                  <p className="font-bold text-blue-600">{flight.currency} {flight.price}</p>
                ) : (
                  <p className="font-bold text-blue-600">Check Price</p>
                )}
                <p className="text-xs text-gray-500">{flight.flight_status}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
      ) : (
        flights && flights.length === 0 && (
            <div className="bg-white p-6 rounded-lg shadow-md">
                <h3 className="text-lg font-semibold mb-4">✈️ Outbound Flights</h3>
                <p className="text-sm text-red-500">No flights found for this route.</p>
            </div>
        )
      )}

      {/* Return Flight Section */}
      {hasReturnFlights && (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-4">✈️ Return Flights</h3>
        <div className="space-y-4">
          {returnFlights?.map((flight: any, index: number) => (
            <div 
              key={index} 
              className="flex justify-between items-center p-4 border rounded-md hover:bg-gray-50 cursor-pointer transition-colors"
              onClick={() => setSelectedFlight(flight)}
            >
              <div>
                <p className="font-medium text-gray-900">{flight.airline?.name || 'Airline'}</p>
                <p className="text-sm text-gray-500">
                  {flight.departure?.iata} → {flight.arrival?.iata}
                </p>
                <p className="text-xs text-gray-400">
                  {new Date(flight.departure?.scheduled).toLocaleTimeString()} - {new Date(flight.arrival?.scheduled).toLocaleTimeString()}
                </p>
              </div>
              <div className="text-right">
                {flight.price ? (
                  <p className="font-bold text-blue-600">{flight.currency} {flight.price}</p>
                ) : (
                  <p className="font-bold text-blue-600">Check Price</p>
                )}
                <p className="text-xs text-gray-500">{flight.flight_status}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
      )}

      <Modal
        isOpen={!!selectedFlight}
        onClose={() => setSelectedFlight(null)}
        title="Flight Details"
      >
        {selectedFlight && (
          <div className="space-y-6">
            <div className="flex justify-between items-center border-b pb-4">
              <div>
                <p className="text-sm text-gray-500">Airline</p>
                <p className="font-semibold text-lg">{selectedFlight.airline?.name || 'Unknown Airline'}</p>
                <p className="text-xs text-gray-400">Flight: {selectedFlight.flight?.iata || 'N/A'}</p>
              </div>
              <div className="text-right">
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                  selectedFlight.flight_status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {selectedFlight.flight_status || 'Scheduled'}
                </span>
                {selectedFlight.price && (
                   <p className="text-xl font-bold text-gray-900 mt-2">{selectedFlight.currency} {selectedFlight.price}</p>
                )}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-8">
              <div>
                <h4 className="text-sm font-medium text-gray-500 mb-1">Departure</h4>
                <p className="text-2xl font-bold text-gray-900">{selectedFlight.departure?.iata}</p>
                <p className="text-sm text-gray-600">{selectedFlight.departure?.airport}</p>
                <p className="text-sm font-medium mt-1">
                  {new Date(selectedFlight.departure?.scheduled).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                </p>
                <p className="text-xs text-gray-400">
                  {new Date(selectedFlight.departure?.scheduled).toLocaleDateString()}
                </p>
                {selectedFlight.departure?.terminal && (
                  <p className="text-xs text-gray-500 mt-1">Terminal {selectedFlight.departure.terminal}</p>
                )}
              </div>

              <div className="text-right">
                <h4 className="text-sm font-medium text-gray-500 mb-1">Arrival</h4>
                <p className="text-2xl font-bold text-gray-900">{selectedFlight.arrival?.iata}</p>
                <p className="text-sm text-gray-600">{selectedFlight.arrival?.airport}</p>
                <p className="text-sm font-medium mt-1">
                  {new Date(selectedFlight.arrival?.scheduled).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                </p>
                <p className="text-xs text-gray-400">
                  {new Date(selectedFlight.arrival?.scheduled).toLocaleDateString()}
                </p>
                {selectedFlight.arrival?.terminal && (
                  <p className="text-xs text-gray-500 mt-1">Terminal {selectedFlight.arrival.terminal}</p>
                )}
              </div>
            </div>
            
            {selectedFlight.booking_link && (
                <div className="pt-4 border-t">
                    <a 
                        href={selectedFlight.booking_link} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="block w-full text-center bg-indigo-600 text-white py-2 rounded-md hover:bg-indigo-700 transition-colors font-medium"
                    >
                        Book Flight
                    </a>
                </div>
            )}


            <div className="bg-blue-50 p-4 rounded-md border border-blue-100 mt-4">
              <p className="text-sm text-blue-800 text-center">
                This is a live flight status. To book this flight, please visit the airline's website or a booking aggregator.
              </p>
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
}

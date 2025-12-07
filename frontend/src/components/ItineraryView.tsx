import React, { useState } from 'react';
import Modal from './ui/Modal';

interface Activity {
  time: string;
  description: string;
  location: string;
  cost_estimate: string;
  image_url?: string;
  reason?: string;
}

interface Day {
  day_number: number;
  date: string;
  theme: string;
  activities: Activity[];
  rationale?: string;
  weather_note?: string;
}

interface Itinerary {
  trip_title: string;
  summary: string;
  personal_travel_tip?: string;
  days: Day[];
}

interface ItineraryViewProps {
  itinerary: Itinerary;
  weather?: any;
}

const ItineraryView: React.FC<ItineraryViewProps> = ({ itinerary, weather }) => {
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);
  const [expandedWeatherDay, setExpandedWeatherDay] = useState<number | null>(null);

  console.log("ItineraryView received weather:", weather);
  console.log("ItineraryView received itinerary:", itinerary);
  console.log("Itinerary Tip:", itinerary?.personal_travel_tip); // Debug log

  if (itinerary && itinerary.days && itinerary.days.length > 0) {
      console.log("First day activities:", itinerary.days[0].activities);
  }

  if (!itinerary) return null;

  // Helper to find weather for a date
  const getWeatherForDate = (dateStr: string, dayIndex: number) => {
    if (!weather || !weather.daily) return null;
    
    // Try exact match
    const exactMatch = weather.daily.find((d: any) => d.date === dateStr);
    if (exactMatch) return exactMatch;

    // Fallback: If we have weather data but dates don't match (e.g. future trip),
    // map the first day of the trip to the first day of the forecast.
    // This is a heuristic to show *some* weather data.
    if (weather.daily.length > dayIndex) {
        return weather.daily[dayIndex];
    }
    
    return null;
  };

  return (
    <>
      <div className="bg-white shadow-lg rounded-lg overflow-hidden mt-8">
        <div className="bg-indigo-600 px-6 py-4">
          <h2 className="text-2xl font-bold text-white">{itinerary.trip_title}</h2>
          <p className="text-indigo-100 mt-1">{itinerary.summary}</p>
          {itinerary.personal_travel_tip && (
              <div className="mt-4 bg-indigo-700 bg-opacity-50 p-3 rounded-md border border-indigo-400">
                  <p className="text-sm text-white">
                      <span className="font-bold text-yellow-300">💡 Travel Tip: </span> 
                      {itinerary.personal_travel_tip}
                  </p>
              </div>
          )}
        </div>
        
        <div className="p-6">
          <div className="space-y-8">
            {itinerary.days.map((day, index) => {
              const dayWeather = getWeatherForDate(day.date, index);
              return (
              <div key={day.day_number} className="border-b border-gray-200 pb-6 last:border-0 last:pb-0">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center">
                    <div className="bg-indigo-100 text-indigo-800 font-bold rounded-full h-10 w-10 flex items-center justify-center mr-4">
                      {day.day_number}
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold text-gray-900">Day {day.day_number}: {day.theme}</h3>
                      <p className="text-sm text-gray-500">{day.date}</p>
                    </div>
                  </div>
                  {dayWeather && (
                    <div className="flex flex-col items-end">
                        <div 
                            className="flex items-center bg-blue-50 px-3 py-1 rounded-full cursor-pointer hover:bg-blue-100 transition-colors"
                            onClick={() => setExpandedWeatherDay(expandedWeatherDay === day.day_number ? null : day.day_number)}
                            title="Click to see hourly forecast"
                        >
                          <span className="text-2xl mr-2">{dayWeather.icon || '🌤️'}</span>
                          <div className="text-right">
                            <p className="text-sm font-bold text-gray-800">{dayWeather.temp_max}° / {dayWeather.temp_min}°</p>
                            <p className="text-xs text-gray-500 flex items-center justify-end gap-1">
                                {dayWeather.condition} 
                                <span className="text-[10px]">{expandedWeatherDay === day.day_number ? '▲' : '▼'}</span>
                            </p>
                          </div>
                        </div>
                    </div>
                  )}
                </div>

                {/* Hourly Weather Section */}
                {expandedWeatherDay === day.day_number && dayWeather && dayWeather.hourly && (
                    <div className="ml-14 mb-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-100 overflow-x-auto shadow-inner">
                        <h4 className="text-xs font-semibold text-indigo-800 mb-2 uppercase tracking-wider">Hourly Forecast</h4>
                        <div className="flex space-x-6 min-w-max pb-2">
                            {dayWeather.hourly.map((hour: any, hIdx: number) => (
                                <div key={hIdx} className="flex flex-col items-center min-w-[60px] group">
                                    <span className="text-xs text-gray-500 font-medium mb-1">{hour.time}</span>
                                    <span className="text-2xl my-1 transform group-hover:scale-110 transition-transform duration-200">{hour.icon}</span>
                                    <span className="text-sm font-bold text-gray-800">{hour.temp}°</span>
                                    <span className="text-[10px] text-gray-500 truncate w-full text-center mt-1">{hour.condition}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* AI Rationale & Weather Note */}
                {(day.rationale || day.weather_note) && (
                    <div className="ml-14 mb-6 p-4 bg-amber-50 rounded-lg border border-amber-100">
                        {day.weather_note && (
                            <div className="flex items-start mb-2">
                                <span className="text-lg mr-2">🌦️</span>
                                <p className="text-sm text-amber-800 italic"><span className="font-semibold">Weather Note:</span> {day.weather_note}</p>
                            </div>
                        )}
                        {day.rationale && (
                            <div className="flex items-start">
                                <span className="text-lg mr-2">🤖</span>
                                <p className="text-sm text-amber-800"><span className="font-semibold">AI Insight:</span> {day.rationale}</p>
                            </div>
                        )}
                    </div>
                )}
                
                <div className="ml-14 space-y-4">
                  {day.activities.map((activity, idx) => (
                    <div 
                      key={idx} 
                      className="bg-gray-50 p-4 rounded-md border border-gray-100 cursor-pointer hover:bg-gray-100 transition-colors"
                      onClick={() => setSelectedActivity(activity)}
                    >
                      <div className="flex justify-between items-start">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                          {activity.time}
                        </span>
                        <span className="text-xs text-gray-500 font-medium">
                          {activity.cost_estimate}
                        </span>
                      </div>
                      <h4 className="text-lg font-bold text-gray-900 mt-2">{activity.location}</h4>
                      <p className="text-gray-600 text-sm mt-1">{activity.description}</p>
                      {activity.reason && (
                          <p className="text-xs text-indigo-600 mt-2 italic border-l-2 border-indigo-200 pl-2">
                              " {activity.reason} "
                          </p>
                      )}
                      <div className="mt-2">
                         <a 
                            href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(activity.location)}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-indigo-600 hover:text-indigo-800 text-xs underline"
                            onClick={(e) => e.stopPropagation()}
                          >
                            View on Map 📍
                          </a>
                      </div>
                      <div className="flex mt-2 space-x-4">
                        {activity.image_url && (
                          <img 
                            src={activity.image_url} 
                            alt={activity.location} 
                            className="w-24 h-24 object-cover rounded-md flex-shrink-0"
                          />
                        )}
                        <div>
                          <p className="text-gray-800">{activity.description}</p>
                          <div className="mt-2 flex items-center text-sm text-gray-500">
                            <svg className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                            <a 
                              href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(activity.location)}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-600 hover:underline"
                              onClick={(e) => e.stopPropagation()}
                            >
                              {activity.location}
                            </a>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )})}
          </div>
        </div>
      </div>

      <Modal
        isOpen={!!selectedActivity}
        onClose={() => setSelectedActivity(null)}
        title="Activity Details"
      >
        {selectedActivity && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                {selectedActivity.time}
              </span>
              <span className="text-sm font-medium text-gray-500">
                Cost: {selectedActivity.cost_estimate}
              </span>
            </div>
            
            <div>
              <h4 className="text-sm font-medium text-gray-500">Description</h4>
              <p className="text-gray-900 mt-1">{selectedActivity.description}</p>
            </div>

            <div>
              <h4 className="text-sm font-medium text-gray-500">Location</h4>
              <div className="flex items-center mt-1 text-gray-900">
                <svg className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {selectedActivity.location}
              </div>
              <a 
                href={`https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(selectedActivity.location)}`}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-indigo-600 hover:text-indigo-800 mt-1 inline-block"
              >
                View on Google Maps &rarr;
              </a>
            </div>

            <div className="bg-yellow-50 p-4 rounded-md border border-yellow-100">
              <h4 className="text-sm font-medium text-yellow-800 mb-1">Travel Tip</h4>
              <p className="text-sm text-yellow-700">
                Make sure to check opening hours and ticket availability in advance.
              </p>
            </div>
          </div>
        )}
      </Modal>
    </>
  );
};

export default ItineraryView;

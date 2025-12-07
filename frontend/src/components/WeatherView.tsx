"use client";

import React, { useState } from 'react';

interface WeatherViewProps {
  data: any; // Type this properly based on API response
}

export default function WeatherView({ data }: WeatherViewProps) {
  const [selectedDay, setSelectedDay] = useState<any | null>(null);

  if (!data || !data.daily) {
    return <div className="p-4 bg-yellow-50 text-yellow-700 rounded-md">Weather data unavailable</div>;
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-4">Weather Forecast</h3>
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
        {data.daily.map((day: any, index: number) => (
          <div 
            key={index} 
            className={`text-center p-2 border rounded-md cursor-pointer transition-all ${
                selectedDay === day ? 'ring-2 ring-indigo-500 bg-indigo-50' : 'bg-blue-50 hover:bg-blue-100'
            }`}
            onClick={() => setSelectedDay(selectedDay === day ? null : day)}
          >
            <p className="text-sm font-medium text-gray-600">
              {new Date(day.date).toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' })}
            </p>
            <div className="my-2">
               <span className="text-2xl">{day.icon}</span>
            </div>
            <p className="text-lg font-bold text-gray-900">{day.temp_max}° / {day.temp_min}°</p>
            <p className="text-xs text-gray-500 capitalize flex justify-center items-center gap-1">
                {day.condition}
                {day.hourly && <span className="text-[10px] text-indigo-400">▼</span>}
            </p>
          </div>
        ))}
      </div>

      {selectedDay && selectedDay.hourly && (
        <div className="mt-4 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-100 overflow-x-auto shadow-inner animate-fade-in">
            <h4 className="text-xs font-semibold text-indigo-800 mb-2 uppercase tracking-wider">
                Hourly Forecast for {new Date(selectedDay.date).toLocaleDateString(undefined, { weekday: 'long' })}
            </h4>
            <div className="flex space-x-6 min-w-max pb-2">
                {selectedDay.hourly.map((hour: any, hIdx: number) => (
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
    </div>
  );
}

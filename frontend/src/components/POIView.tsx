"use client";

import React, { useState } from 'react';
import Modal from './ui/Modal';

interface POIViewProps {
  pois: any[];
}

export default function POIView({ pois }: POIViewProps) {
  const [selectedPOI, setSelectedPOI] = useState<any>(null);

  const [visibleCount, setVisibleCount] = useState(6);

  if (!pois || pois.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-4">Points of Interest</h3>
        <p className="text-gray-500">No points of interest found.</p>
      </div>
    );
  }

  const handleShowMore = () => {
    setVisibleCount(prev => prev + 6);
  };

  return (
    <>
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold mb-4">Top Attractions</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {pois.slice(0, visibleCount).map((poi: any, index: number) => (
            <div 
              key={index} 
              className="flex items-start space-x-3 p-3 border rounded-md hover:bg-gray-50 cursor-pointer transition-colors"
              onClick={() => setSelectedPOI(poi)}
            >
              {poi.photo_url ? (
                 <img src={poi.photo_url} alt={poi.name} className="w-16 h-16 object-cover rounded-md flex-shrink-0" />
              ) : (
                 <div className="w-16 h-16 bg-gray-200 rounded-md flex-shrink-0 flex items-center justify-center text-gray-400">
                   📷
                 </div>
              )}
              <div>
                <p className="font-medium text-gray-900 line-clamp-1">{poi.name}</p>
                <div className="flex items-center space-x-1">
                  <span className="text-yellow-400">★</span>
                  <span className="text-sm text-gray-600">{poi.rating || 'N/A'}</span>
                  <span className="text-xs text-gray-400">({poi.user_ratings_total || 0})</span>
                </div>
                <p className="text-xs text-gray-500 line-clamp-1">{poi.vicinity}</p>
              </div>
            </div>
          ))}
        </div>
        {visibleCount < pois.length && (
          <div className="mt-4 text-center">
            <button 
              onClick={handleShowMore}
              className="text-blue-600 hover:text-blue-800 font-medium text-sm"
            >
              Show More
            </button>
          </div>
        )}
      </div>

      <Modal
        isOpen={!!selectedPOI}
        onClose={() => setSelectedPOI(null)}
        title={selectedPOI?.name || 'Attraction Details'}
      >
        {selectedPOI && (
          <div className="space-y-4">
            {selectedPOI.photo_url ? (
              <img src={selectedPOI.photo_url} alt={selectedPOI.name} className="w-full h-48 object-cover rounded-md" />
            ) : (
              <div className="h-48 bg-gray-200 rounded-md flex items-center justify-center text-gray-400">
                <span className="text-4xl">📷</span>
              </div>
            )}
            
            <div>
              <h4 className="text-sm font-medium text-gray-500">Address</h4>
              <p className="text-gray-900">{selectedPOI.vicinity || selectedPOI.formatted_address || 'Address not available'}</p>
            </div>

            <div className="flex items-center space-x-4">
              <div>
                <h4 className="text-sm font-medium text-gray-500">Rating</h4>
                <div className="flex items-center">
                  <span className="text-yellow-400 text-lg mr-1">★</span>
                  <span className="text-gray-900 font-bold">{selectedPOI.rating || 'N/A'}</span>
                  <span className="text-gray-500 text-sm ml-1">({selectedPOI.user_ratings_total || 0} reviews)</span>
                </div>
              </div>
              {selectedPOI.price_level && (
                <div>
                  <h4 className="text-sm font-medium text-gray-500">Price Level</h4>
                  <p className="text-gray-900">{'💰'.repeat(selectedPOI.price_level)}</p>
                </div>
              )}
            </div>

            {selectedPOI.opening_hours && (
              <div>
                <h4 className="text-sm font-medium text-gray-500">Opening Status</h4>
                <p className={selectedPOI.opening_hours.open_now ? "text-green-600 font-medium" : "text-red-600 font-medium"}>
                  {selectedPOI.opening_hours.open_now ? "Open Now" : "Closed"}
                </p>
              </div>
            )}

            {selectedPOI.website && (
                <div>
                    <h4 className="text-sm font-medium text-gray-500">Website</h4>
                    <a 
                        href={selectedPOI.website} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-indigo-600 hover:text-indigo-800 underline"
                    >
                        Visit Website
                    </a>
                </div>
            )}

            <div>
              <h4 className="text-sm font-medium text-gray-500">Types</h4>
              <div className="flex flex-wrap gap-2 mt-1">
                {selectedPOI.types?.map((type: string) => (
                  <span key={type} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full capitalize">
                    {type.replace(/_/g, ' ')}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </Modal>
    </>
  );
}

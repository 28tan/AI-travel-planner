import React, { useEffect, useState } from 'react';
import Link from 'next/link';

interface Trip {
  id: string;
  _id?: string;
  destination: string;
  start_date: string;
  end_date: string;
  status: string;
  trip_title?: string; // From itinerary if generated
}

interface TripListProps {
  onSelectTrip?: (tripId: string) => void;
}

const TripList: React.FC<TripListProps> = ({ onSelectTrip }) => {
  const [trips, setTrips] = useState<Trip[]>([]);
  const [loading, setLoading] = useState(true);
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchTrips();
  }, []);

  const fetchTrips = async () => {
    try {
      const res = await fetch(`${API_URL}/trips/`, {
        credentials: 'include'
      });
      if (res.ok) {
        const data = await res.json();
        setTrips(data);
      }
    } catch (error) {
      console.error("Error fetching trips", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (e: React.MouseEvent, tripId: string) => {
    e.preventDefault(); // Prevent navigation if inside a link
    if (!confirm("Are you sure you want to delete this trip?")) return;

    try {
      const res = await fetch(`${API_URL}/trips/${tripId}`, {
        method: 'DELETE',
        credentials: 'include',
      });
      if (res.ok) {
        setTrips(trips.filter(t => (t.id || t._id) !== tripId));
      } else {
        alert("Failed to delete trip");
      }
    } catch (error) {
      console.error("Error deleting trip", error);
    }
  };

  if (loading) return <div className="text-center py-8">Loading trips...</div>;

  if (trips.length === 0) {
    return (
      <div className="text-center py-12 bg-white rounded-lg shadow">
        <p className="text-gray-500 mb-4">You haven't planned any trips yet.</p>
        <Link href="/plan" className="text-indigo-600 hover:text-indigo-800 font-medium">
          Plan your first trip &rarr;
        </Link>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {trips.map((trip) => {
        const tripId = trip.id || trip._id || '';
        return (
        <div key={tripId} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
          <div className="p-6">
            <div className="flex justify-between items-start">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                {trip.destination}
              </h3>
              <span className={`px-2 py-1 text-xs rounded-full ${
                trip.status === 'completed' ? 'bg-green-100 text-green-800' : 
                trip.status === 'draft' ? 'bg-yellow-100 text-yellow-800' : 
                'bg-gray-100 text-gray-800'
              }`}>
                {trip.status}
              </span>
            </div>
            
            <p className="text-gray-600 text-sm mb-4">
              {new Date(trip.start_date).toLocaleDateString()} - {new Date(trip.end_date).toLocaleDateString()}
            </p>
            
            <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-100">
              <Link 
                href={`/trips/${tripId}`}
                className="text-indigo-600 hover:text-indigo-800 text-sm font-medium"
              >
                View Details
              </Link>
              
              <button 
                onClick={(e) => handleDelete(e, tripId)}
                className="text-red-500 hover:text-red-700 text-sm"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
        );
      })}
    </div>
  );
};

export default TripList;

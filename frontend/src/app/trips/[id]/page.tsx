"use client";

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import TripSummary from '@/components/TripSummary';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import Spinner from '@/components/ui/Spinner';
import Link from 'next/link';

export default function TripDetailsPage() {
  const { id } = useParams();
  const { user, loading } = useAuth();
  const { showToast } = useToast();
  const router = useRouter();
  const [trip, setTrip] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
      return;
    }

    if (user && id) {
      fetchTripDetails();
    }
  }, [user, loading, id]);

  const fetchTripDetails = async () => {
    try {
      const res = await fetch(`${API_URL}/trips/${id}`, {
        credentials: 'include'
      });
      if (res.ok) {
        const data = await res.json();
        setTrip(data);
      } else {
        showToast("Failed to load trip details", "error");
        router.push('/dashboard');
      }
    } catch (error) {
      console.error("Error fetching trip", error);
      showToast("Error loading trip", "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateItinerary = async () => {
    const tripId = trip?.id || trip?._id;
    if (!trip || !tripId) return;
    
    setIsGenerating(true);
    try {
      // Use preview=true to avoid auto-saving
      const res = await fetch(`${API_URL}/trips/${tripId}/itinerary?preview=true`, {
        method: 'POST',
        credentials: 'include',
      });
      
      if (res.ok) {
        const data = await res.json();
        // Update local state with the preview itinerary
        setTrip((prev: any) => ({ ...prev, itinerary: data, isPreview: true }));
        showToast("Itinerary generated! Review and save.", "success");
      } else {
        showToast("Failed to generate itinerary.", "error");
      }
    } catch (error) {
      console.error("Error generating itinerary", error);
      showToast("Error generating itinerary.", "error");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSaveItinerary = async () => {
    const tripId = trip?.id || trip?._id;
    if (!trip || !tripId || !trip.itinerary) return;

    try {
      const res = await fetch(`${API_URL}/trips/${tripId}/itinerary`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(trip.itinerary),
        credentials: 'include',
      });

      if (res.ok) {
        setTrip((prev: any) => ({ ...prev, isPreview: false }));
        showToast("Itinerary saved successfully!", "success");
      } else {
        showToast("Failed to save itinerary.", "error");
      }
    } catch (error) {
      console.error("Error saving itinerary", error);
      showToast("Error saving itinerary.", "error");
    }
  };

  const handleDiscardItinerary = () => {
    if (!confirm("Are you sure you want to discard this itinerary?")) return;
    // Revert to original state (reload trip or just clear itinerary if it was new)
    // Ideally we should revert to the saved state.
    // For simplicity, let's just reload the trip details from server
    fetchTripDetails();
    showToast("Itinerary discarded.", "info");
  };

  if (loading || isLoading) return <Spinner />;

  if (!trip) return <div className="text-center py-12">Trip not found</div>;

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6 flex items-center justify-between">
          <Link href="/dashboard" className="text-indigo-600 hover:text-indigo-800 font-medium">
            &larr; Back to Dashboard
          </Link>
          {trip.isPreview && (
            <div className="flex space-x-4">
              <button
                onClick={handleDiscardItinerary}
                className="px-4 py-2 border border-red-300 text-red-700 rounded-md hover:bg-red-50 font-medium transition-colors"
              >
                Discard Changes
              </button>
              <button
                onClick={handleSaveItinerary}
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 font-medium transition-colors shadow-sm"
              >
                Save Itinerary
              </button>
            </div>
          )}
        </div>
        
        <h1 className="text-3xl font-bold text-gray-900 mb-6">{trip.destination} Trip</h1>
        
        <TripSummary 
          summary={trip} 
          onGenerateItinerary={handleGenerateItinerary}
          isGenerating={isGenerating}
        />
      </div>
    </div>
  );
}

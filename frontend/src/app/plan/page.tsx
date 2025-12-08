"use client";

import React, { useState, useEffect } from 'react';
import TripForm from '@/components/TripForm';
import TripSummary from '@/components/TripSummary';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import Spinner from '@/components/ui/Spinner';
import { useRouter } from 'next/navigation';

export default function PlanPage() {
  const { user, loading } = useAuth();
  const { showToast } = useToast();
  const router = useRouter();
  const [summary, setSummary] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [initialValues, setInitialValues] = useState<any>(null);
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    if (user) {
      fetchUserPreferences();
    }
  }, [user]);

  const fetchUserPreferences = async () => {
    try {
      const res = await fetch(`${API_URL}/users/me`, {
        credentials: 'include'
      });
      if (res.ok) {
        const data = await res.json();
        console.log("Fetched user preferences:", data);
        if (data.home_airport || data.default_budget || data.preferences) {
          setInitialValues({
            origin: data.home_airport || '',
            budget: data.default_budget || 1000,
            trip_preferences: data.preferences || ''
          });
        }
      }
    } catch (error) {
      console.error("Error fetching preferences", error);
    }
  };

  // Protect route
  if (!loading && !user) {
    router.push('/login');
    return null;
  }

  const handlePlanTrip = async (formData: any) => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API_URL}/trips/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
        credentials: 'include',
      });
      
      if (res.ok) {
        const data = await res.json();
        setSummary(data);
        showToast("Trip planned successfully!", "success");
      } else {
        console.error("Failed to plan trip");
        showToast("Failed to plan trip. Please try again.", "error");
      }
    } catch (error) {
      console.error("Error planning trip", error);
      showToast("Error planning trip. Please check your connection.", "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateItinerary = async () => {
    if (!summary || !summary.trip_id) return;
    
    setIsGenerating(true);
    try {
      const res = await fetch(`${API_URL}/trips/${summary.trip_id}/itinerary`, {
        method: 'POST',
        credentials: 'include',
      });
      
      if (res.ok) {
        const data = await res.json();
        setSummary({ ...summary, itinerary: data });
        showToast("Itinerary generated successfully!", "success");
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

  const handleSaveTrip = async () => {
    if (!summary || !summary.trip_id) return;
    try {
      const res = await fetch(`${API_URL}/trips/${summary.trip_id}/confirm`, {
        method: 'PUT',
        credentials: 'include',
      });
      if (res.ok) {
        showToast("Trip saved to your dashboard!", "success");
        router.push('/dashboard');
      } else {
        showToast("Failed to save trip.", "error");
      }
    } catch (error) {
      console.error("Error saving trip", error);
      showToast("Error saving trip.", "error");
    }
  };

  const handleDiscardTrip = async () => {
    if (!summary || !summary.trip_id) return;
    if (!confirm("Are you sure you want to discard this trip?")) return;
    
    try {
      const res = await fetch(`${API_URL}/trips/${summary.trip_id}`, {
        method: 'DELETE',
        credentials: 'include',
      });
      if (res.ok) {
        setSummary(null);
        showToast("Trip discarded.", "info");
      } else {
        showToast("Failed to discard trip.", "error");
      }
    } catch (error) {
      console.error("Error discarding trip", error);
      showToast("Error discarding trip.", "error");
    }
  };

  if (loading) return <Spinner />;

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Plan Your Trip</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
                  <TripForm 
        onSubmit={handlePlanTrip} 
        isLoading={isLoading} 
        initialValues={initialValues}
      />
          </div>
          
          <div className="lg:col-span-2">
            {summary ? (
              <>
                <TripSummary 
                  summary={summary} 
                  onGenerateItinerary={handleGenerateItinerary}
                  isGenerating={isGenerating}
                />
                <div className="mt-8 flex justify-end space-x-4 border-t border-gray-200 pt-6">
                  <button
                    onClick={handleDiscardTrip}
                    className="px-6 py-2 border border-red-300 text-red-700 rounded-md hover:bg-red-50 font-medium transition-colors"
                  >
                    Discard Trip
                  </button>
                  <button
                    onClick={handleSaveTrip}
                    className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium transition-colors shadow-sm"
                  >
                    Save Trip
                  </button>
                </div>
              </>
            ) : (
              <div className="bg-white p-12 rounded-lg shadow-md text-center text-gray-500">
                <p className="text-lg">Fill out the form to see your trip summary here.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

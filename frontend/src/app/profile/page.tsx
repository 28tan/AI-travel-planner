"use client";

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import Spinner from '@/components/ui/Spinner';
import { useRouter } from 'next/navigation';

export default function ProfilePage() {
  const { user, loading } = useAuth();
  const { showToast } = useToast();
  const router = useRouter();
  const [preferences, setPreferences] = useState('');
  const [homeAirport, setHomeAirport] = useState('');
  const [defaultBudget, setDefaultBudget] = useState<number | ''>('');
  const [isSaving, setIsSaving] = useState(false);
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    if (user) {
      fetchPreferences();
    }
  }, [user]);

  const fetchPreferences = async () => {
    try {
      const res = await fetch(`${API_URL}/users/me`, {
        credentials: 'include'
      });
      if (res.ok) {
        const data = await res.json();
        setPreferences(data.preferences || '');
        setHomeAirport(data.home_airport || '');
        setDefaultBudget(data.default_budget || '');
      }
    } catch (error) {
      console.error("Error fetching profile", error);
      showToast("Failed to load profile data.", "error");
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);

    try {
      const res = await fetch(`${API_URL}/users/me/preferences`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          preferences,
          home_airport: homeAirport,
          default_budget: defaultBudget === '' ? null : Number(defaultBudget)
        }),
        credentials: 'include',
      });

      if (res.ok) {
        showToast('Preferences saved successfully!', 'success');
      } else {
        showToast('Failed to save preferences.', 'error');
      }
    } catch (error) {
      console.error("Error saving preferences", error);
      showToast('Error saving preferences.', 'error');
    } finally {
      setIsSaving(false);
    }
  };

  if (!loading && !user) {
    router.push('/login');
    return null;
  }

  if (loading) return <Spinner />;

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-md overflow-hidden">
        <div className="bg-indigo-600 px-6 py-4">
          <h1 className="text-2xl font-bold text-white">User Profile</h1>
        </div>
        
        <div className="p-6">
          <div className="mb-8">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Account Information</h2>
            <div className="bg-gray-50 p-4 rounded-md">
              <p className="text-sm text-gray-500">Name</p>
              <p className="font-medium text-gray-900">{user.name}</p>
            </div>
          </div>

          <form onSubmit={handleSave}>
            <h2 className="text-lg font-medium text-gray-900 mb-4">Travel Preferences</h2>
            
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700">Home Airport (Origin)</label>
                <input
                  type="text"
                  value={homeAirport}
                  onChange={(e) => setHomeAirport(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                  placeholder="e.g. JFK"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">Default Budget (USD)</label>
                <input
                  type="number"
                  value={defaultBudget}
                  onChange={(e) => setDefaultBudget(e.target.value === '' ? '' : Number(e.target.value))}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2 border"
                  placeholder="e.g. 2000"
                />
              </div>
            </div>

            <p className="text-sm text-gray-500 mb-4">
              Tell us about your travel style. This will be used to customize your AI-generated itineraries.
              (e.g., "I love museums and history", "I prefer outdoor activities and hiking", "Foodie")
            </p>
            
            <div className="mb-4">
              <textarea
                value={preferences}
                onChange={(e) => setPreferences(e.target.value)}
                rows={5}
                className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border"
                placeholder="Enter your travel preferences..."
              />
            </div>

            <div className="flex justify-end">
              <button
                type="submit"
                disabled={isSaving}
                className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
              >
                {isSaving ? 'Saving...' : 'Save Preferences'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

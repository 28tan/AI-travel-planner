"use client";

import React, { useState, useEffect } from 'react';

interface TripFormData {
  origin: string;
  destination: string;
  start_date: string;
  end_date: string;
  budget: number;
  transportation_preference: "FLIGHT" | "DRIVE" | "BOTH";
  trip_preferences?: string;
}

interface TripFormProps {
  onSubmit: (data: TripFormData) => void;
  isLoading: boolean;
  initialValues?: Partial<TripFormData>;
}

export default function TripForm({ onSubmit, isLoading, initialValues }: TripFormProps) {
  const [formData, setFormData] = useState<TripFormData>({
    origin: '',
    destination: '',
    start_date: '',
    end_date: '',
    budget: 1000,
    transportation_preference: 'BOTH',
    trip_preferences: ''
  });

  useEffect(() => {
    if (initialValues) {
      console.log("TripForm received initialValues:", initialValues);
      setFormData(prev => ({
        ...prev,
        ...initialValues
      }));
    }
  }, [initialValues]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'budget' ? parseFloat(value) : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white p-8 rounded-lg shadow-md">
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        <div>
          <label className="block text-sm font-medium text-gray-700">Origin</label>
          <input
            type="text"
            name="origin"
            required
            value={formData.origin}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
            placeholder="New York, NY"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Destination</label>
          <input
            type="text"
            name="destination"
            required
            value={formData.destination}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
            placeholder="Tokyo, Japan"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Start Date</label>
          <input
            type="date"
            name="start_date"
            required
            value={formData.start_date}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">End Date</label>
          <input
            type="date"
            name="end_date"
            required
            value={formData.end_date}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Budget (USD)</label>
          <input
            type="number"
            name="budget"
            required
            min="0"
            value={formData.budget}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Transport Preference</label>
          <select
            name="transportation_preference"
            value={formData.transportation_preference}
            onChange={handleChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
          >
            <option value="BOTH">Both</option>
            <option value="FLIGHT">Flight Only</option>
            <option value="DRIVE">Drive Only</option>
          </select>
        </div>
        <div className="md:col-span-2">
          <label className="block text-sm font-medium text-gray-700">Trip Preferences (Optional)</label>
          <textarea
            name="trip_preferences"
            value={formData.trip_preferences || ''}
            onChange={handleChange}
            rows={3}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2 border"
            placeholder="Specific interests for this trip (e.g., 'Focus on food', 'Kid-friendly activities')"
          />
        </div>
      </div>
      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isLoading}
          className="inline-flex justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {isLoading ? 'Planning...' : 'Plan Trip'}
        </button>
      </div>
    </form>
  );
}

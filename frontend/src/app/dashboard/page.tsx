"use client";

import React from 'react';
import TripList from '@/components/TripList';
import { useAuth } from '@/context/AuthContext';
import Spinner from '@/components/ui/Spinner';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function DashboardPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  if (!loading && !user) {
    router.push('/login');
    return null;
  }

  if (loading) return <Spinner />;

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Trips</h1>
          <Link 
            href="/plan"
            className="bg-indigo-600 text-white px-4 py-2 rounded-md font-medium hover:bg-indigo-700"
          >
            Plan New Trip
          </Link>
        </div>
        
        <TripList />
      </div>
    </div>
  );
}

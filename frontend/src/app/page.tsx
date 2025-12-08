import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-white dark:bg-slate-900 text-slate-900 dark:text-white">
      
      {/* Hero Section */}
      <main className="flex-grow">
        <section className="relative py-20 lg:py-32 px-6 overflow-hidden">
          <div className="absolute inset-0 -z-10 opacity-10 dark:opacity-20">
             <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[1000px] rounded-full bg-gradient-to-b from-blue-400 to-teal-300 blur-3xl"></div>
          </div>
          
          <div className="max-w-5xl mx-auto text-center">
            <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8">
              Discover Your Next <br/>
              <span className="text-blue-600 dark:text-blue-400">Adventure</span>
            </h1>
            <p className="text-xl md:text-2xl text-slate-600 dark:text-slate-300 mb-10 max-w-3xl mx-auto leading-relaxed">
              Experience the future of travel planning. Our AI builds personalized itineraries, finds the best flights, and optimizes your route in seconds.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/login" 
                className="px-8 py-4 rounded-full bg-blue-600 text-white font-bold text-lg hover:bg-blue-700 hover:shadow-lg hover:-translate-y-1 transition-all duration-300"
              >
                Start Planning Free
              </Link>
              <Link 
                href="#features" 
                className="px-8 py-4 rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 font-bold text-lg hover:bg-slate-50 dark:hover:bg-slate-700 transition-all duration-300"
              >
                Learn More
              </Link>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section id="features" className="py-20 bg-slate-50 dark:bg-slate-800/50">
          <div className="max-w-7xl mx-auto px-6">
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">Why Choose AI Travel Planner?</h2>
            
            <div className="grid md:grid-cols-3 gap-10">
              {/* Feature 1 */}
              <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl shadow-sm hover:shadow-md transition-shadow border border-slate-100 dark:border-slate-700">
                <div className="w-14 h-14 bg-blue-100 dark:bg-blue-900/30 rounded-xl flex items-center justify-center text-3xl mb-6">
                  🤖
                </div>
                <h3 className="text-xl font-bold mb-3">Smart Itineraries</h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Forget generic guides. Get a day-by-day plan tailored to your interests, budget, and pace.
                </p>
              </div>

              {/* Feature 2 */}
              <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl shadow-sm hover:shadow-md transition-shadow border border-slate-100 dark:border-slate-700">
                <div className="w-14 h-14 bg-teal-100 dark:bg-teal-900/30 rounded-xl flex items-center justify-center text-3xl mb-6">
                  ✈️
                </div>
                <h3 className="text-xl font-bold mb-3">Live Flight Search</h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Instantly find the best flights
                </p>
              </div>

              {/* Feature 3 */}
              <div className="bg-white dark:bg-slate-800 p-8 rounded-2xl shadow-sm hover:shadow-md transition-shadow border border-slate-100 dark:border-slate-700">
                <div className="w-14 h-14 bg-purple-100 dark:bg-purple-900/30 rounded-xl flex items-center justify-center text-3xl mb-6">
                  🚗
                </div>
                <h3 className="text-xl font-bold mb-3">Multi-Mode Transport</h3>
                <p className="text-slate-600 dark:text-slate-400">
                  Compare driving vs. flying
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* How it Works */}
        <section id="how-it-works" className="py-20">
          <div className="max-w-7xl mx-auto px-6">
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-16">How It Works</h2>
            <div className="grid md:grid-cols-3 gap-8 text-center">
              <div className="relative">
                <div className="text-8xl font-bold text-slate-100 dark:text-slate-800 absolute -top-10 left-1/2 -translate-x-1/2 -z-10">1</div>
                <h3 className="text-xl font-bold mb-2">Tell us your dream</h3>
                <p className="text-slate-600 dark:text-slate-400">Enter your destination, dates, and budget.</p>
              </div>
              <div className="relative">
                <div className="text-8xl font-bold text-slate-100 dark:text-slate-800 absolute -top-10 left-1/2 -translate-x-1/2 -z-10">2</div>
                <h3 className="text-xl font-bold mb-2">AI does the magic</h3>
                <p className="text-slate-600 dark:text-slate-400">We analyze thousands of options to build your perfect trip.</p>
              </div>
              <div className="relative">
                <div className="text-8xl font-bold text-slate-100 dark:text-slate-800 absolute -top-10 left-1/2 -translate-x-1/2 -z-10">3</div>
                <h3 className="text-xl font-bold mb-2">Pack & Go</h3>
                <p className="text-slate-600 dark:text-slate-400">Save your itinerary, book your flights, and enjoy!</p>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-12">
        <div className="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <span className="text-xl font-bold text-white">AI Travel Planner</span>
            <p className="text-sm mt-2">© 2025 All rights reserved.</p>
          </div>
          <div className="flex gap-6">
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
            <a href="#" className="hover:text-white transition-colors">Contact</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

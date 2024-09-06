import React from 'react';
import { MenuIcon, XIcon } from '@heroicons/react/outline';
import { useState } from 'react';
import backgroundSvg from '../Decore.svg';
import girlImage from '../Image.png';
import random from '../abc.svg'
import tripImage from '../trip.png'
import InfoCard from './card';

const LandingPage = () => {
  const [nav, setNav] = useState(false);

  const handleClick = () => {
    setNav(!nav);
  };

  return (
    <div className="relative bg-gray-50">
      {/* Navbar */}
      <nav className="bg-[#fff1da] w-full  px-4 sm:px-6 lg:px-8 py-2 flex justify-between items-center">
        <div className="flex items-center">
          <h1 className="text-3xl font-bold text-gray-900">Travello</h1>
        </div>
        <div className="hidden md:flex space-x-8">
          <a href="#destinations" className="text-gray-700 hover:text-gray-900 py-1">Destinations</a>
          <a href="#hotels" className="text-gray-700 hover:text-gray-900 py-1">Hotels</a>
          <a href="#flights" className="text-gray-700 hover:text-gray-900 py-1">Flights</a>
          <a href="#bookings" className="text-gray-700 hover:text-gray-900 py-1">Bookings</a>
          <a href="#login" className="text-gray-700 hover:text-gray-900 py-1">Login</a>
          <a href="#signup" className="px-4 py-1 text-white bg-yellow-500 rounded-md hover:bg-yellow-600">Sign Up</a>
        </div>
        {/* Mobile Menu Button */}
        <div className="md:hidden">
          <button onClick={handleClick}>
            {!nav ? (
              <MenuIcon className="h-6 w-6 text-gray-900" />
            ) : (
              <XIcon className="h-6 w-6 text-gray-900" />
            )}
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div className={`md:hidden ${nav ? 'block' : 'hidden'} bg-white shadow-lg`}>
        <a href="#destinations" className="block px-4 py-2 text-gray-700">Destinations</a>
        <a href="#hotels" className="block px-4 py-2 text-gray-700">Hotels</a>
        <a href="#flights" className="block px-4 py-2 text-gray-700">Flights</a>
        <a href="#bookings" className="block px-4 py-2 text-gray-700">Bookings</a>
        <a href="#login" className="block px-4 py-2 text-gray-700">Login</a>
        <a href="#signup" className="block px-4 py-2 text-white bg-yellow-500">Sign Up</a>
      </div>

      {/* Hero Section */}
      <div className="relative flex flex-col-reverse md:flex-row items-center">
        <div className="md:w-1/2 p-8 md:pl-20 text-center md:text-left">
          <h2 className="text-4xl md:text-6xl font-bold text-gray-900 leading-tight">Travel, enjoy<br />and live a new<br />and full life</h2>
          <p className="text-lg text-gray-700 mt-4">
            Built Wicket longer admire do barton vanity itself do in it.
            Preferred to sportsmen it engrossed listening. Park gate
            sell they west hard for the.
          </p>
          <div className="mt-8 flex justify-center md:justify-start">
            <a href="#find-out" className="px-8 py-3 bg-yellow-500 text-white rounded-md shadow-lg hover:bg-yellow-600">Find out more</a>
            <a href="#play-demo" className="ml-4 px-8 py-3 bg-white text-gray-900 rounded-md shadow-lg hover:bg-gray-100 flex items-center">
              <span className="mr-2">Play Demo</span>
              <span className="h-4 w-4 bg-red-500 rounded-full"></span>
            </a>
          </div>
        </div>
        <div className="md:w-1/2 relative">
          <img src={backgroundSvg} alt="Background" className="absolute inset-0 w-full h-full object-cover" />
          <img src={girlImage} alt="Girl with suitcase" className="relative z-10 max-w-full h-auto mx-auto" />
        </div>
      </div>

      <section>
      <div className=" flex flex-col md:flex-row items-center justify-center p-6 md:p-12 bg-white">
      {/* Left Side */}
      <div className="md:ml-5 md:w-1/2 space-y-6">
        <h1 className="text-xl md:text-2xl font-bold text-gray-500">
          Easy and Fast
        </h1>
        <h2 className="text-3xl md:text-5xl font-bold text-gray-800">
          Book Your Next Trip In 3 Easy Steps
        </h2>

        {/* Steps */}
        <div className="space-y-4">
          <div className=" md:ml-9 flex items-start space-x-4">
            <div className="bg-yellow-400 p-3 rounded-md">
              {/* SVG for Choose Destination */}
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                {/* Add your SVG path here */}
              </svg>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-800">
                Choose Destination
              </h3>
              <p className="text-gray-600">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Urna,
                tortor tempus.
              </p>
            </div>
          </div>

          <div className=" md:ml-9 flex items-start space-x-4">
            <div className="bg-red-400 p-3 rounded-md">
              {/* SVG for Make Payment */}
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                {/* Add your SVG path here */}
              </svg>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-800">Make Payment</h3>
              <p className="text-gray-600">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Urna,
                tortor tempus.
              </p>
            </div>
          </div>

          <div className=" md:ml-9 flex items-start space-x-4">
            <div className="bg-teal-600 p-3 rounded-md">
              {/* SVG for Reach Airport */}
              <svg
                className="w-6 h-6 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                {/* Add your SVG path here */}
              </svg>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-gray-800">
                Reach Airport on Selected Date
              </h3>
              <p className="text-gray-600">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Urna,
                tortor tempus.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side */}
      <div className="md:w-1/2 md:mt-0 md:ml-12 relative">
        <div className="bg-white  rounded-xl overflow-hidden">
          <img
            src={tripImage} // Replace with your image source
            alt="Trip To Greece"
            className="w-full object-cover"
          />
        </div>
      </div>
    </div>
      </section>

      <section>
        <div>
          <div className='text-2xl text-center'>
             <h1 className='text-3xl md:text-5xl font-bold text-gray-800 mt-10'>We offer the following services</h1>
             <p className=' text-gray-600'>The best in the market</p>
          </div>
          <div className='grid grid-cols-1 sm:grid-cols-2  md:grid-cols-4 md:space-x-5 p-10'>
           <InfoCard svgIcon={random} title="Hasslefree Trip Planning" description ="We provide our users with the best services there are in the town obviously in the market but also in the best soln of the jgnere" />
           <InfoCard svgIcon={random} title="Hasslefree Trip Planning" description ="We provide our users with the best services there are in the town obviously in the market but also in the best soln of the jgnere" />
           <InfoCard svgIcon={random} title="Hasslefree Trip Planning" description ="We provide our users with the best services there are in the town obviously in the market but also in the best soln of the jgnere" />
           <InfoCard svgIcon={random} title="Hasslefree Trip Planning" description ="We provide our users with the best services there are in the town obviously in the market but also in the best soln of the jgnere" />
          </div>
        </div>
      </section>
    </div>
  );
}

export default LandingPage;

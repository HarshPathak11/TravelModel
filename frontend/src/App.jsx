import { useState } from 'react'
import Map from './map'
import LocationSearch from './forwardgeoencoding'
import LandingPage from './home'

function App() {
 

  return (
    <>
    {/* <div className='min-h-screen p-10 flex justify-center'>
      <div className='w-full'><Map/></div>
      <LocationSearch/>
      </div> */}
      <LandingPage/>
    </>
  )
}

export default App

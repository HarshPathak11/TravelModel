import React from 'react';

const InfoCard = ({ svgIcon, title, description }) => {
  return (
    <div className="max-w-xs mx-auto bg-yellow-500 rounded-xl shadow-md overflow-hidden md:max-w-sm">
      <div className="flex justify-center mt-5">
        <div className="flex items-center justify-center">
          {/* Insert the SVG icon here */}
          <img src={svgIcon}/>
        </div>
      </div>
      <div className="p-6">
        <h3 className="text-center text-xl font-semibold text-gray-800">{title}</h3>
        <p className="mt-4 text-gray-600 text-center">{description}</p>
      </div>
    </div>
  );
};

export default InfoCard;
import React from 'react';

const LoadingPlaceholder = () => (
  <div className="p-6 text-center">
    <div className="bg-gray-100 rounded-lg shadow-sm h-64 flex items-center justify-center animate-pulse">
      <span className="text-lg text-gray-600">Loading...</span>
    </div>
  </div>
);

export default LoadingPlaceholder;

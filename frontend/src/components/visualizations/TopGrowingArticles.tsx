import React, { useEffect, useState } from 'react';
import { getTopGrowingData, TopGrowingData } from '../../lib/api';

const TopGrowingArticles = () => {
  const [topGrowingData, setTopGrowingData] = useState<TopGrowingData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    getTopGrowingData('2024-09-01', 10)
      .then((data) => {
        setTopGrowingData(data);
      })
      .catch((error) => console.error('Failed to get data', error))
      .finally(() => setIsLoading(false));
  }, []);

  const formatBytes = (bytes: number) => {
    if (Math.abs(bytes) > 1000000) {
      return `${(bytes / 1000000).toFixed(1)}M`;
    }
    if (Math.abs(bytes) > 1000) {
      return `${(bytes / 1000).toFixed(1)}K`;
    }
    return bytes;
  };

  if (isLoading) {
    return (
      <div className="p-6 bg-white rounded-lg shadow-sm">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/4"></div>
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-4 bg-gray-200 rounded w-full"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-white rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Top Growing Articles
      </h2>
      <div className="space-y-3">
        {topGrowingData.map((data) => (
          <div
            key={data.page_name}
            className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-md transition-colors"
          >
            <span className="text-gray-700 font-medium truncate flex-1">
              {data.page_name}
            </span>
            <span
              className={`px-3 py-1 rounded-full text-sm ${
                data.net_bytes_changed > 0
                  ? 'bg-green-100 text-green-800'
                  : 'bg-red-100 text-red-800'
              }`}
            >
              {data.net_bytes_changed > 0 ? '+' : ''}
              {formatBytes(data.net_bytes_changed)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TopGrowingArticles;

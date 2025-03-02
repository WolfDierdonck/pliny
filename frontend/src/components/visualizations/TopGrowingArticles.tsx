import React, { useEffect, useState } from 'react';
import {
  getTopGrowingData,
  TopGrowingData,
  getTopShrinkingData,
  TopShrinkingData,
} from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';

const TopGrowingArticles = ({ date }: { date: string }) => {
  const [topGrowingData, setTopGrowingData] = useState<TopGrowingData[]>([]);
  const [topShrinkingData, setTopShrinkingData] = useState<TopShrinkingData[]>(
    [],
  );
  const [isLoading, setIsLoading] = useState(true);
  const [isShrinkingLoading, setIsShrinkingLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    getTopGrowingData(date, 10)
      .then((data) => {
        setTopGrowingData(data);
      })
      .catch((error) => {
        console.error('Failed to get growing data', error);
        setTopGrowingData([]); // reset to default
      })
      .finally(() => setIsLoading(false));

    setIsShrinkingLoading(true);
    getTopShrinkingData(date, 10)
      .then((data) => {
        setTopShrinkingData(data);
      })
      .catch((error) => {
        console.error('Failed to get shrinking data', error);
        setTopShrinkingData([]); // reset to default
      })
      .finally(() => setIsShrinkingLoading(false));
  }, [date]);

  const formatBytes = (bytes: number) => {
    if (Math.abs(bytes) > 1000000) {
      return `${(bytes / 1000000).toFixed(1)} MB`;
    }
    if (Math.abs(bytes) > 1000) {
      return `${(bytes / 1000).toFixed(1)} KB`;
    }
    return bytes;
  };

  if (isLoading) {
    return <LoadingPlaceholder />;
  }
  if (!topGrowingData?.length || !topShrinkingData?.length) {
    return <NoDataPlaceholder />;
  }

  return (
    <div className="flex flex-col md:flex-row gap-8">
      <div className="w-full md:w-1/2 p-6 bg-white rounded-lg shadow-sm">
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
                {data.page_name.replace(/_/g, ' ')}
              </span>
              <span
                className={`px-3 py-1 rounded-full text-sm ${
                  data.abs_bytes_changed > 0
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}
              >
                {data.abs_bytes_changed > 0 ? '+' : ''}
                {formatBytes(data.abs_bytes_changed)}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="w-full md:w-1/2 p-6 bg-white rounded-lg shadow-sm">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">
          Top Shrinking Articles
        </h2>
        {isShrinkingLoading ? (
          <LoadingPlaceholder />
        ) : (
          <div className="space-y-3">
            {topShrinkingData
              .slice() // copy so as not to mutate state
              .reverse()
              .map((data) => (
                <div
                  key={data.page_name}
                  className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-md transition-colors"
                >
                  <span className="text-gray-700 font-medium truncate flex-1">
                    {data.page_name.replace(/_/g, ' ')}
                  </span>
                  <span
                    className={`px-3 py-1 rounded-full text-sm ${
                      data.net_bytes_changed < 0
                        ? 'bg-red-100 text-red-800'
                        : 'bg-green-100 text-green-800'
                    }`}
                  >
                    {data.net_bytes_changed < 0 ? '' : '+'}
                    {formatBytes(data.net_bytes_changed)}
                  </span>
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default TopGrowingArticles;

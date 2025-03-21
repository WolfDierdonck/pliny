import React, { useEffect, useState } from 'react';
import { TopGrowingData, TopShrinkingData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';
import { BackendData } from '../Home';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '../ui/shadcn/card';

const TopGrowingArticles = ({ backendData }: { backendData: BackendData }) => {
  const [topGrowingData, setTopGrowingData] = useState<TopGrowingData[]>([]);
  const [topShrinkingData, setTopShrinkingData] = useState<TopShrinkingData[]>(
    [],
  );
  const [isGrowingLoading, setIsGrowingLoading] = useState(true);
  const [isShrinkingLoading, setIsShrinkingLoading] = useState(true);

  useEffect(() => {
    setIsGrowingLoading(true);
    backendData.topGrowing
      .then((data) => {
        setTopGrowingData(data);
      })
      .catch((error) => {
        console.error('Failed to get growing data', error);
        setTopGrowingData([]); // reset to default
      })
      .finally(() => setIsGrowingLoading(false));

    setIsShrinkingLoading(true);
    backendData.topShrinking
      .then((data) => {
        setTopShrinkingData(data);
      })
      .catch((error) => {
        console.error('Failed to get shrinking data', error);
        setTopShrinkingData([]); // reset to default
      })
      .finally(() => setIsShrinkingLoading(false));
  }, [backendData]);

  const formatBytes = (bytes: number) => {
    if (Math.abs(bytes) > 1000000) {
      return `${(bytes / 1000000).toFixed(1)} MB`;
    }
    if (Math.abs(bytes) > 1000) {
      return `${(bytes / 1000).toFixed(1)} KB`;
    }
    return bytes;
  };

  if (isGrowingLoading) {
    return <LoadingPlaceholder />;
  }
  if (!topGrowingData?.length || !topShrinkingData?.length) {
    return <NoDataPlaceholder />;
  }

  return (
    <div className="flex flex-col md:flex-row gap-8">
      <Card>
        <CardHeader>
          <CardTitle>Top Growing Articles</CardTitle>
          <CardDescription>
            Articles with the most bytes added in the last 24 hours
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {topGrowingData.map((data) => (
              <div
                key={data.page_name}
                className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-md transition-colors"
              >
                <span className="text-gray-700 font-medium px-3 flex-1">
                  {data.page_name}
                </span>
                <span
                  className={`px-3 py-1 rounded-full text-sm ${
                    data.abs_bytes_changed > 0
                      ? 'bg-lime-800/30 text-lime-800'
                      : 'bg-red-800/30 text-red-800'
                  }`}
                >
                  {data.abs_bytes_changed > 0 ? '+' : ''}
                  {formatBytes(data.abs_bytes_changed)}
                </span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Top Shrinking Articles</CardTitle>
          <CardDescription>
            Articles with the most bytes removed in the last 24 hours
          </CardDescription>
        </CardHeader>
        <CardContent>
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
                    <span className="text-gray-700 font-medium px-3 flex-1">
                      {data.page_name}
                    </span>
                    <span
                      className={`px-3 py-1 rounded-full text-sm ${
                        data.net_bytes_changed > 0
                          ? 'bg-lime-800/30 text-lime-800'
                          : 'bg-red-800/30 text-red-800'
                      }`}
                    >
                      {data.net_bytes_changed < 0 ? '' : '+'}
                      {formatBytes(data.net_bytes_changed)}
                    </span>
                  </div>
                ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default TopGrowingArticles;

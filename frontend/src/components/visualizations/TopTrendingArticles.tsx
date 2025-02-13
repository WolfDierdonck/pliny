import React, { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from 'recharts';
import { getTopViewDeltaData, TopViewDeltaData } from '../../lib/api';

type TopTrendingArticles = TopViewDeltaData & { growth_percentage: string };

const TopTrendingArticles = () => {
  const [data, setData] = useState<TopTrendingArticles[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    getTopViewDeltaData('2024-09-07', 10)
      .then((data) => {
        const processedData = data.map((item) => ({
          ...item,
          page_name: item.page_name.replace(/_/g, ' '),
          growth_percentage: ((item.view_count_ratio - 1) * 100).toFixed(1),
        }));
        setData(processedData);
      })
      .catch((error) => console.error('Failed to get data', error))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return (
      <div className="p-6 bg-white rounded-lg shadow-sm">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/4"></div>
          <div className="h-64 bg-gray-200 rounded w-full"></div>
        </div>
      </div>
    );
  }

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-4 shadow-lg rounded-lg border">
          <p className="font-medium">{data.page_name}</p>
          <p className="text-gray-600">
            Previous: {data.previous_view_count.toLocaleString()} views
          </p>
          <p className="text-gray-600">
            Current: {data.current_view_count.toLocaleString()} views
          </p>
          <p className="text-green-600">Growth: +{data.growth_percentage}%</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Trending Articles
      </h2>
      <ResponsiveContainer width="100%" height={500}>
        <BarChart
          data={data}
          margin={{ top: 20, right: 30, bottom: 70, left: 60 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="page_name"
            angle={-45}
            textAnchor="end"
            height={100}
            interval={0}
          />
          <YAxis />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Bar
            dataKey="previous_view_count"
            fill="#94a3b8"
            name="Previous Views"
          />
          <Bar
            dataKey="current_view_count"
            fill="#ff7c43"
            name="Current Views"
          />
        </BarChart>
      </ResponsiveContainer>
      <div className="mt-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {data.map((item) => (
          <div
            key={item.page_name}
            className="p-3 bg-gray-50 rounded-lg text-sm"
          >
            <div className="font-medium truncate" title={item.page_name}>
              {item.page_name}
            </div>
            <div className="text-green-600">+{item.growth_percentage}%</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TopTrendingArticles;

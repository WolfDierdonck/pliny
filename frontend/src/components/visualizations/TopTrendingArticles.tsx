import React, { useEffect, useState } from 'react';
import { LineChart, Line, ResponsiveContainer, Legend } from 'recharts';
import { getTopViewsGainedData, TopViewsGainedData } from '../../lib/api';

const colors = [
  '#ff7c43',
  '#8884d8',
  '#82ca9d',
  '#ffc658',
  '#8dd1e1',
  '#d0ed57',
  '#a4de6c',
  '#d88884',
  '#c4a3d6',
  '#ffbb28',
];

const TopTrendingArticles = () => {
  const [articles, setArticles] = useState<TopViewsGainedData[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    getTopViewsGainedData('2024-09-07', 10)
      .then((articlesData) => {
        setArticles(articlesData);
        const days: { day: string; [key: string]: number | string }[] = [
          { day: 'Two Days Ago' },
          { day: 'One Day Ago' },
          { day: 'Current' },
        ];
        articlesData.forEach((article) => {
          days[0][article.page_name] = article.two_days_ago_view_count;
          days[1][article.page_name] = article.one_day_ago_view_count;
          days[2][article.page_name] = article.current_view_count;
        });
        setChartData(days);
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

  return (
    <div className="p-6 bg-white rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Trending Articles
      </h2>
      <ResponsiveContainer width="100%" height={500}>
        <LineChart
          data={chartData}
          margin={{ top: 20, right: 30, bottom: 70, left: 60 }}
        >
          <Legend />
          {articles.map((article, index) => (
            <Line
              key={article.page_name}
              type="monotone"
              dataKey={article.page_name}
              name={article.page_name.replace(/_/g, ' ')}
              stroke={colors[index % colors.length]}
              strokeWidth={2}
              dot={{ r: 3 }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TopTrendingArticles;

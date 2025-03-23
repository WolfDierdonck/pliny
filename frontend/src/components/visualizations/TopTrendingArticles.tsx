import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  ResponsiveContainer,
  Legend,
  CartesianGrid,
  YAxis,
  XAxis,
} from 'recharts';
import { TopViewsGainedData, TopViewsLostData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';
import { BackendData } from '../Home';

// Replace the single colors array with separate arrays for gains and losses
const gainColors = ['#2ca02c', '#1f77b4', '#ff7f0e', '#17becf'];
const lossColors = ['#d62728', '#9467bd', '#8c564b', '#e377c2'];

const TopTrendingArticles = ({ backendData }: { backendData: BackendData }) => {
  // Initialize array states to []
  const [gainedArticles, setGainedArticles] = useState<TopViewsGainedData[]>(
    [],
  );
  const [lostArticles, setLostArticles] = useState<TopViewsLostData[]>([]);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [chartData, setChartData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    Promise.all([backendData.topViewsGained, backendData.topViewsLost])
      .then(([gainedData, lostData]) => {
        setGainedArticles(gainedData);
        setLostArticles(lostData);
        const days: { day: string; [key: string]: number | string }[] = [
          { day: '2 Days Ago' },
          { day: 'Yesterday' },
          { day: 'Today' },
        ];
        // For gained articles: baseline is yesterday (0)
        gainedData.forEach((article) => {
          days[1][article.page_name] = 0; // Yesterday baseline
          days[2][article.page_name] =
            article.current_view_count - article.one_day_ago_view_count;
          days[0][article.page_name] =
            article.two_days_ago_view_count - article.one_day_ago_view_count;
        });
        // For lost articles: baseline is yesterday (0) and differences are negated
        lostData.forEach((article) => {
          days[1][article.page_name] = 0; // Yesterday baseline
          days[2][article.page_name] =
            article.current_view_count - article.one_day_ago_view_count;
          days[0][article.page_name] =
            article.two_days_ago_view_count - article.one_day_ago_view_count;
        });
        setChartData(days);
      })
      .catch((error) => {
        console.error('Failed to get data', error);
        setGainedArticles([]); // reset to default
        setLostArticles([]); // reset to default
        setChartData([]); // reset to default
      })
      .finally(() => setIsLoading(false));
  }, [backendData]);

  if (isLoading) {
    return <LoadingPlaceholder />;
  }
  if (!gainedArticles?.length || !lostArticles?.length) {
    return <NoDataPlaceholder />;
  }

  return (
    <div className="p-6 bg-white rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Trending Articles (Gained & Lost Views)
      </h2>
      <ResponsiveContainer width="100%" height={500}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="day" />
          <YAxis />
          <Legend />
          {gainedArticles.map((article, index) => (
            <Line
              key={article.page_name}
              type="monotone"
              dataKey={article.page_name}
              name={article.page_name}
              stroke={gainColors[index % gainColors.length]} // use gainColors here
              dot={false}
            />
          ))}
          {lostArticles.map((article, index) => (
            <Line
              key={article.page_name}
              type="monotone"
              dataKey={article.page_name}
              name={article.page_name}
              stroke={lossColors[index % lossColors.length]} // use lossColors here
              dot={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TopTrendingArticles;

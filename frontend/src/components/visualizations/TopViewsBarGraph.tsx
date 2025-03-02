import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from 'recharts';
import { getTopViewsData, TopViewsData } from '../../lib/api';

const TopViewsBarGraph = () => {
  const [viewData, setViewData] = useState<TopViewsData[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);

  useEffect(() => {
    getTopViewsData('2024-09-07', 10)
      .then((data) => {
        setViewData(data);
        // Transform data: For each day (0-6) compute the corresponding date,
        // then create an object with day and view counts per article.
        const transformed = Array.from({ length: 7 }, (_, dayOffset) => {
          const dateObj = new Date();
          dateObj.setDate(dateObj.getDate() - dayOffset);
          const formattedDate = dateObj.toISOString().split('T')[0];
          const dayData: { day: string; [key: string]: number | string } = {
            day: formattedDate,
          };
          data.forEach((article) => {
            dayData[article.page_name] = (article as any)[
              `view_count_${dayOffset}`
            ];
          });
          return dayData;
        }).reverse();
        setChartData(transformed);
      })
      .catch((error) => console.error('Failed to get data', error));
  }, []);

  // Use a muted colors palette
  const colors = [
    '#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728',
    '#9467bd',
    '#8c564b',
    '#e377c2',
    '#7f7f7f',
    '#bcbd22',
    '#17becf',
  ];

  // Define a custom dot component that renders only on the last day.
  const CustomDot = (props: any) => {
    const { cx, cy, stroke, index } = props;
    if (chartData.length && index === chartData.length - 1) {
      return <circle cx={cx} cy={cy} r={5} stroke={stroke} fill={stroke} />;
    }
    return null;
  };

  return (
    <ResponsiveContainer width="100%" height={500} style={{ padding: 20 }}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="day" />
        <YAxis />
        <Tooltip />
        {viewData.map((article, idx) => (
          <Line
            key={article.page_name}
            type="monotone"
            dataKey={article.page_name}
            stroke={colors[idx % colors.length]}
            strokeWidth={2}
            dot={<CustomDot />}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
};

export default TopViewsBarGraph;

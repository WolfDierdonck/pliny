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

const TopViews = ({ date }: { date: string }) => {
  const [viewData, setViewData] = useState<TopViewsData[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);

  useEffect(() => {
    getTopViewsData(date, 10)
      .then((data) => {
        setViewData(data);
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
  }, [date]);

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
            dot={<CustomDot />}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
};

export default TopViews;

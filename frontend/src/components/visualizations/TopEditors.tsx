import React, { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { getTopEditorsData, TopEditorsData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';

const TopEditors = ({ date }: { date: string }) => {
  const [data, setData] = useState<TopEditorsData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    getTopEditorsData(date, 15)
      .then((data) => {
        const processedData = data.map((item) => ({
          ...item,
          page_name: item.page_name.replace(/_/g, ' '),
        }));
        setData(processedData);
      })
      .catch((error) => {
        console.error('Failed to get data', error);
        setData([]); // reset to default
      })
      .finally(() => setIsLoading(false));
  }, [date]);

  if (isLoading) {
    return <LoadingPlaceholder />;
  }
  if (!data?.length) {
    return <NoDataPlaceholder />;
  }

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-4 shadow-lg rounded-lg border">
          <p className="font-medium">{data.page_name}</p>
          <p className="text-gray-600">{data.editor_count} unique editors</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Articles by Unique Editors
      </h2>
      <ResponsiveContainer width="100%" height={500}>
        <BarChart
          data={data}
          margin={{ top: 20, right: 20, bottom: 70, left: 60 }}
        >
          <XAxis
            dataKey="page_name"
            angle={-45}
            textAnchor="end"
            height={100}
            interval={0}
          />
          <YAxis
            label={{
              value: 'Number of Unique Editors',
              angle: -90,
              position: 'insideLeft',
            }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="editor_count" fill="#8884d8" fillOpacity={0.6} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TopEditors;

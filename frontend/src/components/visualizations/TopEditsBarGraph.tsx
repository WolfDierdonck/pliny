import React, { useEffect, useState } from 'react';
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ZAxis,
} from 'recharts';
import { getTopEditsData, TopEditsData } from '../../lib/api';

const TopEditsBarGraph = () => {
  const [data, setData] = useState<TopEditsData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    getTopEditsData('2024-09-07', 15)
      .then((data) => {
        const processedData = data.map((item, index) => ({
          ...item,
          page_name: item.page_name.replace(/_/g, ' '),
          x: index, // Use index for X-axis spacing
          y: item.edit_count,
          z: item.edit_count, // Use edit_count for bubble size
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
          <p className="text-gray-600">{data.edit_count} edits</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">
        Most Edited Articles
      </h2>
      <ResponsiveContainer width="100%" height={500}>
        <ScatterChart margin={{ top: 20, right: 20, bottom: 70, left: 60 }}>
          <XAxis
            dataKey="x"
            name="Article"
            tickFormatter={(value) => {
              const item = data[value];
              return item ? item.page_name : '';
            }}
            angle={-45}
            textAnchor="end"
            height={100}
            interval={0}
          />
          <YAxis
            dataKey="y"
            name="Edit Count"
            label={{
              value: 'Number of Edits',
              angle: -90,
              position: 'insideLeft',
            }}
          />
          <ZAxis dataKey="z" range={[400, 2000]} name="Size" />
          <Tooltip content={<CustomTooltip />} />
          <Scatter
            name="Articles"
            data={data}
            fill="#82ca9d"
            fillOpacity={0.6}
          />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TopEditsBarGraph;

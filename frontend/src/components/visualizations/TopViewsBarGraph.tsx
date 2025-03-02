import React, { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from 'recharts';
import { getTopViewsData, TopViewsData } from '../../lib/api';

const TopViewsBarGraph = () => {
  const [viewData, setViewData] = useState<TopViewsData[]>([]);

  useEffect(() => {
    getTopViewsData('2024-09-04', 10)
      .then((data) => setViewData(data))
      .catch((error) => console.error('Failed to get data', error));
  }, []);

  return (
    <ResponsiveContainer width="100%" height={500} style={{ padding: 20 }}>
      <BarChart data={viewData}>
        <CartesianGrid strokeDasharray="3 3" />
        {/* use vertical x-axis labels */}
        <XAxis dataKey="page_name" angle={-45} textAnchor="end" height={100} />
        <YAxis />
        <Tooltip />
        <Bar dataKey="view_count_0" fill="#8884d8" />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default TopViewsBarGraph;

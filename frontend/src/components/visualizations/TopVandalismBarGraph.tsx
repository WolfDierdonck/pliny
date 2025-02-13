import React, { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import { getTopVandalismData, TopVandalismData } from '../../lib/api';

type TopVandalizedWithPercentKept = TopVandalismData & { percent_kept: number };

const TopVandalismBarGraph = () => {
  const [vandalizedData, setVandalizedData] = useState<
    TopVandalizedWithPercentKept[]
  >([]);

  useEffect(() => {
    getTopVandalismData('2024-09-07', 10)
      .then((data) => {
        const vandalizedDataWithPercentKept = data
          // .sort(() => 0.5 - Math.random())
          // .slice(0, 10)
          .map((data) => ({
            ...data,
            page_name: data.page_name.replace(/_/g, ' '),
            percent_reverted: (data.revert_count / data.edit_count) * 100,
            percent_kept: 100 - (data.revert_count / data.edit_count) * 100,
          }));
        setVandalizedData(vandalizedDataWithPercentKept);
      })
      .catch((error) => console.error('Failed to get data', error));
  }, []);

  return (
    <ResponsiveContainer width="100%" height={500} style={{ padding: 20 }}>
      <BarChart data={vandalizedData}>
        <CartesianGrid />
        <XAxis dataKey="page_name" angle={-45} textAnchor="end" height={100} />
        <YAxis />
        <Tooltip />
        <Legend />
        {/* <Bar dataKey="view_count" stackId="a" fill="#8884d8" /> */}
        <Bar dataKey="revert_count" stackId="a" fill="#82ca9d" />
        {/* <Bar dataKey="bytes_reverted" stackId="a" fill="#ffc658" /> */}
        {/* <Bar dataKey="percent_reverted" stackId="a" fill="#ff82ab" /> */}
        {/* <Bar dataKey="percent_kept" stackId="a" fill="#ffc658" /> */}
      </BarChart>
    </ResponsiveContainer>
  );
};

export default TopVandalismBarGraph;

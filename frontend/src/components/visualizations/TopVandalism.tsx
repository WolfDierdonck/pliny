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
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';

const TopVandalism = ({ date }: { date: string }) => {
  const [vandalizedData, setVandalizedData] = useState<TopVandalismData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    getTopVandalismData(date, 10)
      .then((data) => {
        const formattedData = data
          .map((item) => ({
            ...item,
            page_name: item.page_name.replace(/_/g, ' '),
            abs_bytes_not_reverted:
              item.abs_bytes_changed - item.abs_bytes_reverted,
          }))
          .sort((a, b) => b.revert_count - a.revert_count);
        setVandalizedData(formattedData);
      })
      .catch((error) => {
        console.error('Failed to get data', error);
        setVandalizedData([]); // reset to default
      })
      .finally(() => setIsLoading(false));
  }, [date]);

  if (isLoading) {
    return <LoadingPlaceholder />;
  }
  if (!vandalizedData?.length) {
    return <NoDataPlaceholder />;
  }

  return (
    <ResponsiveContainer width="100%" height={500} style={{ padding: 20 }}>
      <BarChart data={vandalizedData}>
        <CartesianGrid />
        <XAxis dataKey="page_name" angle={-45} textAnchor="end" height={100} />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar
          dataKey="abs_bytes_not_reverted"
          stackId="a"
          fill="#00A86B"
          name="Non Vandalized Changes (bytes)"
        />
        <Bar
          dataKey="abs_bytes_reverted"
          stackId="a"
          fill="#FF6F61"
          name="Vandalized Changes (bytes)"
        />
      </BarChart>
    </ResponsiveContainer>
  );
};

export default TopVandalism;

import React, { useEffect, useState } from 'react';
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from 'recharts';
import { getTopEditsData, TopEditsData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';

const TopEdits = ({ date }: { date: string }) => {
  const [data, setData] = useState<TopEditsData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    getTopEditsData(date, 6)
      .then((data) => {
        const formattedData = data.map((item) => ({
          ...item,
          page_name: item.page_name.replace(/_/g, ' '),
        }));
        setData(formattedData);
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

  const renderRadarData = (item: TopEditsData) => [
    { metric: 'View Count', value: item.view_count },
    { metric: 'Edit Count', value: item.edit_count },
    { metric: 'Revert Count', value: item.revert_count },
    { metric: 'Editor Count', value: item.editor_count },
    { metric: 'Net Bytes Changed', value: item.net_bytes_changed },
    { metric: 'Abs Bytes Changed', value: item.abs_bytes_changed },
  ];

  return (
    <div className="p-6 bg-white rounded-lg shadow-sm">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {data.map((item, idx) => (
          <div key={idx} className="border p-4 rounded">
            <h3 className="text-lg font-medium mb-2">{item.page_name}</h3>
            <ResponsiveContainer width="100%" height={250}>
              <RadarChart data={renderRadarData(item)}>
                <PolarGrid />
                <PolarAngleAxis dataKey="metric" />
                <PolarRadiusAxis />
                <Radar
                  name={item.page_name}
                  dataKey="value"
                  stroke="#8884d8"
                  fill="#8884d8"
                  fillOpacity={0.6}
                />
              </RadarChart>
            </ResponsiveContainer>
            <div className="mt-2 text-sm">
              {renderRadarData(item).map((metricItem, i) => (
                <p key={i}>
                  <strong>{metricItem.metric}:</strong> {metricItem.value}
                </p>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TopEdits;

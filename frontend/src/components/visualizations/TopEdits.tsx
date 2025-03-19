'use client';
import React, { useEffect, useState } from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '../ui/shadcn/card';
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '../ui/shadcn/chart';

import { RadarChart, Radar, PolarGrid, PolarAngleAxis, Legend } from 'recharts';
import { TopEditsData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';
import { BackendData } from '../Home';
import { formatDateUTC } from '../../lib/utils';

const TopEdits = ({ backendData }: { backendData: BackendData }) => {
  const [data, setData] = useState<TopEditsData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    backendData.topEdits
      .then((data) => {
        setData(data);
      })
      .catch((error) => {
        console.error('Failed to get data', error);
        setData([]); // reset to default
      })
      .finally(() => setIsLoading(false));
  }, [backendData]);

  if (isLoading) {
    return <LoadingPlaceholder />;
  }
  if (!data?.length) {
    return <NoDataPlaceholder />;
  }

  // Get the top 5 most edited articles
  const top6Data = data.sort((a, b) => b.edit_count - a.edit_count).slice(0, 6);

  // For each article, get the rank of the statistic among the top 5
  const getRank = (item: TopEditsData, key: keyof TopEditsData) =>
    top6Data.filter((i) => i[key] > item[key]).length + 1;

  const getRawdataFromRank = (rank: number, key: keyof TopEditsData) =>
    top6Data
      .filter((item) => getRank(item, key) === rank)
      .map((item) => item[key]);

  const metricToProperty: { [key: string]: keyof TopEditsData } = {
    'Bytes Changed': 'abs_bytes_changed',
    Edits: 'edit_count',
    Views: 'view_count',
    'Bytes Grown': 'net_bytes_changed',
    Reverts: 'revert_count',
    Editors: 'editor_count',
  };

  const normalizedData = top6Data.map((item) => ({
    page_name: item.page_name,
    // get the rank of the statistic among the top 5
    view_count: top6Data.length - getRank(item, 'view_count'),
    edit_count: top6Data.length - getRank(item, 'edit_count'),
    revert_count: top6Data.length - getRank(item, 'revert_count'),
    editor_count: top6Data.length - getRank(item, 'editor_count'),
    net_bytes_changed: top6Data.length - getRank(item, 'net_bytes_changed'),
    abs_bytes_changed: top6Data.length - getRank(item, 'abs_bytes_changed'),
    // store the original values for the radar chart
    original_view_count: item.view_count,
    original_edit_count: item.edit_count,
    original_revert_count: item.revert_count,
    original_editor_count: item.editor_count,
    original_net_bytes_changed: item.net_bytes_changed,
    original_abs_bytes_changed: item.abs_bytes_changed,
  }));

  const radarData = [
    {
      metric: 'Bytes Changed',
      ...normalizedData.reduce(
        (acc, item) => ({ ...acc, [item.page_name]: item.abs_bytes_changed }),
        {},
      ),
    },
    {
      metric: 'Edits',
      ...normalizedData.reduce(
        (acc, item) => ({ ...acc, [item.page_name]: item.edit_count }),
        {},
      ),
    },
    {
      metric: 'Views',
      ...normalizedData.reduce(
        (acc, item) => ({ ...acc, [item.page_name]: item.view_count }),
        {},
      ),
    },
    {
      metric: 'Bytes Grown',
      ...normalizedData.reduce(
        (acc, item) => ({ ...acc, [item.page_name]: item.net_bytes_changed }),
        {},
      ),
    },
    {
      metric: 'Reverts',
      ...normalizedData.reduce(
        (acc, item) => ({ ...acc, [item.page_name]: item.revert_count }),
        {},
      ),
    },
    {
      metric: 'Editors',
      ...normalizedData.reduce(
        (acc, item) => ({ ...acc, [item.page_name]: item.editor_count }),
        {},
      ),
    },
  ];

  const colors = [
    '#B22222',
    '#A52A2A',
    '#CD5C5C',
    '#CD5C5B',
    '#E9967A',
    '#FA8072',
  ];

  const chartConfig: ChartConfig = top6Data.reduce(
    (
      acc: { [key: string]: { label: string; color: string } },
      article,
      idx,
    ) => {
      acc[article.page_name] = {
        label: article.page_name,
        color: idx === 0 ? '#ff7300' : colors[idx % colors.length],
      };
      return acc;
    },
    {} as { [key: string]: { label: string; color: string } },
  );

  const dataDate = new Date(backendData.date);
  const threeDaysAgo = new Date(dataDate);
  threeDaysAgo.setDate(dataDate.getDate() - 3);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Top Edited Pages</CardTitle>
        <CardDescription>
          {formatDateUTC(threeDaysAgo)} - {formatDateUTC(dataDate)}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="px-0 grid grid-cols-3 gap-4">
          {top6Data.map((item, idx) => (
            <ChartContainer
              config={chartConfig}
              key={item.page_name}
              className="w-full aspect-square"
            >
              <RadarChart data={radarData}>
                <ChartTooltip
                  cursor={false}
                  content={
                    <ChartTooltipContent
                      valueFn={(item) => {
                        console.log(
                          item,
                          getRawdataFromRank(
                            item.value as number,
                            metricToProperty[item.payload.metric],
                          ).toLocaleString(),
                        );
                        return getRawdataFromRank(
                          item.value as number,
                          metricToProperty[item.payload.metric],
                        ).toLocaleString();
                      }}
                    />
                  }
                />
                <PolarAngleAxis dataKey="metric" />
                <PolarGrid className="fill-red-500 opacity-10" />
                <Radar
                  name={item.page_name}
                  dataKey={item.page_name}
                  fill={colors[idx % colors.length]}
                  stroke={colors[idx % colors.length]}
                />
                <Legend align="center" iconSize={0} />
              </RadarChart>
            </ChartContainer>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default TopEdits;

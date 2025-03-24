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

import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  Legend,
  PolarRadiusAxis,
} from 'recharts';
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

  // Get the top 6 most edited articles
  const top6Data = data.sort((a, b) => b.edit_count - a.edit_count).slice(0, 6);

  // For each article, get the rank of the statistic among the top 6
  const getRank = (item: TopEditsData, key: keyof TopEditsData) =>
    top6Data.filter((i) => i[key] > item[key]).length;

  const getRawdataFromName = (page_name: string, key: keyof TopEditsData) =>
    top6Data.filter((item) => item.page_name === page_name)[0][key];

  const metricToProperty: { [key: string]: keyof TopEditsData } = {
    Change: 'abs_bytes_changed',
    Edits: 'edit_count',
    Views: 'view_count',
    Growth: 'net_bytes_changed',
    Reverts: 'revert_count',
    Editors: 'editor_count',
  };

  const normalizedData = top6Data.map((item) => ({
    page_name: item.page_name,
    // get the rank of the statistic among the top 6
    view_count: top6Data.length - getRank(item, 'view_count'),
    edit_count: top6Data.length - getRank(item, 'edit_count'),
    revert_count: top6Data.length - getRank(item, 'revert_count'),
    editor_count: top6Data.length - getRank(item, 'editor_count'),
    net_bytes_changed: top6Data.length - getRank(item, 'net_bytes_changed'),
    abs_bytes_changed: top6Data.length - getRank(item, 'abs_bytes_changed'),
  }));

  console.log(normalizedData);

  const colors = [
    '#B22222',
    '#A52A2A',
    '#CD5C5C',
    '#CD5C5B',
    '#E17564',
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
  const twoDaysAgo = new Date(dataDate);
  twoDaysAgo.setDate(dataDate.getDate() - 2);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Top Edited Pages</CardTitle>
        <CardDescription>
          {formatDateUTC(twoDaysAgo)} - {formatDateUTC(dataDate)}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="px-0 grid grid-cols-3 gap-10">
          {normalizedData.map((item, idx) => (
            <ChartContainer
              config={chartConfig}
              key={item.page_name}
              className="w-full aspect-square"
            >
              <RadarChart
                data={[
                  { metric: 'Views', val: item.view_count },
                  { metric: 'Edits', val: item.edit_count },
                  { metric: 'Reverts', val: item.revert_count },
                  { metric: 'Editors', val: item.editor_count },
                  { metric: 'Growth', val: item.net_bytes_changed },
                  { metric: 'Change', val: item.abs_bytes_changed },
                ]}
              >
                <PolarAngleAxis dataKey="metric" hide={true} axisLine={false} />
                <PolarRadiusAxis
                  domain={[0, 6]}
                  tickCount={7}
                  hide={true}
                  axisLine={false}
                  tick={false}
                />
                <PolarGrid className="fill-red-500 opacity-10" />
                <Radar
                  name={item.page_name}
                  dataKey="val"
                  fill={colors[idx % colors.length]}
                  stroke={colors[idx % colors.length]}
                  fillOpacity={0.85}
                  strokeOpacity={0}
                />
                <Legend
                  align="center"
                  iconSize={0}
                  wrapperStyle={{
                    fontSize: '14px', // Adjust the font size
                    fontWeight: 'bold', // Make the text bold
                    paddingTop: '20px', // Add top padding
                  }}
                />
                <ChartTooltip
                  cursor={false}
                  content={
                    <ChartTooltipContent
                      valueFn={(tooltipItem) => {
                        return getRawdataFromName(
                          item.page_name,
                          metricToProperty[tooltipItem.payload.metric],
                        ).toLocaleString();
                      }}
                    />
                  }
                />
              </RadarChart>
            </ChartContainer>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default TopEdits;

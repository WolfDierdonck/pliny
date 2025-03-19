'use client';

import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Legend } from 'recharts';

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
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from '../ui/shadcn/chart';

import { TopVandalismData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';
import { BackendData } from '../Home';
import { formatDateUTC } from '../../lib/utils';

const TopVandalism = ({ backendData }: { backendData: BackendData }) => {
  const [vandalizedData, setVandalizedData] = useState<TopVandalismData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    backendData.topVandalism
      .then((data) => {
        const formattedData = data
          .map((item) => ({
            ...item,
            page_name: item.page_name,
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
  }, [backendData]);

  if (isLoading) {
    return <LoadingPlaceholder />;
  }
  if (!vandalizedData?.length) {
    return <NoDataPlaceholder />;
  }

  const chartConfig: ChartConfig = {
    abs_bytes_reverted: {
      label: 'Volume of vandalised changes (bytes)',
      color: '#882525',
    },
    abs_bytes_not_reverted: {
      label: 'Volume of non-vandalised changes (bytes)',
      color: '#E17564',
    },
    revert_count: {
      label: 'Number of reverts',
      color: '#000',
    },
    label: {
      color: '#fff',
    },
  } satisfies ChartConfig;

  const dataDate = new Date(backendData.date);
  const threeDaysAgo = new Date(dataDate);
  threeDaysAgo.setDate(dataDate.getDate() - 3);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Most Vandalized Articles</CardTitle>
        <CardDescription>
          {formatDateUTC(threeDaysAgo)} - {formatDateUTC(dataDate)}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <BarChart
            // accessibilityLayer
            data={vandalizedData}
            layout="vertical"
            // margin={{
            //   right: 16,
            //   left: 16,
            // }}
          >
            <CartesianGrid horizontal={false} />
            <YAxis
              dataKey="page_name"
              type="category"
              tickLine={false}
              tickMargin={10}
              axisLine={false}
              width={200}
              // tickFormatter={(value) => value.slice(0, 3)}
              // hide
            />
            <XAxis
              type="number"
              tickLine={false}
              tickMargin={10}
              axisLine={false}
              // tickFormatter={(value) => value.slice(0, 3)}
              hide
            />
            <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
            <Legend
              content={<ChartLegendContent />}
              align="center"
              layout="vertical"
            />
            <Bar
              dataKey="abs_bytes_reverted"
              stackId="a"
              fill="#882525"
              radius={[4, 4, 4, 4]}
            >
              {/* <LabelList
                dataKey="revert_count"
                position="left"
                offset={30}
                fill="#000"
                fontSize={12}
              /> */}
            </Bar>
            <Bar
              dataKey="abs_bytes_not_reverted"
              stackId="a"
              fill="#E17564"
              radius={[4, 4, 4, 4]}
            />
            {/* <Bar
              dataKey="revert_count"
              stackId="a"
              fill="000"
              radius={[4, 4, 4, 4]}
              hide={true}
            /> */}
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
};

export default TopVandalism;

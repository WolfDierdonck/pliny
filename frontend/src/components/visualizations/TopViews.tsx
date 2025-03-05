import React, { useEffect, useState } from 'react';
import { getTopViewsData, TopViewsData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';

('use client');

import { TrendingUp } from 'lucide-react';
import { Area, AreaChart, CartesianGrid, XAxis } from 'recharts';

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '../ui/shadcn/card';
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '../ui/shadcn/chart';

const TopViews = ({ date }: { date: string }) => {
  const [viewData, setViewData] = useState<TopViewsData[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    getTopViewsData(date, 10)
      .then((data) => {
        setViewData(data);
        const transformed = Array.from({ length: 7 }, (_, dayOffset) => {
          const dateObj = new Date(date);
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
      .catch((error) => {
        console.error('Failed to get data', error);
        setViewData([]); // reset to default
        setChartData([]); // reset to default
      })
      .finally(() => setIsLoading(false));
  }, [date]);

  if (isLoading) {
    return <LoadingPlaceholder />;
  }
  if (!viewData?.length) {
    return <NoDataPlaceholder />;
  }

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

  const chartConfig: ChartConfig = viewData.reduce(
    (
      acc: { [key: string]: { label: string; color: string } },
      article,
      idx,
    ) => {
      acc[article.page_name] = {
        label: article.page_name.replace(/_/g, ' '),
        color: colors[idx % colors.length],
      };
      return acc;
    },
    {},
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle>Area Chart - Stacked</CardTitle>
        <CardDescription>
          Showing total visitors for the last 6 months
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <AreaChart
            accessibilityLayer
            data={chartData}
            margin={{
              left: 12,
              right: 12,
            }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="day"
              tickLine={false}
              axisLine={false}
              tickMargin={15}
              // tickFormatter={(value) => value.slice(0, 3)}
            />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent />}
              defaultIndex={1}
            />
            {viewData.map((article, idx) => (
              <Area
                key={article.page_name}
                type="monotone"
                dataKey={article.page_name}
                stroke={colors[idx % colors.length]}
                // dot={<CustomDot />}
                // type="natural"
                fill={chartConfig[article.page_name].color}
                fillOpacity={0.5}
                strokeOpacity={0.5}
                //stackId="a"
              />
            ))}
          </AreaChart>
        </ChartContainer>
      </CardContent>
      <CardFooter>
        <div className="flex w-full items-start gap-2 text-sm">
          <div className="grid gap-2">
            <div className="flex items-center gap-2 font-medium leading-none">
              Trending up by 5.2% this month <TrendingUp className="h-4 w-4" />
            </div>
            <div className="flex items-center gap-2 leading-none text-muted-foreground">
              January - June 2024
            </div>
          </div>
        </div>
      </CardFooter>
    </Card>
  );
};

export default TopViews;

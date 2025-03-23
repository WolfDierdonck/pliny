import React, { useEffect, useState } from 'react';
import { TopViewsData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';

('use client');

import { Area, AreaChart, CartesianGrid, LabelList, XAxis } from 'recharts';

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
import { BackendData } from '../Home';
import { formatDateUTC } from '../../lib/utils';

const TopViews = ({ backendData }: { backendData: BackendData }) => {
  const [viewData, setViewData] = useState<TopViewsData[]>([]);
  const [chartData, setChartData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [highlighted, setHighlighted] = useState<string | null>(null);

  useEffect(() => {
    setIsLoading(true);
    backendData.topViews
      .then((data) => {
        data = data.slice(0, 6);
        setViewData(data);
        const transformed = Array.from({ length: 7 }, (_, dayOffset) => {
          const dateObj = new Date(backendData.date);
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
  }, [backendData]);

  if (isLoading) {
    return <LoadingPlaceholder />;
  }
  if (!viewData?.length) {
    return <NoDataPlaceholder />;
  }

  const colors = [
    '#FF6347',
    '#E76637',
    '#FF7F50',
    '#CD5C5C',
    '#B22222',
    '#800000',
    '#8B4513',
    '#A52A2A',
    '#E9967A',
    '#FA8072',
  ];

  // const CustomDot = (props: any) => {
  //   const { cx, cy, stroke, index } = props;
  //   if (chartData.length && index === chartData.length - 1) {
  //     return <circle cx={cx} cy={cy} r={5} stroke={stroke} fill={stroke} />;
  //   }
  //   return null;
  // };

  const dateObj = new Date(backendData.date);
  const sevenDaysAgo = new Date(dateObj);
  sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 6);

  const chartConfig: ChartConfig = viewData.reduce(
    (
      acc: { [key: string]: { label: string; color: string } },
      article,
      idx,
    ) => {
      acc[article.page_name] = {
        label: article.page_name,
        color: colors[idx % colors.length],
      };
      return acc;
    },
    {},
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle>Most Viewed Articles</CardTitle>
        <CardDescription>
          {formatDateUTC(sevenDaysAgo)} - {formatDateUTC(dateObj)}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <AreaChart
            accessibilityLayer
            data={chartData}
            margin={{
              left: 40,
              right: 40,
              top: 20,
              bottom: 20,
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
              offset={100}
            />
            {viewData.map((article, idx) => (
              <Area
                key={article.page_name}
                type="monotone"
                dataKey={article.page_name}
                stroke={colors[idx % colors.length]}
                fill={chartConfig[article.page_name].color}
                strokeOpacity={0}
                fillOpacity={highlighted === article.page_name ? 0.85 : 0.5}
                // onClick={() =>
                //   setHighlighted((prev) =>
                //     prev === article.page_name ? null : article.page_name,
                //   )
                // }
                onMouseEnter={() => setHighlighted(article.page_name)}
                onMouseLeave={() => setHighlighted(null)}
                connectNulls={true}
                // stackId="a"
              >
                <LabelList
                  dataKey={article.page_name}
                  position="top"
                  offset={8}
                  fill="#000"
                  fillOpacity={highlighted === article.page_name ? 1 : 0}
                  fontSize={12}
                />
              </Area>
            ))}
          </AreaChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex justify-center items-center">
        <p className="text-center text-xl font-semibold p-3">{highlighted}</p>
      </CardFooter>
    </Card>
  );
};

export default TopViews;

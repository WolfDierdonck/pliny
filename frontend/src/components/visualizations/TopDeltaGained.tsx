import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  CartesianGrid,
  YAxis,
  XAxis,
  LabelList,
} from 'recharts';
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
import { TopViewsGainedData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';
import { BackendData } from '../Home';
import { formatDateUTC } from '../../lib/utils';

// Replace the single colors array with separate arrays for gains and losses
export const colors = [
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

const TopDeltaGained = ({ backendData }: { backendData: BackendData }) => {
  const [gainedArticles, setGainedArticles] = useState<TopViewsGainedData[]>(
    [],
  );
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [chartData, setChartData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [highlighted, setHighlighted] = useState<string | null>(null);

  useEffect(() => {
    setIsLoading(true);
    backendData.topViewsGained
      .then((gainedData) => {
        setGainedArticles(
          gainedData
            .slice(0, 5)
            .sort((a, b) => b.current_view_count - a.current_view_count),
        );
        const days: { day: string; [key: string]: number | string }[] = [
          { day: '2 Days Ago' },
          { day: 'Yesterday' },
          { day: 'Today' },
        ];
        gainedData.forEach((article) => {
          days[2][article.page_name] = article.current_view_count; // Yesterday baseline
          days[1][article.page_name] = article.one_day_ago_view_count || 0;
          days[0][article.page_name] = article.two_days_ago_view_count || 0;
        });
        setChartData(days);
      })
      .catch((error) => {
        console.error('Failed to get data', error);
        setGainedArticles([]);
        setChartData([]);
      })
      .finally(() => setIsLoading(false));
  }, [backendData]);

  if (isLoading) {
    return <LoadingPlaceholder />;
  }
  if (!gainedArticles?.length) {
    return <NoDataPlaceholder />;
  }

  const chartConfig: ChartConfig = chartData.reduce(
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

  const dataDate = new Date(backendData.date);
  const twoDaysAgo = new Date(dataDate);
  twoDaysAgo.setDate(dataDate.getDate() - 2);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Trending Articles (Gained Views)</CardTitle>
        <CardDescription>
          {formatDateUTC(twoDaysAgo)} - {formatDateUTC(dataDate)}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <LineChart
            accessibilityLayer
            data={chartData}
            margin={{
              right: 40,
              left: 40,
              top: 25,
              bottom: 25,
            }}
          >
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent />}
              defaultIndex={1}
              offset={100}
            />
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="day"
              tickLine={false}
              axisLine={false}
              tickMargin={15}
              // tickFormatter={(value) => value.slice(0, 3)}
            />
            <YAxis type="number" tickLine={false} axisLine={false} hide />
            {gainedArticles.map((article, index) => (
              <Line
                key={article.page_name}
                type="monotone"
                dataKey={article.page_name}
                name={article.page_name}
                stroke={colors[index % colors.length]}
                strokeOpacity={highlighted === article.page_name ? 0.7 : 0.4}
                connectNulls={true}
                strokeWidth={15}
                strokeLinecap="round"
                dot={false}
                onMouseEnter={() => setHighlighted(article.page_name)}
                onMouseLeave={() => setHighlighted(null)}
              >
                <LabelList
                  dataKey={article.page_name}
                  position="top"
                  offset={8}
                  fill="#000"
                  fillOpacity={highlighted === article.page_name ? 1 : 0}
                  fontSize={12}
                  onMouseEnter={() => null}
                  onMouseLeave={() => null}
                />
              </Line>
            ))}
          </LineChart>
        </ChartContainer>
      </CardContent>
      <CardFooter className="flex justify-center items-center">
        <p className="text-center text-xl font-semibold p-3">
          {highlighted || 'No Page Selected'}
        </p>
      </CardFooter>
    </Card>
  );
};

export default TopDeltaGained;

import React, { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  LabelList,
} from 'recharts';
import { TopEditorsData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';
import { BackendData } from '../Home';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '../ui/shadcn/card';
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
  ChartConfig,
} from '../ui/shadcn/chart';
import { formatDateUTC } from '../../lib/utils';

const TopEditors = ({ backendData }: { backendData: BackendData }) => {
  const [data, setData] = useState<TopEditorsData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    backendData.topEditors
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

  const chartConfig: ChartConfig = {
    editor_count: {
      label: 'Unique Editors',
      color: '#D17463',
    },
  } satisfies ChartConfig;

  const dataDate = new Date(backendData.date);
  const twoDaysAgo = new Date(dataDate);
  twoDaysAgo.setDate(dataDate.getDate() - 2);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Top pages by unique editors</CardTitle>
        <CardDescription>
          {formatDateUTC(twoDaysAgo)} - {formatDateUTC(dataDate)}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <BarChart
            // accessibilityLayer
            data={data}
            layout="vertical"
            margin={{
              right: 16,
            }}
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
            <Bar dataKey="editor_count" fill="#D17463" radius={[2, 2, 2, 2]}>
              <LabelList
                dataKey="editor_count"
                position="right"
                offset={8}
                fill="#000"
                fontSize={12}
              />
            </Bar>
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
};

export default TopEditors;

{
  /* <div className="p-6 bg-white rounded-lg shadow-sm">
  <h2 className="text-xl font-semibold text-gray-800 mb-4">
    Articles by Unique Editors
  </h2>
  <ResponsiveContainer width="100%" height={500}>
    <BarChart data={data} margin={{ top: 20, right: 20, bottom: 70, left: 60 }}>
      <XAxis
        dataKey="page_name"
        angle={-45}
        textAnchor="end"
        height={100}
        interval={0}
      />
      <YAxis
        label={{
          value: 'Number of Unique Editors',
          angle: -90,
          position: 'insideLeft',
        }}
      />
      <Tooltip content={<CustomTooltip />} />
      <Bar dataKey="editor_count" fill="#8884d8" fillOpacity={0.6} />
    </BarChart>
  </ResponsiveContainer>
</div>; */
}

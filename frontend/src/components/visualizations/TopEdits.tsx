// import React, { useEffect, useState } from 'react';
// import {
//   RadarChart,
//   Radar,
//   PolarGrid,
//   PolarAngleAxis,
//   PolarRadiusAxis,
//   ResponsiveContainer,
// } from 'recharts';
// import { TopEditsData } from '../../lib/api';
// import LoadingPlaceholder from '../LoadingPlaceholder';
// import NoDataPlaceholder from '../NoDataPlaceholder';
// import { BackendData } from '../Home';

// const TopEdits = ({ backendData }: { backendData: BackendData }) => {
//   const [data, setData] = useState<TopEditsData[]>([]);
//   const [isLoading, setIsLoading] = useState(true);

//   useEffect(() => {
//     setIsLoading(true);
//     backendData.topEdits
//       .then((data) => {
//         setData(data);
//       })
//       .catch((error) => {
//         console.error('Failed to get data', error);
//         setData([]); // reset to default
//       })
//       .finally(() => setIsLoading(false));
//   }, [backendData]);

//   if (isLoading) {
//     return <LoadingPlaceholder />;
//   }
//   if (!data?.length) {
//     return <NoDataPlaceholder />;
//   }

//   // Get the top 5 most edited articles
//   const top5Data = data.sort((a, b) => b.edit_count - a.edit_count).slice(0, 5);

//   // Find the max values for each metric
//   const maxValues = {
//     view_count: Math.max(...top5Data.map((item) => item.view_count)),
//     edit_count: Math.max(...top5Data.map((item) => item.edit_count)),
//     revert_count: Math.max(...top5Data.map((item) => item.revert_count)),
//     editor_count: Math.max(...top5Data.map((item) => item.editor_count)),
//     net_bytes_changed: Math.max(
//       ...top5Data.map((item) => item.net_bytes_changed),
//     ),
//     abs_bytes_changed: Math.max(
//       ...top5Data.map((item) => item.abs_bytes_changed),
//     ),
//   };

//   // Normalize the data
//   const normalizedData = top5Data.map((item) => ({
//     page_name: item.page_name,
//     view_count: (item.view_count / maxValues.view_count) * 100,
//     edit_count: (item.edit_count / maxValues.edit_count) * 100,
//     revert_count: (item.revert_count / maxValues.revert_count) * 100,
//     editor_count: (item.editor_count / maxValues.editor_count) * 100,
//     net_bytes_changed:
//       (item.net_bytes_changed / maxValues.net_bytes_changed) * 100,
//     abs_bytes_changed:
//       (item.abs_bytes_changed / maxValues.abs_bytes_changed) * 100,
//   }));

//   const radarData = [
//     {
//       metric: 'View Count',
//       ...normalizedData.reduce(
//         (acc, item) => ({ ...acc, [item.page_name]: item.view_count }),
//         {},
//       ),
//     },
//     {
//       metric: 'Edit Count',
//       ...normalizedData.reduce(
//         (acc, item) => ({ ...acc, [item.page_name]: item.edit_count }),
//         {},
//       ),
//     },
//     {
//       metric: 'Revert Count',
//       ...normalizedData.reduce(
//         (acc, item) => ({ ...acc, [item.page_name]: item.revert_count }),
//         {},
//       ),
//     },
//     {
//       metric: 'Editor Count',
//       ...normalizedData.reduce(
//         (acc, item) => ({ ...acc, [item.page_name]: item.editor_count }),
//         {},
//       ),
//     },
//     {
//       metric: 'Net Bytes Changed',
//       ...normalizedData.reduce(
//         (acc, item) => ({ ...acc, [item.page_name]: item.net_bytes_changed }),
//         {},
//       ),
//     },
//     {
//       metric: 'Abs Bytes Changed',
//       ...normalizedData.reduce(
//         (acc, item) => ({ ...acc, [item.page_name]: item.abs_bytes_changed }),
//         {},
//       ),
//     },
//   ];

//   return (
//     <div className="p-6 bg-white rounded-lg shadow-sm">
//       <ResponsiveContainer width="100%" height={500}>
//         <RadarChart data={radarData}>
//           <PolarGrid />
//           <PolarAngleAxis dataKey="metric" />
//           <PolarRadiusAxis />
//           {top5Data.map((item, idx) => (
//             <Radar
//               key={idx}
//               name={item.page_name}
//               dataKey={item.page_name}
//               stroke="#8884d8"
//               fill="#8884d8"
//               fillOpacity={0.6}
//             />
//           ))}
//         </RadarChart>
//       </ResponsiveContainer>
//     </div>
//   );
// };

// export default TopEdits;

'use client';
import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/shadcn/card';
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '../ui/shadcn/chart';

import { RadarChart, Radar, PolarGrid, PolarAngleAxis } from 'recharts';
import { TopEditsData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';
import { BackendData } from '../Home';

const TopEdits = ({ backendData }: { backendData: BackendData }) => {
  const [data, setData] = useState<TopEditsData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [highlighted, setHighlighted] = useState<string | null>(null);

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

  // Find the max values for each metric
  const maxValues = {
    view_count: Math.max(...top6Data.map((item) => item.view_count)),
    edit_count: Math.max(...top6Data.map((item) => item.edit_count)),
    revert_count: Math.max(...top6Data.map((item) => item.revert_count)),
    editor_count: Math.max(...top6Data.map((item) => item.editor_count)),
    net_bytes_changed: Math.max(
      ...top6Data.map((item) => item.net_bytes_changed),
    ),
    abs_bytes_changed: Math.max(
      ...top6Data.map((item) => item.abs_bytes_changed),
    ),
  };

  // Normalize the data
  const normalizedData = top6Data.map((item) => ({
    page_name: item.page_name,
    view_count: (item.view_count / maxValues.view_count) * 100,
    edit_count: (item.edit_count / maxValues.edit_count) * 100,
    revert_count: (item.revert_count / maxValues.revert_count) * 100,
    editor_count: (item.editor_count / maxValues.editor_count) * 100,
    net_bytes_changed:
      (item.net_bytes_changed / maxValues.net_bytes_changed) * 100,
    abs_bytes_changed:
      (item.abs_bytes_changed / maxValues.abs_bytes_changed) * 100,
    original_view_count: item.view_count,
    original_edit_count: item.edit_count,
    original_revert_count: item.revert_count,
    original_editor_count: item.editor_count,
    original_net_bytes_changed: item.net_bytes_changed,
    original_abs_bytes_changed: item.abs_bytes_changed,
  }));

  const radarData = [
    {
      metric: 'View Count',
      ...normalizedData.reduce(
        (acc, item) => ({ ...acc, [item.page_name]: item.view_count }),
        {},
      ),
    },
    {
      metric: 'Edit Count',
      ...normalizedData.reduce(
        (acc, item) => ({ ...acc, [item.page_name]: item.edit_count }),
        {},
      ),
    },
    {
      metric: 'Revert Count',
      ...normalizedData.reduce(
        (acc, item) => ({ ...acc, [item.page_name]: item.revert_count }),
        {},
      ),
    },
    {
      metric: 'Editor Count',
      ...normalizedData.reduce(
        (acc, item) => ({ ...acc, [item.page_name]: item.editor_count }),
        {},
      ),
    },
    {
      metric: 'Net Bytes Changed',
      ...normalizedData.reduce(
        (acc, item) => ({ ...acc, [item.page_name]: item.net_bytes_changed }),
        {},
      ),
    },
    {
      metric: 'Abs Bytes Changed',
      ...normalizedData.reduce(
        (acc, item) => ({ ...acc, [item.page_name]: item.abs_bytes_changed }),
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

  return (
    <div className="px-0 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-10 ">
      {top6Data.map((item, idx) => (
        <Card key={idx}>
          <CardHeader className="items-center pb-4">
            <CardTitle className="text-center">{item.page_name}</CardTitle>
          </CardHeader>
          <CardContent className="flex justify-center items-center">
            <ChartContainer
              config={chartConfig}
              className=" px-10 mx-auto aspect-square w-[300px] h-[300px] "
            >
              <RadarChart data={radarData}>
                <ChartTooltip
                  cursor={false}
                  content={<ChartTooltipContent />}
                />
                <PolarAngleAxis dataKey="metric" />
                <PolarGrid className="fill-red-500 opacity-10" />
                <Radar
                  name={item.page_name}
                  dataKey={item.page_name}
                  fill={colors[idx % colors.length]}
                  fillOpacity={highlighted === item.page_name ? 1 : 0.8}
                  stroke={colors[idx % colors.length]}
                  onMouseEnter={() => setHighlighted(item.page_name)}
                  onMouseLeave={() => setHighlighted(null)}
                />
              </RadarChart>
            </ChartContainer>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default TopEdits;

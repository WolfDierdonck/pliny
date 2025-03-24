import React, { useEffect, useState } from 'react';
import { WikipediaStatsData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';
import { BackendData } from '../Home';

import {
  Card,
  CardContent,
  // CardDescription,
  // CardFooter,
  CardHeader,
  CardTitle,
} from '../ui/shadcn/card';

const WikipediaStats = ({ backendData }: { backendData: BackendData }) => {
  const [stats, setStats] = useState<WikipediaStatsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    backendData.wikipediaStats
      .then((statsData) => setStats(statsData))
      .catch((error) => console.error('Failed to get data', error))
      .finally(() => setIsLoading(false));
  }, [backendData]);

  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`;
    }
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}K`;
    }
    return num.toString();
  };

  const formatBytes = (bytes: number) => {
    const isNegative = bytes < 0;
    const absBytes = Math.abs(bytes);
    let formatted: string;

    if (absBytes >= 1000000) {
      formatted = `${(absBytes / 1000000).toFixed(1)}MB`;
    } else if (absBytes >= 1000) {
      formatted = `${(absBytes / 1000).toFixed(1)}KB`;
    } else {
      formatted = `${absBytes}B`;
    }

    return isNegative ? `-${formatted}` : `+${formatted}`;
  };
  if (isLoading) {
    return <LoadingPlaceholder />;
  }
  if (!stats) {
    return <NoDataPlaceholder />;
  }

  const statsConfig = [
    {
      label: 'Total Views',
      value: stats.total_view_count,
      icon: '👁️',
      color: 'text-orange-700',
      format: formatNumber,
    },
    {
      label: 'Total Edits',
      value: stats.total_edit_count,
      icon: '✏️',
      color: 'text-red-700',
      format: formatNumber,
    },
    {
      label: 'Unique Editors',
      value: stats.total_editor_count,
      icon: '👥',
      color: 'text-amber-600',
      format: formatNumber,
    },
    {
      label: 'Reverted Edits',
      value: stats.total_revert_count,
      icon: '↩️',
      color: 'text-red-900/80',
      format: formatNumber,
    },
    {
      label: 'Net Growth',
      value: stats.total_net_bytes_changed,
      icon: '📈',
      color: 'text-rose-700',
      format: formatBytes,
    },
  ];

  return (
    <div className="flex gap-x-20 gap-y-10 p-6 justify-center items-center align-center flex-wrap py-10">
      {statsConfig.map((stat) => (
        <Card
          key={stat.label}
          className={`transition-transform hover:scale-105 bg-stone-100/40 ${stat.color} shadow-md`} //${stat.color} rounded-lg shadow-sm p-6 transition-transform
        >
          <CardHeader className="flex items-center">
            <CardTitle>{stat.label}</CardTitle>
          </CardHeader>
          <CardContent className="flex justify-center items-center px-16">
            <div className="text-3xl font-bold">{stat.format(stat.value)}</div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default WikipediaStats;

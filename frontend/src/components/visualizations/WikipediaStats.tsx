import React, { useEffect, useState } from 'react';
import { getTotalMetadata, WikipediaStatsData } from '../../lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';

const WikipediaStats = ({ date }: { date: string }) => {
  const [stats, setStats] = useState<WikipediaStatsData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    getTotalMetadata(date)
      .then((statsData) => setStats(statsData))
      .catch((error) => console.error('Failed to get data', error))
      .finally(() => setIsLoading(false));
  }, [date]);

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
  console.log('isLoading', isLoading, 'stats', stats);
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
      color: 'bg-blue-50 text-blue-700',
      format: formatNumber,
    },
    {
      label: 'Total Edits',
      value: stats.total_edit_count,
      icon: '✏️',
      color: 'bg-green-50 text-green-700',
      format: formatNumber,
    },
    {
      label: 'Unique Editors',
      value: stats.total_editor_count,
      icon: '👥',
      color: 'bg-purple-50 text-purple-700',
      format: formatNumber,
    },
    {
      label: 'Reverted Edits',
      value: stats.total_revert_count,
      icon: '↩️',
      color: 'bg-red-50 text-red-700',
      format: formatNumber,
    },
    {
      label: 'Net Growth',
      value: stats.total_net_bytes_changed,
      icon: '📈',
      color: 'bg-indigo-50 text-indigo-700',
      format: formatBytes,
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 p-6">
      {statsConfig.map((stat) => (
        <div
          key={stat.label}
          className={`${stat.color} rounded-lg shadow-sm p-6 transition-transform hover:scale-105`}
        >
          <div className="flex items-center mb-2">
            <span className="text-2xl mr-2">{stat.icon}</span>
            <h3 className="text-lg font-medium">{stat.label}</h3>
          </div>
          <div className="text-3xl font-bold">{stat.format(stat.value)}</div>
        </div>
      ))}
    </div>
  );
};

export default WikipediaStats;

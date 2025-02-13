import React, { useEffect, useState } from 'react';
import {
  getTotalMetadata,
  getWikipediaGrowth,
  WikipediaStatsData,
  WikipediaGrowthData,
} from '../../lib/api';

const WikipediaStats = () => {
  const [stats, setStats] = useState<WikipediaStatsData | null>(null);
  const [growth, setGrowth] = useState<WikipediaGrowthData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    Promise.all([
      getTotalMetadata('2024-09-01'),
      getWikipediaGrowth('2024-09-01'),
    ])
      .then(([statsData, growthData]) => {
        setStats(statsData);
        setGrowth(growthData);
      })
      .catch((error) => console.error('Failed to get data', error))
      .finally(() => setIsLoading(false));
  }, []);

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

  if (isLoading || !stats || !growth) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 p-6">
        {[...Array(5)].map((_, i) => (
          <div
            key={i}
            className="animate-pulse bg-white rounded-lg shadow-sm p-6"
          >
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
            <div className="h-8 bg-gray-200 rounded w-3/4"></div>
          </div>
        ))}
      </div>
    );
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
      value: growth.wikipedia_growth_bytes,
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

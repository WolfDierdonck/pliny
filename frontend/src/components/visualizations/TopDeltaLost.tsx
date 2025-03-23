import React, { useEffect, useState } from 'react';

import { BackendData } from '../Home';
import { TopViewsLostData } from '@/src/lib/api';
import LoadingPlaceholder from '../LoadingPlaceholder';
import NoDataPlaceholder from '../NoDataPlaceholder';

const TopDeltaLost = ({ backendData }: { backendData: BackendData }) => {
  const [lostArticles, setLostArticles] = useState<TopViewsLostData[]>([]);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    backendData.topViewsLost
      .then((lostData) => {
        setLostArticles(lostData.slice(0, 5));
      })
      .catch((error) => {
        console.error('Failed to get data', error);
        setLostArticles([]);
      })
      .finally(() => setIsLoading(false));
  }, [backendData]);

  if (isLoading) {
    return <LoadingPlaceholder />;
  }
  if (!lostArticles?.length) {
    return <NoDataPlaceholder />;
  }

  return (
    <div>
      <h2>Top Lost Articles</h2>
    </div>
  );
};

export default TopDeltaLost;

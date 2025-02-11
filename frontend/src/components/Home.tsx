import React, { useEffect, useState } from 'react';
import {
  getTopVandalismData,
  getTopViewsData,
  TopVandalismData,
  TopViewsData,
} from '../lib/api';

const Home = () => {
  const [viewData, setViewData] = useState<TopViewsData[]>([]);
  const [vandalismData, setVandalismData] = useState<TopVandalismData[]>([]);

  useEffect(() => {
    getTopViewsData('2024-09-01', 10)
      .then((data) => {
        setViewData(data);
      })
      .catch((error) => {
        console.error('Failed to get data', error);
      });
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">
        Welcome to the Data Visualization Website
      </h1>
      <p className="mt-4">
        This website provides different visualizations based on the data queried
        from our backend.
      </p>

      <p className="mt-4 font-bold">The view data from BigQuery is:</p>
      <ul>
        {viewData.map((item: TopViewsData) => (
          <li key={item.page_name}>
            {item.page_name}: {item.view_count}
          </li>
        ))}
      </ul>

      <p className="mt-4 font-bold">The vandalism data from BigQuery is:</p>
      <ul>
        {vandalismData.map((item: TopVandalismData) => (
          <li key={item.page_name}>
            {item.page_name}: {item.percent_reverted}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Home;

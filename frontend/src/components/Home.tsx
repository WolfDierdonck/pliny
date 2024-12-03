import React, { useEffect, useState } from 'react';
import { getTopViewsData, TopViewsData } from '../lib/api';

const Home = () => {
  const [viewData, setViewData] = useState<TopViewsData[]>([]);

  useEffect(() => {
    getTopViewsData().then((data) => {
      setViewData(data);
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

      <p>The data from BigQuery is:</p>
      <ul>
        {viewData.map((item) => (
          <li key={item.article}>
            {item.article}: {item.views}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Home;

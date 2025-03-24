import React, { useEffect, useState } from 'react';
import '../styles/Home.css';
import TopViews from './visualizations/TopViews';
import TopVandalism from './visualizations/TopVandalism';
import TopGrowingArticles from './visualizations/TopGrowingArticles';
import TopEditors from './visualizations/TopEditors';
import TopEdits from './visualizations/TopEdits';
import WikipediaStats from './visualizations/WikipediaStats';
import TopDeltaGained from './visualizations/TopDeltaGained';
import TopDeltaLost from './visualizations/TopDeltaLost';
import {
  getTopEditorsData,
  getTopEditsData,
  getTopGrowingData,
  getTopShrinkingData,
  getTopVandalismData,
  getTopViewsData,
  getTopViewsGainedData,
  getTopViewsLostData,
  getTotalMetadata,
  TopEditorsData,
  TopEditsData,
  TopGrowingData,
  TopShrinkingData,
  TopVandalismData,
  TopViewsData,
  TopViewsGainedData,
  TopViewsLostData,
  WikipediaStatsData,
} from '../lib/api';

export type BackendData = {
  date: string;
  topEditors: Promise<TopEditorsData[]>;
  topEdits: Promise<TopEditsData[]>;
  topGrowing: Promise<TopGrowingData[]>;
  topShrinking: Promise<TopShrinkingData[]>;
  topVandalism: Promise<TopVandalismData[]>;
  topViewsGained: Promise<TopViewsGainedData[]>;
  topViewsLost: Promise<TopViewsLostData[]>;
  topViews: Promise<TopViewsData[]>;
  wikipediaStats: Promise<WikipediaStatsData | null>;
};

const getBackendData = (date: string, limit: number): BackendData => {
  return {
    date: date,
    topEditors: getTopEditorsData(date, limit),
    topEdits: getTopEditsData(date, limit),
    topGrowing: getTopGrowingData(date, limit),
    topShrinking: getTopShrinkingData(date, limit),
    topVandalism: getTopVandalismData(date, limit),
    topViewsGained: getTopViewsGainedData(date, limit),
    topViewsLost: getTopViewsLostData(date, limit),
    topViews: getTopViewsData(date, limit),
    wikipediaStats: getTotalMetadata(date),
  };
};

const Home = () => {
  const now = new Date();
  const two_days_ago = new Date(now);
  two_days_ago.setDate(now.getDate() - 2);
  const latest_available_date_str = two_days_ago
    .toLocaleDateString('en-CA', {
      timeZone: 'America/New_York',
    })
    .split('/')
    .reverse()
    .join('-');

  const [typingDate, setTypingDate] = useState(latest_available_date_str);
  const [date, setDate] = useState(latest_available_date_str);
  const [backendData, setBackendData] = useState<BackendData>(
    getBackendData(date, 10),
  );

  useEffect(() => {
    if (backendData.date !== date) {
      setBackendData(getBackendData(date, 10));
    }
  }, [date]);

  return (
    <div className="home-container">
      <header className="home-header">
        <input
          type="date"
          value={typingDate}
          onChange={(e) => {
            setTypingDate(e.target.value);
            // its a real date
            if (e.target.value && !isNaN(new Date(e.target.value).getTime())) {
              setDate(e.target.value);
            }
          }}
          className="bg-[#ffebe3] text-black accent-[#ed856bb3] p-3 shadow-md rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#ed856b] focus:border-[#ed856b]"
          min="2023-01-01"
          max={latest_available_date_str}
        />
      </header>
      <main className="home-main">
        <section className="home-section">
          <img
            src={`${process.env.PUBLIC_URL}/assets/pliny.png`}
            alt="Pliny logo"
            className="home-logo banner"
          />
          <p className="home-splash-text">
            Welcome to Pliny! Here you can explore the patterns and trends in
            Wikipedia metadata. Customize the date you're looking at in the top
            left and scroll to get started.
          </p>
        </section>
        <section className="home-section">
          <p className="home-description">
            Wikipedia is the largest and most comprehensive source of
            information in the world. Unlike the encyclopedias of the past,
            Wikipedia is a living document that is constantly updated by
            volunteers from around the world. This project explores the
            real-time patterns and trends in this knowledge. To get a sense of
            sense of the scale of these numbers, here are today's statistics
            across all articles (and scroll for more!):
          </p>
          <WikipediaStats backendData={backendData} />
        </section>
        <section className="home-section">
          <aside className="home-aside">
            <p>
              Each day, millions of pages are viewed by over 50 million people.
              These are the most viewed pages for the day, and how they've
              evolved over the past week.
            </p>
          </aside>
          <TopViews backendData={backendData} />
        </section>

        <section className="home-section">
          <aside className="home-aside">
            <p>
              Knowledge is constantly changing on Wikipedia. Thousands of
              articles are edited every day, however each article is changed for
              different reasons. Some articles are entirely new, others are
              expanded upon, and some are vandalized. Here are the top edited
              articles for the last three days, and why each one was changed.
            </p>
          </aside>
          <TopEdits backendData={backendData} />
        </section>
        <section className="home-section">
          <aside className="home-aside">
            <p>
              On top of just the number of edits, pages also vary wildly in the
              number of editors. Some pages are edited by a single person, while
              others are edited by many. These are the articles that have seen
              the most unique editors in the last three days.
            </p>
          </aside>
          <TopEditors backendData={backendData} />
        </section>
        <section className="home-section">
          <aside className="home-aside">
            <p>
              As anyone can contribute to Wikipedia, it's under a constant storm
              of vandalism. Some pages, however, are more susceptible than
              others. These are the most vandalized articles for the last three
              days.
            </p>
          </aside>
          <TopVandalism backendData={backendData} />
        </section>
        <section className="home-section">
          <aside className="home-aside">
            <p>
              Some pages may not be edited frequently, but have a lot of content
              added each time. These are the articles that have seen the most
              growth in the last three days. Each byte of text is roughly one
              character, so a change of 1KB is roughly 200 words!
            </p>
          </aside>
          <TopGrowingArticles backendData={backendData} />
        </section>

        <section className="home-section">
          <aside className="home-aside">
            <p>
              Some articles suddenly gain significant attention. Here are the
              articles that have seen the biggest increase in views compared to
              the previous day.
            </p>
          </aside>
          <TopDeltaGained backendData={backendData} />
        </section>
        <section className="home-section">
          <aside className="home-aside">
            <p>
              Additionally, some articles suddenly lose significant attention.
              Here are the articles that have seen the biggest decrease in views
              compared to the previous day.
            </p>
          </aside>
          <TopDeltaLost backendData={backendData} />
        </section>
      </main>
      <footer className="home-footer">
        <p>&copy; 2024 Pliny. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;

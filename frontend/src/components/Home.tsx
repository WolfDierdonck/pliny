import React, { useEffect, useState, useRef } from 'react';
import '../styles/Home.css';
import TopViews from './visualizations/TopViews';
import TopVandalism from './visualizations/TopVandalism';
import TopGrowingArticles from './visualizations/TopGrowingArticles';
import TopEditors from './visualizations/TopEditors';
import TopEdits from './visualizations/TopEdits';
import WikipediaStats from './visualizations/WikipediaStats';
import TopDeltaGained from './visualizations/TopDeltaGained';
import TopDeltaLost from './visualizations/TopDeltaLost';
import ScrollIndicator from './ScrollIndicator';
import ScrollToTop from './ScrollToTop';
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
import { formatDateUTC } from '../lib/utils';

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
  const topRef = useRef<HTMLDivElement>(null);
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

  const dataDate = new Date(backendData.date);
  const twoDaysAgo = new Date(backendData.date);
  twoDaysAgo.setDate(twoDaysAgo.getDate() - 2);

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
        <section className="home-section no-gap relative" ref={topRef}>
          <img
            src={`${process.env.PUBLIC_URL}/assets/pliny.png`}
            alt="Pliny logo"
            className="home-logo banner"
          />
          <h1 className="text-center">
            Exploring & analyzing Wikipedia metadata
          </h1>
          <ScrollIndicator showText={true} />
        </section>

        <section className="home-section relative">
          <p>
            Wikipedia is the world's largest encyclopedia and operates at
            incredible scale. As a living document constantly updated by
            volunteers around the world, on {formatDateUTC(dataDate)}, Wikipedia
            amassed:
          </p>
          <WikipediaStats backendData={backendData} />
          <ScrollIndicator showText={false} />
        </section>
        <section className="home-section relative">
          <aside className="home-aside">
            <p>
              Wikipedia is one of the most trafficked websites on the internet.
              Its millions of articles don't share this traffic equally - these
              are the most viewed articles on {formatDateUTC(dataDate)} and
              their evolution over the past week.
            </p>
          </aside>
          <TopViews backendData={backendData} />
          <ScrollIndicator showText={false} />
        </section>

        <section className="home-section relative">
          <aside className="home-aside">
            <p>
              Knowledge is constantly changing on Wikipedia. Thousands of
              articles are edited every day, each for different reasons.
              Articles are created, expanded, vandalized and deprecated. Here
              are the top edited articles on {formatDateUTC(twoDaysAgo)} -{' '}
              {formatDateUTC(dataDate)}.
            </p>
          </aside>
          <TopEdits backendData={backendData} />
          <ScrollIndicator showText={false} />
        </section>
        <section className="home-section relative">
          <aside className="home-aside">
            <p>
              Beyond the number of edits, pages also vary wildly in the number
              of editors. These are the articles that have seen the most unique
              editors on {formatDateUTC(twoDaysAgo)} - {formatDateUTC(dataDate)}
              .
            </p>
          </aside>
          <TopEditors backendData={backendData} />
          <ScrollIndicator showText={false} />
        </section>
        <section className="home-section relative">
          <aside className="home-aside">
            <p>
              As anyone can contribute to Wikipedia, it's under a constant storm
              of vandalism. Some pages, however, are more susceptible than
              others. These are the most vandalized articles on{' '}
              {formatDateUTC(twoDaysAgo)} - {formatDateUTC(dataDate)}.
            </p>
          </aside>
          <TopVandalism backendData={backendData} />
          <ScrollIndicator showText={false} />
        </section>
        <section className="home-section relative">
          <aside className="home-aside">
            <p>
              Some pages may not be edited frequently, but have a lot of content
              changed each time. These are the articles that have seen the most
              changes on {formatDateUTC(twoDaysAgo)} - {formatDateUTC(dataDate)}
              . Each byte of text is roughly one character, so a change of 1 KB
              is roughly 200 words!
            </p>
          </aside>
          <TopGrowingArticles backendData={backendData} />
          <ScrollIndicator showText={false} />
        </section>

        <section className="home-section relative">
          <aside className="home-aside">
            <p>
              Articles experience large fluctuations in viewership, sometimes in
              response to world events and sometimes for reasons unknown. These
              articles are the ones that gained the most views on{' '}
              {formatDateUTC(dataDate)}.
            </p>
          </aside>
          <TopDeltaGained backendData={backendData} />
          <ScrollIndicator showText={false} />
        </section>
        <section className="home-section relative">
          <aside className="home-aside">
            <p>
              Similarly, just as attention for an article can suddenly explode,
              it can also suddenly disappear. Here are the articles that have
              lost the most views on {formatDateUTC(dataDate)}.
            </p>
          </aside>
          <TopDeltaLost backendData={backendData} />
          <ScrollIndicator showText={false} />
        </section>

        {/* Updated Date Selection Section */}
        <section className="home-section relative">
          <h1>Wikipedia is constantly evolving.</h1>
          <p>
            Use the date picker in the top right corner to explore how articles,
            edits, and viewership changed throughout time on any section of
            Pliny. Discover trending topics, editing patterns, and content
            growth from different time periods.
          </p>
          <ScrollToTop targetRef={topRef} />
        </section>
      </main>
    </div>
  );
};

export default Home;

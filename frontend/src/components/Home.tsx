import React from 'react';
import '../styles/Home.css';
import TopViews from './visualizations/TopViews';
import TopVandalism from './visualizations/TopVandalism';
import TopGrowingArticles from './visualizations/TopGrowingArticles';
import TopEditors from './visualizations/TopEditors';
import TopEdits from './visualizations/TopEdits';
import TopTrendingArticles from './visualizations/TopTrendingArticles';
import WikipediaStats from './visualizations/WikipediaStats';

const Home = () => {
  return (
    <div className="home-container">
      <header className="home-header">
        <h1 className="home-title">Pliny</h1>
        <p className="home-description">
          Wikipedia is largest and most comprehensive source of information in
          the world. Unlike the encyclopedias of the past, Wikipedia is a living
          document that is constantly updated by volunteers from around the
          world. This project explores the real-time patterns and trends in this
          knowledge.
        </p>
      </header>
      <main className="home-main">
        <section className="home-section">
          <aside className="home-aside">
            <p>
              Every day, Wikipedia grows through millions of views, edits, and
              contributions. Here are today's statistics across all articles.
            </p>
          </aside>
          <WikipediaStats />
        </section>
        <section className="home-section">
          <aside className="home-aside">
            <p>
              Wikipedia is a vast repository of knowledge. This month, the most
              viewed pages are about XXXX, XXXX, and XXXX.
            </p>
          </aside>
          <TopViews />
        </section>

        <section className="home-section">
          <aside className="home-aside">
            <p>
              Knowledge is constantly changing on Wikipedia. This month, the
              most edited pages are about XXXX, XXXX, and XXXX.
            </p>
          </aside>
          <TopEdits />
        </section>
        <section className="home-section">
          <aside className="home-aside">
            <p>
              As anyone can contribute to Wikipedia, it is under a constant
              storm of vandalism. Some pages, however, are more susceptible than
              others.
            </p>
          </aside>
          <TopVandalism />
        </section>
        <section className="home-section">
          <aside className="home-aside">
            <p>
              Wikipedia is a living document that is constantly updated by
              volunteers from around the world. This month, the articles that
              grew the most are about XXXX, XXXX, and XXXX.
            </p>
          </aside>
          <TopGrowingArticles />
        </section>
        <section className="home-section">
          <aside className="home-aside">
            <p>
              Some pages are written by few authors while others are large
              collaborations. This month, the articles with the most unique
              editors are about XXXX, XXXX, and XXXX.
            </p>
          </aside>
          <TopEditors />
        </section>
        <section className="home-section">
          <aside className="home-aside">
            <p>
              Some articles suddenly gain significant attention. Here are the
              articles that have seen the biggest increase in views compared to
              last week.
            </p>
          </aside>
          <TopTrendingArticles />
        </section>
      </main>
      <footer className="home-footer">
        <p>&copy; 2024 Pliny. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;

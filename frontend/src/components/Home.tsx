import React from 'react';
import '../styles/Home.css';
import TopViewsBarGraph from './visualizations/TopViewsBarGraph';
import TopVandalismBarGraph from './visualizations/TopVandalismBarGraph';
import TopGrowingArticles from './visualizations/TopGrowingArticles';

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
              Knowledge is constantly changing on Wikipedia. This month, the
              most edited pages are about XXXX, XXXX, and XXXX.
            </p>
          </aside>
          <TopViewsBarGraph />
        </section>
        <section className="home-section">
          <aside className="home-aside">
            <p>
              As anyone can contribute to Wikipedia, it is under a constant
              storm of vandalism. Some pages, however, are more susceptible than
              others.
            </p>
          </aside>
          <TopVandalismBarGraph />
        </section>
        <section className="home-section">
          <aside className="home-aside">
            <p>
              Wikipedia is a living document that is constantly updated by
              volunteers from around the world. This month, the most edited
              pages are about XXXX, XXXX, and XXXX.
            </p>
          </aside>
          <TopGrowingArticles />
        </section>
      </main>
      <footer className="home-footer">
        <p>&copy; 2024 Pliny. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;

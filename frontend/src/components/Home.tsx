import React from 'react';
import TopViewsBarGraph from './visualizations/TopViewsBarGraph';

const Home = () => {
  return (
    <div className="newspaper-layout">
      <header className="header newspaper-header">
        <h1 className="title newspaper-title">Pliny</h1>
        <p className="subtitle newspaper-subtitle">
          Wikipedia is largest and most comprehensive source of information in
          the world. Unlike the encyclopedias of the past, Wikipedia is a living
          document that is constantly updated by volunteers from around the
          world. This project explores the real-time patterns and trends in this
          knowledge.
        </p>
      </header>
      <main className="content">
        <section className="main-article">
          <h2 className="section-title">Top Views</h2>
          <TopViewsBarGraph />
        </section>
        <aside className="sidebar">
          <h2 className="section-title">Most Edited Pages</h2>
          <p>
            Knowledge is constantly changing on Wikipedia. This month, the most
            edited pages are about XXXX, XXXX, and XXXX.
          </p>
        </aside>
      </main>
      <footer className="footer">
        <p>&copy; 2024 Pliny. All rights reserved.</p>
      </footer>
    </div>
  );
};

export default Home;

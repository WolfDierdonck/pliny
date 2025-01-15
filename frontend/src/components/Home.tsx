import React from 'react';
import StackedLinesExample from './StackedLines';
import PackExample from './Pack';
import BarGraphExample from './BarGraph';
import SankeyExample from './Sankey';
import ScatterPlot from './ScatterPlot';

const Divider = () => <div style={{
width: '20%',
height: '3px',
borderRadius: '3px',
backgroundColor: '#E3DAC9',
marginTop: '32px',
}} />;

const Home = () => {

  const fullChartWidth = window.innerWidth * 0.9;
  const fullChartHeight = window.innerWidth * 0.3;
  const smallChartWidth = window.innerWidth * 0.5;
  const smallChartHeight = smallChartWidth * 0.6;

  return (
    <div style={{
      display: 'flex',
      width: '100%',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      gap: '10vw',
      backgroundColor: 'linen',
      color: 'black',
      paddingBottom: '10vh',
    }}>
      <Header />
      <Divider />
      <GraphWrapper component={<BarGraphExample width={smallChartWidth} height={smallChartHeight} />}
        title=""
        body="Wikipedia operates and changes at an incredible scale. This year, its XXXX pages were edited XXXX times and it amassed XXXX views."
        textPosition="left"
      />
      <Divider />
      <GraphWrapper component={<PackExample width={fullChartWidth} height={fullChartHeight} />}
        title=""
        body="Knowledge is constantly changing on Wikipedia. This month, the most edited pages are about XXXX, XXXX, and XXXX."
        textPosition="top"
      />
      <GraphWrapper component={<ScatterPlot width={smallChartWidth} height={smallChartHeight} />}
        title=""
        body="Surprisingly, the correlation between the number of page views and the number of revisions is not as strong as one might expect. As of XXXX, the correlation coefficient is 0.3."
        textPosition="left"
      />
      <Divider />
      <GraphWrapper component={<SankeyExample width={fullChartWidth} height={fullChartHeight} />}
        title=""
        body="A Sankey diagram is a type of flow diagram in which the width of the arrows is proportional to the flow rate. This can be a cool way to visualize the top X pages over the last 12 months."
        textPosition="top"
      />
      <GraphWrapper component={<StackedLinesExample width={smallChartWidth} height={smallChartHeight} />}
        title=""
        body="As anyone can contribute to Wikipedia, it is under a constant storm of vandalism. Some pages, however, are more susceptible than others."
        textPosition="left"
      />
    </div>
  );
};

const GraphWrapper: React.FC<{
  component: React.ReactNode;
  title: string;
  body: string;
  textPosition: 'top' | 'left' | 'right';
}> = ({ component, title, body, textPosition }) => {
  const textAlignment = textPosition === 'top' ? 'center' : 'left';
  const titleColor = '#000000'; // Black for titles
  const bodyColor = '#555555'; // Medium gray for body text

  const textComponent = (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: textAlignment,
      maxWidth: textPosition === 'top' ? '50%' : '30%',
      padding: '1rem',
      gap: '1rem',
    }}>
      <h2 style={{
        fontSize: '2rem',
        fontWeight: 'bold',
        color: titleColor,
      }}
      >{title}</h2>
      <p style={{
        fontSize: '1.2rem',
        fontWeight: 'semibold',
        color: bodyColor,
      }}>{body}</p>
    </div>
  );
  const wrappedComponent = (<div style={{
    borderRadius: '16px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
    display: 'flex',
    overflow: 'hidden',
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
  }}>
    {component}
  </div>);
  const order = textPosition === 'right' ? [component, textComponent] : [textComponent, component];
  const flexDirection = textPosition === 'top' ? 'column' : 'row';

  return (
    <div style={{
      display: 'flex',
      flexDirection: flexDirection,
      justifyContent: 'center',
      flexWrap: 'wrap',
      alignItems: 'center',
      gap: '1rem',
      width: '100%',
    }}>
      {order}
    </div>
  );
};

const Header = () => {
  const titleColor = '#000000'; // Black for titles
  const bodyColor = '#555555'; // Medium gray for body text

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'row',
      justifyContent: 'center',
      alignItems: 'center',
      gap: '16rem',
      paddingLeft: '15vw',
      paddingRight: '15vw',
      paddingTop: '35vh',
      paddingBottom: '15vh'
    }}>
      <h1 style={{
        fontSize: '8rem',
        fontWeight: 'bold',
        maxWidth: '50%',
        color: titleColor,
        fontFamily: 'serif',
      }}
      >
        Pliny
      </h1>
      <p
        style={{
          maxWidth: '50%',
          fontSize: '1.2rem',
          color: bodyColor,
        }}
      >
        Wikipedia is largest and most comprehensive source of information in the world. Unlike the encyclopedias of the past, Wikipedia is a living document that is constantly updated by volunteers from around the world. This project explores the real-time patterns and trends in this knowledge.
      </p>
    </div>
  );
};

export default Home;
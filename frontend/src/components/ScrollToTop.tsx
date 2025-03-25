import React from 'react';

interface ScrollToTopProps {
  targetRef: React.RefObject<HTMLElement>;
}

const ScrollToTop: React.FC<ScrollToTopProps> = ({ targetRef }) => {
  const handleClick = () => {
    targetRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div
      className="scroll-indicator absolute bottom-4 left-1/2 transform -translate-x-1/2 flex flex-col items-center text-slate-800 opacity-80 hover:opacity-100 transition-opacity cursor-pointer"
      onClick={handleClick}
      aria-label="Scroll to top"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="currentColor"
        className="w-8 h-8 animate-bounce"
      >
        <path
          fillRule="evenodd"
          d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm-.53 5.47a.75.75 0 011.06 0l3 3a.75.75 0 11-1.06 1.06l-1.72-1.72V15.75a.75.75 0 01-1.5 0V10.06l-1.72 1.72a.75.75 0 11-1.06-1.06l3-3z"
          clipRule="evenodd"
        />
      </svg>
      <span className="text-sm font-medium mt-1">Back to top</span>
    </div>
  );
};

export default ScrollToTop;

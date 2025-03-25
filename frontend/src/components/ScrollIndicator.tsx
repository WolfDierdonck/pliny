import React from 'react';

interface ScrollIndicatorProps {
  showText?: boolean;
}

const ScrollIndicator: React.FC<ScrollIndicatorProps> = ({
  showText = true,
}) => {
  const handleClick = (event: React.MouseEvent) => {
    // Find the parent section
    const currentSection = (event.currentTarget as HTMLElement).closest(
      '.home-section',
    );

    if (currentSection) {
      // Find the next section sibling
      const nextSection = currentSection.nextElementSibling as HTMLElement;

      if (nextSection && nextSection.classList.contains('home-section')) {
        // Scroll to the next section
        nextSection.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <div
      className="scroll-indicator absolute bottom-4 left-1/2 transform -translate-x-1/2 flex flex-col items-center text-slate-800 opacity-80 hover:opacity-100 transition-opacity cursor-pointer"
      onClick={handleClick}
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="currentColor"
        className="w-8 h-8 animate-bounce"
      >
        <path
          fillRule="evenodd"
          d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm-.53 14.03a.75.75 0 001.06 0l3-3a.75.75 0 10-1.06-1.06l-1.72 1.72V8.25a.75.75 0 00-1.5 0v5.69l-1.72-1.72a.75.75 0 00-1.06 1.06l3 3z"
          clipRule="evenodd"
        />
      </svg>
      {showText && (
        <span className="text-sm font-medium mt-1">Scroll to explore</span>
      )}
    </div>
  );
};

export default ScrollIndicator;

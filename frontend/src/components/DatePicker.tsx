import React from 'react';

interface DatePickerProps {
  date: string;
  // eslint-disable-next-line
  onChange: (newDate: string) => void;
  minDate?: string;
  maxDate?: string;
  className?: string;
  showLabel?: boolean;
}

const DatePicker: React.FC<DatePickerProps> = ({
  date,
  onChange,
  minDate = '2023-01-01',
  maxDate,
  className = '',
  showLabel = false,
}) => {
  const [typingDate, setTypingDate] = React.useState(date);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newDate = e.target.value;
    setTypingDate(newDate);

    // Only update parent if it's a valid date
    if (newDate && !isNaN(new Date(newDate).getTime())) {
      onChange(newDate);
    }
  };

  return (
    <div className="date-picker-wrapper">
      {showLabel && (
        <label htmlFor="date-input" className="date-picker-label mr-3">
          Select Date:
        </label>
      )}
      <input
        id="date-input"
        type="date"
        value={typingDate}
        onChange={handleChange}
        className={className || 'date-picker'}
        min={minDate}
        max={maxDate}
      />
    </div>
  );
};

export default DatePicker;

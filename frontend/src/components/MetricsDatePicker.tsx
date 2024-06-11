import { RangeDatepicker } from "chakra-dayzed-datepicker";
import { useState } from "react";

const MetricsDatePicker = ({ onSelectedDatesChange }) => {
  const [selectedDates, setSelectedDates] = useState([new Date(), new Date()]);

  const handleDateChange = (newDates) => {
    // handle date changes here
    setSelectedDates(newDates);
    // Pass the selected dates to the parent component
    onSelectedDatesChange(newDates);
  };

  return (
    <div>
      <RangeDatepicker
        selectedDates={selectedDates}
        onDateChange={handleDateChange}
      />
    </div>
  );
};

export default MetricsDatePicker;

interface Log {
  date: string;
  time: string;
  temperature: number;
  gasLevels: number;
}

const averageLogs = [
  { date: "Tuesday, 4 October 2023", average_temperature: 26.55, average_gasLevels: 67.5 },
  { date: "Wednesday, 5 October 2023", average_temperature: 26.85, average_gasLevels: 82.5 },
  { date: "Thursday, 6 October 2023", average_temperature: 27.15, average_gasLevels: 97.5 },
  { date: "Friday, 7 October 2023", average_temperature: 27.45, average_gasLevels: 112.5 },
  { date: "Saturday, 8 October 2023", average_temperature: 27.75, average_gasLevels: 127.5 },
  { date: "Sunday, 9 October 2023", average_temperature: 28.05, average_gasLevels: 142.5 },
  { date: "Monday, 10 October 2023", average_temperature: 28.35, average_gasLevels: 157.5 },
];

const logs: Log[] = [
  { date: "Monday, 3 October 2023", time: "12:00:00", temperature: 25.65, gasLevels: 180 },
  { date: "Monday, 3 October 2023", time: "12:30:00", temperature: 26.13, gasLevels: 175 },
  { date: "Monday, 3 October 2023", time: "13:00:00", temperature: 26.48, gasLevels: 170 },
  { date: "Monday, 3 October 2023", time: "13:30:00", temperature: 26.02, gasLevels: 165 },
  { date: "Monday, 3 October 2023", time: "14:00:00", temperature: 25.75, gasLevels: 160 },
  { date: "Monday, 3 October 2023", time: "14:30:00", temperature: 25.85, gasLevels: 155 },
  { date: "Monday, 3 October 2023", time: "15:00:00", temperature: 25.92, gasLevels: 150 },
  { date: "Monday, 3 October 2023", time: "15:30:00", temperature: 25.45, gasLevels: 145 },
  { date: "Monday, 3 October 2023", time: "16:00:00", temperature: 25.27, gasLevels: 140 },
  { date: "Monday, 3 October 2023", time: "16:30:00", temperature: 25.82, gasLevels: 135 },
  { date: "Monday, 3 October 2023", time: "17:00:00", temperature: 26.03, gasLevels: 130 },
  { date: "Monday, 3 October 2023", time: "17:30:00", temperature: 25.95, gasLevels: 125 },
  { date: "Monday, 3 October 2023", time: "18:00:00", temperature: 25.78, gasLevels: 120 },
  { date: "Monday, 3 October 2023", time: "18:30:00", temperature: 25.62, gasLevels: 115 },
  { date: "Monday, 3 October 2023", time: "19:00:00", temperature: 25.55, gasLevels: 110 },
  { date: "Monday, 3 October 2023", time: "19:30:00", temperature: 25.88, gasLevels: 105 },
  { date: "Monday, 3 October 2023", time: "20:00:00", temperature: 26.13, gasLevels: 100 },
  { date: "Monday, 3 October 2023", time: "20:30:00", temperature: 25.98, gasLevels: 95 },
  { date: "Monday, 3 October 2023", time: "21:00:00", temperature: 25.77, gasLevels: 90 },
  { date: "Monday, 3 October 2023", time: "21:30:00", temperature: 25.45, gasLevels: 85 },
  { date: "Monday, 3 October 2023", time: "22:00:00", temperature: 25.35, gasLevels: 80 },
  { date: "Monday, 3 October 2023", time: "22:30:00", temperature: 25.72, gasLevels: 75 },
  { date: "Monday, 3 October 2023", time: "23:00:00", temperature: 25.95, gasLevels: 70 },
  { date: "Monday, 3 October 2023", time: "23:30:00", temperature: 25.85, gasLevels: 65 },
  { date: "Tuesday, 4 October 2023", time: "00:00:00", temperature: 25.65, gasLevels: 60 },
  { date: "Tuesday, 4 October 2023", time: "00:30:00", temperature: 25.58, gasLevels: 55 },
  { date: "Tuesday, 4 October 2023", time: "01:00:00", temperature: 25.43, gasLevels: 50 },
  { date: "Tuesday, 4 October 2023", time: "01:30:00", temperature: 25.28, gasLevels: 45 },
  { date: "Tuesday, 4 October 2023", time: "02:00:00", temperature: 25.35, gasLevels: 40 },
  { date: "Tuesday, 4 October 2023", time: "02:30:00", temperature: 25.68, gasLevels: 35 },
  { date: "Tuesday, 4 October 2023", time: "03:00:00", temperature: 25.95, gasLevels: 30 },
  { date: "Tuesday, 4 October 2023", time: "03:30:00", temperature: 26.05, gasLevels: 25 },
  { date: "Tuesday, 4 October 2023", time: "04:00:00", temperature: 26.15, gasLevels: 20 },
  { date: "Tuesday, 4 October 2023", time: "04:30:00", temperature: 26.28, gasLevels: 15 },
  { date: "Tuesday, 4 October 2023", time: "05:00:00", temperature: 26.18, gasLevels: 10 },
  { date: "Tuesday, 4 October 2023", time: "05:30:00", temperature: 25.85, gasLevels: 5 },
  { date: "Tuesday, 4 October 2023", time: "06:00:00", temperature: 25.75, gasLevels: 10 },
  { date: "Tuesday, 4 October 2023", time: "06:30:00", temperature: 25.85, gasLevels: 15 },
  { date: "Tuesday, 4 October 2023", time: "07:00:00", temperature: 25.95, gasLevels: 20 },
  { date: "Tuesday, 4 October 2023", time: "07:30:00", temperature: 26.05, gasLevels: 25 },
  { date: "Tuesday, 4 October 2023", time: "08:00:00", temperature: 26.15, gasLevels: 30 },
  { date: "Tuesday, 4 October 2023", time: "08:30:00", temperature: 26.25, gasLevels: 35 },
  { date: "Tuesday, 4 October 2023", time: "09:00:00", temperature: 26.35, gasLevels: 40 },
  { date: "Tuesday, 4 October 2023", time: "09:30:00", temperature: 26.45, gasLevels: 45 },
  { date: "Tuesday, 4 October 2023", time: "10:00:00", temperature: 26.55, gasLevels: 50 },
  { date: "Tuesday, 4 October 2023", time: "10:30:00", temperature: 26.65, gasLevels: 55 },
  { date: "Tuesday, 4 October 2023", time: "11:00:00", temperature: 26.75, gasLevels: 60 },
  { date: "Tuesday, 4 October 2023", time: "11:30:00", temperature: 26.85, gasLevels: 65 },
  { date: "Tuesday, 4 October 2023", time: "12:00:00", temperature: 26.95, gasLevels: 70 },
  { date: "Tuesday, 4 October 2023", time: "12:30:00", temperature: 27.05, gasLevels: 75 },
  { date: "Tuesday, 4 October 2023", time: "13:00:00", temperature: 27.15, gasLevels: 80 },
  { date: "Tuesday, 4 October 2023", time: "13:30:00", temperature: 27.25, gasLevels: 85 },
  { date: "Tuesday, 4 October 2023", time: "14:00:00", temperature: 27.35, gasLevels: 90 },
  { date: "Tuesday, 4 October 2023", time: "14:30:00", temperature: 27.45, gasLevels: 95 },
  { date: "Tuesday, 4 October 2023", time: "15:00:00", temperature: 27.55, gasLevels: 100 },
  { date: "Tuesday, 4 October 2023", time: "15:30:00", temperature: 27.65, gasLevels: 105 },
  { date: "Tuesday, 4 October 2023", time: "16:00:00", temperature: 27.75, gasLevels: 110 },
  { date: "Tuesday, 4 October 2023", time: "16:30:00", temperature: 27.85, gasLevels: 115 },
  { date: "Tuesday, 4 October 2023", time: "17:00:00", temperature: 27.95, gasLevels: 120 },
];

export { logs, averageLogs };

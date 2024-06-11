import LogsChart from "./LogsChart.tsx";
import { useEffect, useState } from "react";
import { getAverageMetrics } from "../../services/data-service.ts";
import { Tab, TabList, TabPanel, TabPanels, Tabs } from "@chakra-ui/react";

interface Props {
  roomId: number;
}

export interface MetaData {
  title: string;
  series: string;
  minY: number;
  maxY: number;
  xAxis: string;
  yAxis: string;
  logs: Array<number>;
  dates: Array<string>;
}

const metricNames = [
  "TEMP",
  "CO",
  "H2",
  "CH4",
  "LPG",
  "PROPANE",
  "ALCOHOL",
  "SMOKE",
];

function RoomCharts({ roomId }: Props) {
  const [metrics, setMetrics] = useState([]);

  const testData: MetaData = {
    title: "Temperature For Last 7 Days",
    series: "Temperature",
    xAxis: "Days",
    yAxis: "Temperature",
    minY: 0,
    maxY: 1,
    logs: [0.3, 0.4, 0.5, 0.2, 0.1],
    dates: [
      "Thursday 31 Oct",
      "Friday 1 November",
      "Saturday 2 November",
      "Sunday 3 November",
      "Monday 5 November",
    ],
  };

  function transformData(inputData, metricName: string) {
    // Filter the inputData based on the metric name
    const filteredData = inputData
      .map((entry) => ({
        date: entry.date,
        value: entry[metricName],
      }))
      .slice(0, 7);

    // Extract dates and logs from the filtered data
    const dates = filteredData.map((entry) => entry.date);
    const logs = filteredData.map((entry) =>
      parseFloat(entry.value.toFixed(3)),
    );

    // Calculate minY and maxY
    const minY = Math.min(...logs);
    const maxY = Math.max(...logs);

    const title = `${metricName} For Last 7 Days`;

    const object = {
      title,
      series: metricName,
      xAxis: "Days",
      yAxis: metricName,
      minY,
      maxY,
      logs,
      dates,
    };
    return object;
  }

  useEffect(() => {
    getAverageMetrics(roomId).then((metrics) => setMetrics(metrics));
  }, []);

  return (
    <>
      <Tabs variant="soft-rounded" colorScheme="green">
        <TabList>
          {metricNames.map((metric) => {
            return <Tab key={metric}>{metric}</Tab>;
          })}
        </TabList>
        <TabPanels>
          {metricNames.map((metric) => {
            return (
              <TabPanel key={metric}>
                <LogsChart metaData={transformData(metrics, metric)} />
              </TabPanel>
            );
          })}
        </TabPanels>
      </Tabs>
    </>
  );
}

export default RoomCharts;

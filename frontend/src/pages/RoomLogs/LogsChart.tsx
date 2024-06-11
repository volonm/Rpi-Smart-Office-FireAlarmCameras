import React from "react";
import ReactApexChart from "react-apexcharts";
import { MetaData } from "./RoomCharts.tsx";

interface Props {
  metaData: MetaData;
}

const LogsChart = (props: Props) => {
  const { metaData } = props;

  const state = {
    series: [
      {
        name: metaData.series,
        data: metaData.logs,
      },
    ],
    options: {
      chart: {
        height: 350,
        type: "line",
        dropShadow: {
          enabled: true,
          color: "#000",
          top: 18,
          left: 7,
          blur: 10,
          opacity: 0.2,
        },
        toolbar: {
          show: false,
        },
      },
      colors: ["#77B6EA", "#545454"],
      dataLabels: {
        enabled: true,
      },
      stroke: {
        curve: "smooth",
      },
      title: {
        text: metaData.title,
        align: "left",
      },
      grid: {
        borderColor: "#e7e7e7",
        row: {
          colors: ["#f3f3f3", "transparent"],
          opacity: 0.5,
        },
      },
      markers: {
        size: 1,
      },
      xaxis: {
        categories: metaData.dates,
        title: {
          text: "Days",
        },
      },
      yaxis: {
        title: {
          text: "Metrics",
        },
        min: metaData.minY,
        max: metaData.maxY,
        forceNiceScale: true,
        labels: {
          formatter: function (value) {
            return value.toFixed(2);
          },
        },
      },
      legend: {
        position: "top",
        horizontalAlign: "right",
        floating: true,
        offsetY: -25,
        offsetX: -5,
      },
    },
  };

  return (
    <div id="chart">
      <ReactApexChart
        options={state.options}
        series={state.series}
        type="line"
        height={350}
      />
    </div>
  );
};

export default LogsChart;

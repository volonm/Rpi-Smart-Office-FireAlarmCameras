import { useState } from "react";
import {
  Button,
  ButtonGroup,
  Flex,
  Stack,
  Table,
  TableCaption,
  TableContainer,
  Tbody,
  Td,
  Text,
  Tfoot,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react";
import { Entry, getMetricsByPeriod } from "../../services/data-service.ts";
import { useLocation } from "react-router-dom";
import MetricsDatePicker from "../../components/MetricsDatePicker.tsx";

const rowsPerPage = 5;

function LogsTable() {
  const { state } = useLocation();
  const [startIndex, setStartIndex] = useState(0);
  const [logs, setLogs] = useState<Entry[]>([]);

  // useEffect(() => {
  //   console.log(state.room.id);
  //   getAllMetrics(state.room.id).then((data) => {
  //     setLogs(data);
  //     console.log("Metrics", data);
  //   });
  // }, []);

  const handleSelectedDates = (selectedDates: Date[]) => {
    if (selectedDates.length >= 2) {
      const formattedStartDate = selectedDates[0].toISOString().split("T")[0];
      const formattedEndDate = selectedDates[1].toISOString().split("T")[0];

      getMetricsByPeriod(
        state.room.id,
        formattedStartDate,
        formattedEndDate,
      ).then((data) => {
        setLogs(data);
        setStartIndex(0);
      });
    }
  };

  const handlePrevClick = () => {
    if (startIndex >= rowsPerPage) {
      setStartIndex(startIndex - rowsPerPage);
    }
  };

  const handleNextClick = () => {
    if (startIndex + rowsPerPage < logs.length) {
      setStartIndex(startIndex + rowsPerPage);
    }
  };

  return (
    <Stack spacing={3}>
      <MetricsDatePicker onSelectedDatesChange={handleSelectedDates} />
      <TableContainer>
        {logs.length > 0 ? (
          <Table variant="simple">
            <TableCaption>Metrics are captured every 30 minutes</TableCaption>
            <Thead>
              <Tr>
                <Th>Date</Th>
                <Th>Time</Th>
                <Th>Temperature</Th>
                <Th>Carbon Monoxide</Th>
                <Th>Hydrogen</Th>
                <Th>Methane</Th>
                <Th>Butane</Th>
                <Th>Propane</Th>
                <Th>Alcohol</Th>
                <Th>Smoke</Th>
              </Tr>
            </Thead>
            <Tbody>
              {logs
                .slice(startIndex, startIndex + rowsPerPage)
                .map((log, index) => (
                  <Tr key={index}>
                    <Td>{log.date}</Td>
                    <Td>{log.time}</Td>
                    <Td>{log.temperature}</Td>
                    <Td>{log.carbonMonoxide}</Td>
                    <Td>{log.hydrogen}</Td>
                    <Td>{log.methane}</Td>
                    <Td>{log.butane}</Td>
                    <Td>{log.propane}</Td>
                    <Td>{log.alcohol}</Td>
                    <Td>{log.smoke}</Td>
                  </Tr>
                ))}
            </Tbody>
            <Tfoot>
              <Tr>
                <Th>Date</Th>
                <Th>Time</Th>
                <Th>Temperature</Th>
                <Th>Carbon Monoxide</Th>
                <Th>Hydrogen</Th>
                <Th>Methane</Th>
                <Th>Butane</Th>
                <Th>Propane</Th>
                <Th>Alcohol</Th>
                <Th>Smoke</Th>
              </Tr>
            </Tfoot>
          </Table>
        ) : (
          <Text>No Data Available</Text>
        )}
      </TableContainer>

      <Flex justifyContent="right">
        {logs.length > 0 && (
          <Stack mt={4}>
            <Text color="teal">{`${
              startIndex / rowsPerPage + 1
            } out of ${Math.ceil(logs.length / rowsPerPage)}`}</Text>
            <ButtonGroup size="sm">
              <Button colorScheme="teal" onClick={handlePrevClick}>
                Prev
              </Button>
              <Button colorScheme="teal" onClick={handleNextClick}>
                Next
              </Button>
            </ButtonGroup>
          </Stack>
        )}
      </Flex>
    </Stack>
  );
}

export default LogsTable;

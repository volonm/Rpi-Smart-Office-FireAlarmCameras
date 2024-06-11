import {
  Heading,
  Stack,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
} from "@chakra-ui/react";
import LogsTable from "./LogsTable";
import { useLocation } from "react-router-dom";
import RoomCharts from "./RoomCharts.tsx";
import VideoPage from "./VideoPage.tsx";
import { Room } from "../../services/data-service.ts";

function RoomLogs() {
  const { state } = useLocation();

  const room = state?.room as Room;

  // @ts-ignore
  return (
    <Stack spacing={3}>
      <Heading size="lg">{state ? room.name + " Logs" : "Logs"}</Heading>

      <Tabs>
        <TabList>
          <Tab>Table</Tab>
          <Tab>Chart</Tab>
          <Tab>Camera</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            <LogsTable />
          </TabPanel>
          <TabPanel>
            <RoomCharts roomId={room.id} />
          </TabPanel>
          <TabPanel>
            <VideoPage room={room} />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Stack>
  );
}

export default RoomLogs;

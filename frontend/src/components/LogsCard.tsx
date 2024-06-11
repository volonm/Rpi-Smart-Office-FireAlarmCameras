import {
  Alert,
  AlertIcon,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Heading,
  Stack,
  StackDivider,
} from "@chakra-ui/react";
import { useState, useEffect } from "react";
import { Log, getRecentLogs } from "../services/data-service";

function LogsCard() {

  const [logs, setLogs] = useState<Log[]>();

  useEffect(() => {
    getRecentLogs().then(data => setLogs(data))
  }, [])

  return (
    <Card>
      <CardHeader>
        <Heading size="md">Recent Logs</Heading>
      </CardHeader>
      <Divider />
      <CardBody>
        <Stack divider={<StackDivider />} spacing="4">
          {logs && logs.slice(-3).map((log) => {
            let alertStarted = log.msg.includes("Alert started")
            return <Alert status={alertStarted ? "error" : "success"}>
              <AlertIcon />
              {log.msg}
            </Alert>
          })}
        </Stack>
      </CardBody>
    </Card>
  );
}

export default LogsCard;

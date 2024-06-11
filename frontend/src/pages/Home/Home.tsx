import {
  Box,
  Divider,
  Flex,
  Heading,
  SimpleGrid,
  Stack,
} from "@chakra-ui/react";
import RoomCard from "./RoomCard";
import { useEffect, useState } from "react";
import { getRooms, Room } from "../../services/data-service.ts";
import LogsCard from "../../components/LogsCard.tsx";
import ColorBox from "../../components/ColorBox.tsx";

function Home() {
  const [rooms, setRooms] = useState<Room[]>([]);

  useEffect(() => {
    getRooms().then((rooms) => setRooms(rooms));
  }, []);

  function changeRoomCard(room: Room) {
    const updatedRooms = rooms.map((r) => (r.id === room.id ? room : r));
    setRooms(updatedRooms);
  }

  return (
    <Stack spacing={3}>
      <Heading size="lg">Rooms</Heading>
      <Divider />

      <Flex direction={{ base: "column", md: "row" }}>
        <Box
          flex="1"
          maxW={{ base: "100%", md: "25%" }}
          mr={{ base: 0, md: 4 }}
          mb={{ base: 4, md: 0 }}
        >
          <LogsCard />
        </Box>

        <SimpleGrid
          columns={{ base: 1, md: 4 }}
          spacing={4}
          minChildWidth={250}
          mb={12}
          width="100%"
          flex="1"
        >
          {rooms.map((room) => (
            <RoomCard
              room={room}
              key={room.id}
              changeRoomCard={changeRoomCard}
            />
          ))}
        </SimpleGrid>
      </Flex>
    </Stack>
  );
}

export default Home;

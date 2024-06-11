import {
  Button,
  Card,
  CardBody,
  CardFooter,
  Divider,
  Heading,
  Image,
  Stack,
  Text,
  useDisclosure,
} from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import { Room } from "../../services/data-service.ts";
import { getImage } from "../../services/image-service.ts";
import { useEffect, useState } from "react";
import RoomModal from "../../components/RoomModal.tsx";

interface Props {
  room: Room;
  changeRoomCard: (room: Room) => void;
}

function RoomCard({ room, changeRoomCard }: Props) {
  const navigate = useNavigate();
  const [imageURL, setImageURL] = useState("");

  const { isOpen, onOpen, onClose } = useDisclosure();

  useEffect(() => {
    getImage(room.name).then((resultURL) => setImageURL(resultURL));
  }, []);

  return (
    <>
      {" "}
      <Card maxWidth={450}>
        <CardBody>
          {/* Image */}
          <Image
            src={
              room.name === "Undefined"
                ? "https://static.vecteezy.com/system/resources/previews/014/989/719/original/question-mark-hand-drawn-doodle-faq-symbol-free-vector.jpg"
                : imageURL
            }
            borderRadius="lg"
            objectFit="fill"
            aspectRatio={5 / 3}
          />

          {/* Main Part */}
          <Stack spacing={3} mt={4}>
            <Heading size="md">{room.name}</Heading>

            <Text color="blue.400">
              Last Temperature: {parseFloat(room.average_temp.toFixed(3))}
            </Text>
          </Stack>
        </CardBody>

        {/* Footer */}
        <Divider />

        <CardFooter>
          <Stack spacing={2} direction="row" align="center">
            <Button
              colorScheme="teal"
              onClick={() => navigate("/logs", { state: { room } })}
              size={"sm"}
            >
              View
            </Button>
            <Button colorScheme="blue" onClick={onOpen} size={"sm"}>
              Edit
            </Button>
          </Stack>
        </CardFooter>
      </Card>
      <RoomModal
        isOpen={isOpen}
        onClose={onClose}
        room={room}
        changeRoomCard={changeRoomCard}
      />
    </>
  );
}

export default RoomCard;

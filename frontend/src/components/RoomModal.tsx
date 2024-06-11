import {
  Button,
  FormControl,
  FormLabel,
  Input,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalFooter,
  ModalHeader,
  ModalOverlay,
} from "@chakra-ui/react";
import { changeRoomName, Room } from "../services/data-service.ts";
import { useState } from "react";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  changeRoomCard: (room: Room) => void;
  room: Room;
}

function RoomModal({ isOpen, onClose, room, changeRoomCard }: Props) {
  const [newName, setNewName] = useState("");

  function handleChange(event: React.ChangeEvent<HTMLInputElement>) {
    setNewName(event.target.value);
  }

  function saveNewRoom() {
    changeRoomName(room.id, newName);
    changeRoomCard({ ...room, name: newName });
    onClose();
  }

  return (
    <>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Change Room Name</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <FormControl>
              <FormLabel>New room name</FormLabel>
              <Input
                placeholder="Room name..."
                value={newName}
                onChange={handleChange}
              />
            </FormControl>
          </ModalBody>

          <ModalFooter>
            <Button colorScheme="blue" mr={3} onClick={saveNewRoom}>
              Save
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}

export default RoomModal;

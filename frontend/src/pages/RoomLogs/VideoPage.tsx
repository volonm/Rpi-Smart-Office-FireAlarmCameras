import {
  Accordion,
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Box,
} from "@chakra-ui/react";
import { Room } from "../../services/data-service.ts";
import { useEffect, useState } from "react";
import {
  getVideosByRoom,
  VideoMetaData,
} from "../../services/video-service.ts";
import VideoBox from "../../components/VideoBox.tsx";

interface Props {
  room: Room;
}

function VideoPage({ room }: Props) {
  const [videos, setVideos] = useState<VideoMetaData[]>([]);

  useEffect(() => {
    console.log("Room id");
    getVideosByRoom(room.id).then((data) => {
      setVideos(data);
    });
  }, []);

  return (
    <Accordion defaultIndex={[0]} allowMultiple>
      {videos &&
        videos.map((video) => {
          return (
            <AccordionItem key={video.id}>
              <h2>
                <AccordionButton>
                  <Box as="span" flex="1" textAlign="left">
                    {video.date} {video.time}
                  </Box>
                  <AccordionIcon />
                </AccordionButton>
              </h2>
              <AccordionPanel pb={4}>
                <VideoBox videoId={video.id} />
              </AccordionPanel>
            </AccordionItem>
          );
        })}
    </Accordion>
  );
}

export default VideoPage;

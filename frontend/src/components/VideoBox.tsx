import { djangoServerPort, ipAddress } from "../config.ts";

interface Props {
  videoId: number;
}

function VideoBox({ videoId }: Props) {
  return (
    <>
      <video controls>
        <source
          src={`http://${ipAddress}:${djangoServerPort}/sensors/media?id=${videoId}`}
          type="video/mp4"
        />
        Your browser does not support
      </video>
    </>
  );
}

export default VideoBox;

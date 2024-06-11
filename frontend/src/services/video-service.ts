import api from "./api.ts";

export interface Video {
  id: number;
  date: string;
  time: string;
  file: string;
}

export interface VideoMetaData {
  id: number;
  rid: number;
  time: string;
  date: string;
  roomName: string;
}

export async function getAllVideos() {
  const res = await api.get<{ videos: VideoMetaData[] }>(
    "/sensors/getAllVideos",
  );
  return res.data.videos;
}

export async function getVideosByRoom(rid: number) {
  const res = await api.get<{ videos: VideoMetaData[] }>(
    "/sensors/getVideosByRoom",
    { params: { rid } },
  );
  return res.data.videos;
}

export async function getVideoById(id: number) {
  const res = await api.get<Video>("/sensors/getVideoById", {
    params: {
      id,
    },
  });
  return res.data;
}

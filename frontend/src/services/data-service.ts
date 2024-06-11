import api from "./api";

export interface Entry {
  date: string;
  time: string;
  temperature: number;
  carbonMonoxide: number;
  hydrogen: number;
  methane: number;
  butane: number;
  propane: number;
  alcohol: number;
  smoke: number;
}

export interface Room {
  id: number;
  name: string;
  average_temp: number;
}

function serialize(data: any) {
  let entry: Entry = {
    date: data.date,
    time: data.time,
    temperature: data.TEMP,
    carbonMonoxide: data.CO,
    hydrogen: data.H2,
    methane: data.CH4,
    butane: data.LPG,
    propane: data.PROPANE,
    alcohol: data.ALCOHOL,
    smoke: data.SMOKE,
  };
  return entry;
}

export async function getRooms() {
  const res = await api.get<{
    rooms: Room[];
  }>("/api/getAverageAll");
  return res.data.rooms;
}

export async function getAllMetrics(id: number) {
  console.log("From func " + id);
  const res = await api.get("api/getRoomMetricDay", {
    params: { id },
  });
  console.log("Fromd data service", res.data);
  const serializedData: Entry[] = res.data.length > 0 ? res.data.map((element: any) => serialize(element)) : [];
  return serializedData;
}

export async function changeRoomName(id: number, newName: string) {
  return await api.post(
    "/api/renameRoom",
    { id: id, name: newName },
    {
      headers: { "Content-Type": "application/json" },
    }
  );
}

export async function getAverageMetrics(roomId: number) {
  const res = await api.get("/api/getAverageRid", {
    params: { id: roomId },
  });
  return res.data["average_per_7_days"];
}

export async function getMetricsByPeriod(id: number, start: string, end: string) {
  const res = await api.get("api/getRoomMetricPeriod", {
    params: {
      id,
      start,
      end,
    },
  });
  const data = res.data["selected_days"];
  const serializedData: Entry[] = data.length > 0 ? data.map((element: any) => serialize(element)) : [];
  return serializedData;
}

/*
"id": 1,
"rid": 1,
"date": "2023-11-03",
"time": "13:03:46.408166",
"msg": "Alert started in Living Room"
*/

export interface Log {
  id: number;
  rid: number;
  date: string;
  time: string;
  msg: string;
}

export async function getRecentLogs() {
  const res = await api.get<{ logs: Log[] }>("sensors/getSysLogs");
  return res.data.logs;
}

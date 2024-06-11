export interface Room {
  image: string;
  name: string;
  isOnline: boolean;
  lastTemperature: string;
}

const rooms: Room[] = [
  {
    image: "https://media.houseandgarden.co.uk/photos/649188c6d6a55acd0396e5f0/4:3/w_2220,h_1665,c_limit/HG-HAM-KateCox06468-CREDIT-TomGriffiths-TomGPhoto.jpg",
    name: "Kitchen",
    isOnline: true,
    lastTemperature: "23.5",
  },
  {
    image: "https://www.ikea.com/images/a-grey-green-taellasen-upholstered-bed-frame-with-privacy-sc-26f132d5d7faea7ca2311dcd8b473897.jpg?f=xxxl",
    name: "Bedroom",
    isOnline: true,
    lastTemperature: "24.5",
  },
  {
    image: "https://media.rbl.ms/image?u=%2Ffiles%2F2016%2F09%2F08%2F636089527843360677470268761_Tai.jpg&ho=https%3A%2F%2Faz616578.vo.msecnd.net&s=454&h=420d5c6b1289fcc29ca7fd7d2b64c70c16d2624c7a039ed0b065a50f207d74fe&size=980x&c=3012468181",
    name: "Garage",
    isOnline: true,
    lastTemperature: "23.5",
  },
  {
    image: "https://www.bhg.com/thmb/dcA2PxsOahxmk2LgzWAaqOWFfxU=/6000x0/filters:no_upscale():strip_icc()/200522-EB_12-Living-Room_1267-b13debcb440a4471981d7ac637e76e7a.jpg",
    name: "Living Room",
    isOnline: true,
    lastTemperature: "21.4",
  },
  {
    image: "https://cdn.apartmenttherapy.info/image/upload/v1554338269/project%20prism/color%20search%20archive/ea0aeabfe761190a4c6454cd512bdd51e0655219.jpg",
    name: "Kids Bedroom",
    isOnline: false,
    lastTemperature: "25.6",
  },
  {
    image: "https://www.casedesign.com/wp-content/uploads/2014/08/07_05_2013K_COPY.jpg",
    name: "Basement",
    isOnline: true,
    lastTemperature: "22.5",
  },
];

export default rooms;

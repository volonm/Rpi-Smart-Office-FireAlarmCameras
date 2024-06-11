import axios from "axios";


const API_KEY = '40416003-78cef6238b27f95b4490cfdb7';

export async function getImage(term: string) {
    try {
        const res = await axios.get('https://pixabay.com/api/', {
            params: {
                key: API_KEY,
                q: term,
            },
        });
        const imageURL = res.data.hits["0"].largeImageURL;
        console.log(res.data.hits[0]);
        return imageURL;

    } catch(error) {
        console.log("Error fetching images: ", error)
    }
}
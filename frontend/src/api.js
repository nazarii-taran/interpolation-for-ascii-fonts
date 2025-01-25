import axios from 'axios';

const origin = 'http://127.0.0.1:5000';

export const getAllFonts = async () => {
    try {
        const response = await axios.get(`${origin}/api/fonts`);

        return response.data;
    } catch (error) {
        console.error('Error fetching all fonts:', error);
    }
}

// one block === one ASCII character
// each block contains array of lines
export const getAsciiBlocks = async (text, scale, fontType, algorithm) => {
    try {
        const response = await axios.get(`${origin}/api/ascii-text?text=${text}&scale=${scale}&fontType=${fontType}&algorithm=${algorithm}`);
        
        return response.data;
    } catch (error) {
        console.error('Error getting ASCII text:', error);
    }
}

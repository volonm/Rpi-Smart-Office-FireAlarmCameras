import { Flex, FormControl, ChakraProvider, theme } from "@chakra-ui/react";
import * as React from "react";
import { ColorPicker } from "chakra-color-picker";

function ColorBox() {
    const handleColorChange = (value) => {
        console.log(value);
    };

    return (
        <ChakraProvider theme={theme}>
            <Flex pt="48" justify="center" align="center" w="full">
                <ColorPicker onChange={handleColorChange} />
            </Flex>
        </ChakraProvider>
    );
}

export default ColorBox;
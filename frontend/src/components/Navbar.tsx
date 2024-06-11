import React from 'react';
import {
    Avatar,
    Box,
    Button,
    Container,
    Flex,
    Heading,
    HStack,
    Spacer,
    Text,
    Input,
    Drawer,
    DrawerBody,
    DrawerFooter,
    DrawerHeader,
    DrawerOverlay,
    DrawerContent,
    DrawerCloseButton,
    useDisclosure,
    Stack,
    useBreakpointValue
} from "@chakra-ui/react";
import { useContext, useEffect, useState, } from "react";
import NavContents from './NavContents';
import { HamburgerIcon } from '@chakra-ui/icons';

const bgcolor = "#262626"

function Navbar() {
    const { isOpen, onOpen, onClose } = useDisclosure();

    const isMobile = useBreakpointValue({ base: true, md: false });


    return (
        <div>
            {!isMobile ? <Box backgroundColor="#262626">
                <Container maxWidth={1300} color="white">
                    <Flex
                        as="nav"
                        p="20px 0px"
                        alignItems="center"
                        justifyContent="space-between"
                    >
                        <Heading size="lg">Phoenix Alarm System</Heading>

                        <Spacer />

                        <Spacer></Spacer>

                        <HStack spacing="20px">

                            <NavContents />

                        </HStack>
                    </Flex>
                </Container>
            </Box> : <Box p={3} backgroundColor={bgcolor} color="white">
                <Button
                    aria-label='Options'
                    leftIcon={<HamburgerIcon />}
                    variant='outline'
                    onClick={onOpen}
                    color="inherit"
                >Menu</Button>
                <Drawer placement="right" onClose={onClose} isOpen={isOpen} colorScheme="gray">
                    <DrawerOverlay />
                    <DrawerContent>
                        <DrawerHeader borderBottomWidth='1px'>Basic Drawer</DrawerHeader>
                        <DrawerBody>
                            <Stack>
                                <NavContents />
                            </Stack>
                        </DrawerBody>
                    </DrawerContent>
                </Drawer>

            </Box>
            }</div >
    );



}

export default Navbar
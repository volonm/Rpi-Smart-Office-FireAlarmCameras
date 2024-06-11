import React from 'react';
import {
    Menu,
    MenuButton,
    MenuList,
    MenuItem,
    MenuItemOption,
    MenuGroup,
    MenuOptionGroup,
    MenuDivider,
    Button
} from '@chakra-ui/react'
import { ChevronDownIcon } from '@chakra-ui/icons';
import { useNavigate } from 'react-router-dom';

function MenuChoices() {

    const navigate = useNavigate();
    return (
        <Menu >
            <MenuButton as={Button} rightIcon={<ChevronDownIcon />} backgroundColor="#262626" color="white">
                Settings
            </MenuButton>
            <MenuList backgroundColor="#262626" borderColor="#262626">
                <MenuItem backgroundColor="#262626" onClick={() => navigate("/update")} color="white">Update Account</MenuItem>
                <MenuItem backgroundColor="#262626" onClick={() => navigate("/create-user")} color="white">Create User</MenuItem>
                <MenuItem backgroundColor="#262626" onClick={() => navigate("/cloud")} color="white">Cloud</MenuItem>
                <MenuItem backgroundColor="#262626" onClick={() => navigate("/users")} color="white">Users</MenuItem>
            </MenuList>
        </Menu >
    )
}

export default MenuChoices;
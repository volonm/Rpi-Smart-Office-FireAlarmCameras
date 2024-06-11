import {
    Table,
    Thead,
    Tbody,
    Tfoot,
    Tr,
    Th,
    Td,
    TableCaption,
    TableContainer,
} from '@chakra-ui/react'
import { User } from '../../context/AuthContext';
import { useEffect, useState } from 'react';
import api from '../../services/api';

function Users() {

    const [users, setUsers] = useState<User[]>();

    useEffect(() => {
        api.get("/auth/getUserDetails").then((res) => {
            console.log(res.data.users);
            setUsers(res.data.users)
        })
    }, [])

    return (
        <TableContainer>
            <Table size='sm'>
                <Thead>
                    <Tr>
                        <Th>User ID</Th>
                        <Th>Username</Th>
                        <Th>Email</Th>
                    </Tr>
                </Thead>
                <Tbody>
                    {users && users.map(user => {
                        return <Tr key={user.id}>
                            <Td>{user.id}</Td>
                            <Td>{user.username}</Td>
                            <Td>{user.email}</Td>
                        </Tr>
                    })}

                </Tbody>
                <Tfoot>
                    <Tr>
                        <Th>User ID</Th>
                        <Th>Username</Th>
                        <Th>Email</Th>
                    </Tr>
                </Tfoot>
            </Table>
        </TableContainer>
    )
}

export default Users
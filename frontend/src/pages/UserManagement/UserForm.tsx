import React, { useContext, useState } from 'react';
import {
    FormControl,
    FormLabel,
    FormErrorMessage,
    FormHelperText,
    Input,
    Button,
    Stack,
    Heading,
    Text
} from '@chakra-ui/react';
import { Form, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { updateMyInfo } from '../../services/auth-service';
import { AuthContext } from '../../context/AuthContext';

const schema = z.object({
    username: z.string().optional(),
    email: z.string().email().or(z.literal("")),
    password: z.string().min(1),
    new_password: z.string().or(z.literal("")),

});

function UserForm() {
    const { user } = useContext(AuthContext)
    const [error, setError] = useState("")
    const { register, handleSubmit, formState: { errors }, } = useForm({
        resolver: zodResolver(schema),
    });

    function onSubmit(data) {
        data.uid = user.id;
        return updateMyInfo(data).catch((err) => setError("Error occured, please try again"));
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <Stack spacing={3}>
                <Heading as='h3' noOfLines={1}>
                    Update my information
                </Heading>
                {/* Username */}
                <FormControl>
                    <FormLabel>Username</FormLabel>
                    <Input placeholder={user.username} {...register("username")} />
                    {errors.username?.message && <FormHelperText color="tomato">{errors.username?.message}</FormHelperText>}
                </FormControl>

                {/* Email */}
                <FormControl>
                    <FormLabel >Email address</FormLabel>
                    <Input placeholder={user.email} type='text' {...register("email")} />
                    {errors.email?.message && <FormHelperText color="tomato">{errors.email?.message}</FormHelperText>}
                </FormControl>

                {/* Password */}
                <FormControl isRequired>
                    <FormLabel>Password</FormLabel>
                    <Input placeholder="Password" type='password' {...register("password")} />
                    {errors.password?.message && <FormHelperText color="tomato">{errors.password?.message}</FormHelperText>}
                </FormControl>

                {/* Password */}
                <FormControl>
                    <FormLabel>New Password</FormLabel>
                    <Input placeholder="New Password" type='password' {...register("new_password")} />
                    {errors.new_password?.message && <FormHelperText color="tomato">{errors.new_password?.message}</FormHelperText>}
                </FormControl>
                {error && <Text color="tomato">{error}</Text>}
                {/* Create Button */}
                <Button colorScheme="teal" type="submit">
                    Create
                </Button>
            </Stack>
        </form>
    )
}

export default UserForm
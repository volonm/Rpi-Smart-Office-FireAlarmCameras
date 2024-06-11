import React from 'react';
import {
    FormControl,
    FormLabel,
    FormErrorMessage,
    FormHelperText,
    Input,
    Button,
    Stack,
    Heading
} from '@chakra-ui/react';
import { Form, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import api from '../../services/api';

const schema = z.object({
    server: z.string(),
    database: z.string(),
    user: z.string(),
    password: z.string(),
    driver: z.string(),
    connection_string: z.string(),
    container_name: z.string(),

});


function CloudForm() {

    const { register, handleSubmit, formState: { errors }, } = useForm({
        resolver: zodResolver(schema),
    });

    const schemaKeys = Object.keys(schema.shape);

    function onSubmit(data) {
        api.post("", data);
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)}>
            <Stack spacing={3}>
                <Heading as='h3' noOfLines={1}>
                    Configure Cloud Server
                </Heading>

                {schemaKeys.map((key, index) => (
                    <FormControl key={index} isRequired>
                        <FormLabel>{key}</FormLabel>
                        <Input placeholder={key} {...register(key)} />
                    </FormControl>
                ))}

                <Button colorScheme="facebook" type="submit">
                    Set Up
                </Button>

            </Stack>
        </form>
    )
}

export default CloudForm
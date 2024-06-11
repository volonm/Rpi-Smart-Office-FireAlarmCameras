import {
  Button,
  FormControl,
  Input,
  InputGroup,
  Text,
  useToast,
} from "@chakra-ui/react";
import { useState } from "react";
import { getAuthToken } from "../services/user-service.ts";

interface Props {
  requestEmailCode: (token: string) => void;
  checkEmailCode: (emailCode: string) => void;
  error: string;
}

function CodeInput({ requestEmailCode, checkEmailCode, error }: Props) {
  const [emailCode, setEmailCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) =>
    setEmailCode(event.target.value);

  const handleRequestEmailCode = () => {
    setIsLoading(true);
    toast({
      title: "Email sent!.",
      description: "Please check your inbox for the code",
      status: "success",
      duration: 9000,
      isClosable: true,
    });
    setTimeout(() => {
      setIsLoading(false);
    }, 5000); // 5000 milliseconds = 5 seconds
    requestEmailCode(getAuthToken()!);
  };

  return (
    <>
      <FormControl>
        <Text mb={2}>Email Verification</Text>
        <InputGroup>
          <Input
            value={emailCode}
            onChange={handleChange}
            type="text"
            placeholder="Email Code"
          />
        </InputGroup>
      </FormControl>
      {error && <Text color="tomato">{error}</Text>}
      <Button
        isLoading={isLoading}
        colorScheme="green"
        onClick={handleRequestEmailCode}
      >
        Request New Code
      </Button>
      <Button colorScheme="orange" onClick={() => checkEmailCode(emailCode)}>
        Check Code
      </Button>
    </>
  );
}

export default CodeInput;

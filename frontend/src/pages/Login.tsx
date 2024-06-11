import { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { Navigate, useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Card,
  CardBody,
  Center,
  chakra,
  FormControl,
  Input,
  InputGroup,
  InputLeftElement,
  InputRightElement,
  Stack,
  Text,
} from "@chakra-ui/react";
import { useForm } from "react-hook-form";
import { FaLock, FaUserAlt } from "react-icons/fa";
import {
  getUserByToken,
  login,
  requestCode,
  sendEmailCode,
} from "../services/auth-service";
import {
  getAuthToken,
  setAuthToken,
  setSessionToken,
} from "../services/user-service";
import CodeInput from "../components/CodeInput.tsx";

const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

interface FormData {
  username: string;
  password: string;
}

function Login() {
  // Form State
  const { register, handleSubmit } = useForm<FormData>();

  // Component State
  const [showPassword, setShowPassword] = useState(true);
  const [showCodeInput, setShowCodeInput] = useState(false);
  const [error, setError] = useState("");

  // Auth Context
  const { setUser, authenticated } = useContext(AuthContext);

  // Navigate Initialization
  const navigate = useNavigate();

  useEffect(() => {
    if (getAuthToken() != null) {
      setShowCodeInput(true);
    }
  }, []);

  if (authenticated) return <Navigate to={"/"} />;

  // Requests a code to be sent to email
  function requestEmailCode(token: string) {
    requestCode(token)
      .then(() => console.log("Email Code Sent, Please Wait"))
      .catch((err) => {
        setError("Error with sending email code");
        console.log(err.message);
      });
  }

  function checkEmailCode(emailCode: string) {
    sendEmailCode(emailCode)
      .then((data) => {
        const session = data.session;
        setSessionToken(session);
        const token = getAuthToken();
        if (token && session) {
          getUserByToken(token, session).then((user) => {
            setUser(user);
            return navigate("/");
          });
        }
      })
      .catch((err) => {
        setError("Error validating verification code");
        console.log(err.message);
      });
  }

  // if (authenticated) return <Navigate to="/" replace/>;

  function onSubmit({ username, password }: FormData) {
    setError("");
    if (!username || !password) {
      return setError("Please enter all fields");
    }

    login(username, password)
      .then((data) => {
        setAuthToken(data.token);
        setShowCodeInput(true);
      })
      .catch((err) => {
        setError("Wrong username or password");
        console.log(err.message);
      });
  }

  return (
    <Box backgroundColor="gray.100" w="100vw" h="100vh">
      <Center w="100vw" h="50vh">
        <Card width={80}>
          <CardBody>
            <form onSubmit={handleSubmit(onSubmit)}>
              <Stack spacing={3}>
                {!showCodeInput ? (
                  <>
                    {/* Username */}
                    <FormControl>
                      <InputGroup>
                        <InputLeftElement
                          pointerEvents="none"
                          children={<CFaUserAlt color="gray.300" />}
                        />
                        <Input
                          type="text"
                          placeholder="Username"
                          {...register("username")}
                        />
                      </InputGroup>
                    </FormControl>

                    {/* Password */}
                    <FormControl>
                      <InputGroup>
                        <InputLeftElement
                          pointerEvents="none"
                          color="gray.300"
                          children={<CFaLock color="gray.300" />}
                        />
                        <Input
                          type={showPassword ? "text" : "password"}
                          placeholder="Password"
                          {...register("password")}
                        />
                        <InputRightElement width="4.5rem">
                          <Button
                            h="1.75rem"
                            size="sm"
                            onClick={() => setShowPassword(!showPassword)}
                          >
                            {showPassword ? "Hide" : "Show"}
                          </Button>
                        </InputRightElement>
                      </InputGroup>
                    </FormControl>

                    {/* Print Errors */}
                    {error && <Text color="tomato">{error}</Text>}

                    {/* Submit */}
                    <Button colorScheme="orange" type="submit">
                      Login
                    </Button>
                  </>
                ) : (
                  <CodeInput
                    requestEmailCode={requestEmailCode}
                    checkEmailCode={checkEmailCode}
                    error={error}
                  />
                )}
              </Stack>
            </form>
          </CardBody>
        </Card>
      </Center>
    </Box>
  );
}

export default Login;

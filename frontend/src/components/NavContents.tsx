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
} from "@chakra-ui/react";
import { useContext, useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext.tsx";
import logo from "./logo.png";
import api from "../services/api.ts";
import MenuChoices from "./MenuChoices.tsx";

function NavContents() {
  const navigate = useNavigate();
  const { setUser, user } = useContext(AuthContext);
  const [status, setStatus] = useState(false);

  function stopAlert() {
    api.post("sensors/stopAlert").then(() => setStatus(false));
  }

  function fetchAlertStatus() {
    api
      .get("/sensors/getSysStatus")
      .then((res) => setStatus(res.data["alertStatus"]));

    console.log("Fetched status");
  }

  useEffect(() => {
    fetchAlertStatus();

    const intervalId = setInterval(fetchAlertStatus, 60000); // Execute fetchData every 1 minute

    return () => clearInterval(intervalId);
  }, []);

  return (
    <>
      <Button
        colorScheme={status ? "red" : "green"}
        onClick={() => {
          stopAlert();
        }}
      >
        {status ? "System alert " : "No alert "}
      </Button>
      <Text>{user && user.email}</Text>
      <MenuChoices />
      <Button
        color="inherit"
        backgroundColor="inherit"
        onClick={() => {
          localStorage.removeItem("token");
          localStorage.removeItem("session");
          setUser(undefined);
          navigate("/login");
        }}
      >
        Logout
      </Button>
      <Avatar name="Logo" src={logo} />
    </>
  );
}

export default NavContents;

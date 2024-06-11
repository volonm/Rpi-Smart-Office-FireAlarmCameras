import { useContext } from "react";
import { AuthContext } from "./context/AuthContext";
import { Navigate, Outlet, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Home from "./pages/Home/Home";
import { Box, Container } from "@chakra-ui/react";
import NavContents from "./components/NavContents";
import RoomLogs from "./pages/RoomLogs/RoomLogs";
import Navbar from "./components/Navbar";
import CloudForm from "./pages/Cloud/CloudForm";
import UserForm from "./pages/UserManagement/UserForm";
import Users from "./pages/UserManagement/Users";
import AddUser from "./pages/UserManagement/AddUser";

function PrivateRoutes() {
  const { authenticated } = useContext(AuthContext);

  if (!authenticated) return <Navigate to="/login" replace />;

  return (
    <Box>
      <Navbar />
      <Container maxWidth={1300} mt={12}>
        <Outlet />
      </Container>
    </Box>
  );
}

function Routing() {
  return (
    <div>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<PrivateRoutes />}>
          <Route path="/" element={<Home />} />
          <Route path="/logs" element={<RoomLogs />} />
          <Route path="/update" element={<UserForm />} />
          <Route path="/cloud" element={<CloudForm />} />
          <Route path="/users" element={<Users />} />
          <Route path="/create-user" element={<AddUser />} />
        </Route>
      </Routes>
    </div>
  );
}

export default Routing;

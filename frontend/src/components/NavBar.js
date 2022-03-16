/*Code taken from: https://mui.com/components/app-bar/#ResponsiveAppBar.js and modified*/


import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import {Link, useHistory} from "react-router-dom";
import {useLocation} from 'react-router-dom';
import "./NavBar.css"
import requests from '../requests';


const pages = ['Home', 'Friends', 'My Profile', 'Post', 'Public Posts'];
const settings = ['Profile Settings', 'Logout'];
const links = {"Home": "./inbox", "Friends": "./friends", "My Profile": "./profile", "Post": "./post", "Public Posts": "./public_posts"}
requests.defaults.headers["Authorization"] = localStorage.getItem('access_token');

const NavBar = () => {
  const history = useHistory();
  const currentPath = "." + useLocation()["pathname"];
  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [anchorElUser, setAnchorElUser] = React.useState(null);
  
  React.useState(function checkAuthenticated() {
    // TODO check and simplify this to for expired accessToken
    const accessToken = localStorage.getItem("access_token");
    if (!accessToken) {
        history.push("/");
        history.go(0);
    }
    // const response = requests.get('get-user/', {headers: {
    //   accept: 'application/json',
    // }}).then(data => {
    //   if (data.status != 200) {
    //     history.push("/");
    //   }
    // }
    // );
    // if (!accessToken || status_code != 200) {
    //   console.log(status_code);
    //   console.log("HERE");
    //   history.push("/");
    // }
  });

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const logout = async () => {
    // send POST request to /logout
    try {
      const response = await requests.post('logout/', {headers: {
        accept: 'application/json',
      }});
    } 
    catch(error) {
      console.log(error);
    }
    localStorage.removeItem("access_token");
    history.push("/")
  }

  const handleCloseUserMenu = (e) => {
    // Handles the selected option
    let selectedOption = e.currentTarget.innerText
    switch(selectedOption) {
      case "Profile Settings":
        history.push('/profile');
        break;
      case "Logout":
        logout();
        break;
    }
    setAnchorElUser(null);
  };


  /* todo
    -move nav bar options to left

  */

  return (
    <AppBar position="static" >
      <Container maxWidth="100%" >
        <Toolbar disableGutters>
          {/* NOTE: un-comment this out if we need a logo in the nav bar

          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ mr: 2, display: { xs: 'none', md: 'flex' } }}
          >
            LOGO
          </Typography>
          
          */}

          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {pages.map((page) => (
                <Link className="navLink" to={links[page]}>
                <MenuItem key={page} onClick={handleCloseNavMenu}>
                  <Typography 
                    textAlign="center" 
                    sx={links[page] === currentPath ? {my: 2, color: "black", display: 'block', fontWeight: "bold"} : {my: 2, color: "rgba(0, 0, 0, 0.5)", display: 'block'}}
                  >
                    {page}
                  </Typography>
                </MenuItem>
                </Link>
              ))}
            </Menu>
          </Box>
          {/* NOTE: un-comment this out if we need a logo in the nav bar
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}
          >
            LOGO
          </Typography>
          */}
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' }, }}>
            {pages.map((page) => (
              <Link className="navLink" to={links[page]}>
                <Button 
                  key={page}
                  onClick={handleCloseNavMenu}
                  sx={links[page] === currentPath ? {my: 2, color: "white", display: 'block', fontWeight: "bold"} : {my: 2, color: "rgba(255, 255, 255, 0.5)", display: 'block'}}
                >
                  {page}
                </Button>
              </Link>
            ))}
          </Box>

          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <Avatar alt="user" src="" />
              </IconButton>
            </Tooltip>
            <Menu
              sx={{ mt: '45px' }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
              {settings.map((setting) => (
                <MenuItem key={setting} onClick={handleCloseUserMenu}>
                  <Typography textAlign="center">{setting}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};
export default NavBar;

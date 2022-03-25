import React, {useState} from "react";
import requests from "../../requests";

import { Alert,
        Avatar,
        Button,
        ListItem,
        ListItemAvatar,
        ListItemText,
        ListItemSecondaryAction,
        } from "@mui/material";
import ClearIcon from '@mui/icons-material/Clear'
import getUuidFromAuthorUrl, { getAuthHeaderForNode } from "../../util"

// assuming props contains all the author attributes of the follower, and the id of the current user
export default function Following(props) {
    const [message, setMessage] = useState({});

    const unfollow = async () => {
        // send DELETE request to
        try {
          var url = props.id + "/followers/";
          url = url + getUuidFromAuthorUrl(props.currentUserId);
          const response = await requests.delete(url,
          getAuthHeaderForNode(url),
            {withCredentials: true});
          setMessage({message: "Unfollowed.", severity: "success"});
        } catch {
          setMessage({message: "Failed to unfollow.", severity: "error"});
        }   
    }
    return (
      <ListItem divider>
        {message.message && (
        <Alert severity={message.severity}>
          {message.message}
        </Alert>
        )}
        <ListItemAvatar>
          <Avatar
          src={props.profileImage}
          />
        </ListItemAvatar>
        <ListItemText
          primary={props.displayName}
        />
        <ListItemSecondaryAction>
          <Button 
            startIcon={<ClearIcon />}
            onClick={unfollow}>
              Unfollow
          </Button>
        </ListItemSecondaryAction>
      </ListItem>
    );
}
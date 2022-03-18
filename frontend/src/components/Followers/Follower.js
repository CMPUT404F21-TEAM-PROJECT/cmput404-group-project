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

// assuming props contains all the author attributes of the follower, and the id of the current user
export default function Follower(props) {
    const [message, setMessage] = useState({});

    const removeFollower = async () => {
        // send DELETE request to author_id/followers/follower_id
        try {
          const response = await requests.delete(`authors/${props.currentUserId}/followers/${props.id}/`,
          {headers: {
                Authorization: localStorage.getItem('access_token'),
                accept: 'application/json',
          }},
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
            onClick={removeFollower}>
              Remove
          </Button>
        </ListItemSecondaryAction>
      </ListItem>
    );
}
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
export default function Following(props) {
    const [error, setError] = useState("");

    const unfollow = async () => {
        // send DELETE request to
        try {
          const response = await requests.delete(`service/authors/${props.id}/followers/${props.currentUserId}/`,
          {headers: {
            Authorization: localStorage.getItem('access_token'),
            accept: 'application/json',
            }},
            {withCredentials: true});
        } catch {
          setError("Failed to unfollow.");
        }   
    }
    return (
      <ListItem divider>
        {error && (
        <Alert severity="error">
          {error}
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
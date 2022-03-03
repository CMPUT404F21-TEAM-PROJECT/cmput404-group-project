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
import CheckIcon from '@mui/icons-material/Check'

// assuming props contains all the author attributes of the person who
// sent the follow request, and the id of the current user
export default function FollowRequest(props) {
    const [error, setError] = useState("");

    const acceptFollowRequest = async () => {
        // send PUT request to author_id/followers/follower_id
        console.log('clicked accept');
        try {
          const response = await requests.put(`service/authors/${props.currentUser}/followers/${props.id}/`,
          {headers: {
            Authorization: localStorage.getItem('access_token'),
            accept: 'application/json',
          }},
          {withCredentials: true});
        } catch {
          setError("Failed to accept follow request.");
        }   
    }


    const rejectFollowRequest = async () => {
        // send DELETE request to author_id/followers/follower_id
        console.log('clicked reject')
        try {
          const response = await requests.delete(`service/authors/${props.currentUser}/followers/${props.id}/`,
          {headers: {
            Authorization: localStorage.getItem('access_token'),
            accept: 'application/json',
          }},
          {withCredentials: true});
        } catch {
          setError("Failed to reject follow request.");
        }   
    }
    return (
      <ListItem>
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
            startIcon={<CheckIcon />}
            onClick={acceptFollowRequest}>
              Accept
          </Button>
          <Button 
            startIcon={<ClearIcon />}
            onClick={rejectFollowRequest}>
              Reject
          </Button>
        </ListItemSecondaryAction>
      </ListItem>
    );
}
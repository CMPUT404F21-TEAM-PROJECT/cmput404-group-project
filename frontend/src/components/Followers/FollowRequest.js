import React, {useState, useEffect} from "react";
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
    const [message, setMessage] = useState({});
    const [accepted, setAccepted] = useState(false);

    const acceptFollowRequest = async () => {
        // send PUT request to author_id/followers/follower_id
        console.log('clicked accept');
        try {
          const response = await requests.put(`authors/${props.currentUserId}/followers/${props.id}/`,
          {headers: {
            Authorization: localStorage.getItem('access_token'),
            accept: 'application/json',
          }},
          {withCredentials: true});
          setMessage({message: "Accepted follow request.", severity: "success"});
        } catch {
          setMessage({message: "Failed to accept follow request.", severity: "error"});
        }   
    }


    const rejectFollowRequest = async () => {
        // send DELETE request to author_id/followers/follower_id
        console.log('clicked reject')
        try {
          const response = await requests.delete(`authors/${props.currentUserId}/followers/${props.id}/`,
          {headers: {
            Authorization: localStorage.getItem('access_token'),
            accept: 'application/json',
          }},
          {withCredentials: true});
          setMessage({message: "Rejected follow request.", severity: "success"});
        } catch {
          setMessage({message: "Failed to reject follow request.", severity: "error"});
        }   
    }
    useEffect(() => {
      setAccepted(props.accepted);
    }, [])

    return (
      <ListItem>
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
        {accepted ? (<ListItemText primary={"You accepted " + props.displayName + "\'s follow request"}/>)  
            : (<ListItemText primary={props.displayName + " wants to follow you"}
        />)}
        {!accepted && <ListItemSecondaryAction>
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
        </ListItemSecondaryAction>}
      </ListItem>
    );
}
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
    const [error, setError] = useState("");

    const removeFollower = async () => {
        // send DELETE request to author_id/followers/follower_id
        console.log('clicked remove')
        try {
          const response = await requests.delete(`service/authors/${props.currentUser}/follwers/${props.id}/`);
        } catch {
          setError("Failed to remove follower.");
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
            startIcon={<ClearIcon />}
            onClick={removeFollower}>
              Remove
          </Button>
        </ListItemSecondaryAction>
      </ListItem>
    );
}
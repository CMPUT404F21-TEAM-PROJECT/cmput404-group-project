import React from "react";
import requests from "../../requests";

import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import ListItemSecondaryAction from "@material-ui/core/ListItemSecondaryAction";
import CheckIcon from '@mui/icons-material/Check';
import ClearIcon from '@mui/icons-material/Clear';

export default function FollowRequest(props) {

    function acceptFollowRequest() {
        // send PUT request to author_id/followers/follower_id
        console.log('clicked accept')
    }

    function rejectFollowRequest() {
        // send DELETE request to author_id/followers/follower_id
        console.log('clicked reject')
    }
    return (
      <ListItem>
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
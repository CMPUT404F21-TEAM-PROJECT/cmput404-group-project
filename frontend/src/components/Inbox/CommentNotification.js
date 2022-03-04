import React, {useState} from "react";

import { Alert,
        Avatar,
        ListItem,
        ListItemAvatar,
        ListItemText,
        } from "@mui/material";

// like notification that appears in the inbox
export default function CommentNotification(props) {

    return (
      <ListItem button component="a" href={props.id}>
        <ListItemAvatar>
          <Avatar
          src={props.profileImage}
          />
        </ListItemAvatar>
        <ListItemText primary={props.displayName + ' commented on your post'} />
      </ListItem>
    );
}
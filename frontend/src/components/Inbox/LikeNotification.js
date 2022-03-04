import React, {useState} from "react";

import { Alert,
        Avatar,
        ListItem,
        ListItemAvatar,
        ListItemText,
        } from "@mui/material";
import FavoriteIcon from '@mui/icons-material/Favorite';

// like notification that appears in the inbox
export default function LikeNotification(props) {

    return (
      <ListItem button component="a" href={props.object}>
        <ListItemAvatar>
          <Avatar
          src={props.profileImage}
          />
        </ListItemAvatar>
        <ListItemText primary={props.summary}/>
      </ListItem>
    );
}
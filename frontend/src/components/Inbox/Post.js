import React, {useState} from "react";
import requests from "../../requests";
import './Post.css'

import { Alert,
        Avatar,
        Button,
        ListItem,
        ListItemAvatar,
        ListItemText,
        ListItemSecondaryAction,
        ImageListItem,
        TextField,
        } from "@mui/material";
import ThumbUp from '@mui/icons-material/ThumbUp'
import Send from '@mui/icons-material/Send'

// assuming props contains all the post attributes
export default function Post(props) {
    const [error, setError] = useState("");
    const [commentText, setCommentText] = useState("")

    const styles = theme => ({
        listItemText:{
          fontSize: '1',
        }
      });

    const like = async () => {
        // send POST request to authors/{authorId}/inbox/ with a like
        console.log('clicked like');
        try {
          const response = await requests.post(`service/authors/${props.currentUser}/inbox/`,
          {headers: {
            Authorization: localStorage.getItem('access_token'),
            accept: 'application/json',
          },
          summary: props.author.displayName + " likes your post.",
          type: "Like",
          author: props.author,
          object: props.author.id + "/posts/" + props.post.id
          },
          {withCredentials: true});
        } catch {
          setError("Failed to send like.");
        }   
    }


    const comment = async () => {
        // send POST request to authors/{authorId}/posts/{postId}/comments/ with a comment
        console.log('clicked comment')
        //try {
            const response = await requests.post(`service/authors/${props.currentUser}/posts/${props.post.id}/comments/`,
            {
            post_id: props.post.id,
            comment: commentText,
            contentType: "text/markdown",
            author: props.author
            },
            {headers: {
                Authorization: localStorage.getItem('access_token'),
                accept: 'application/json',
              }
            },
            {withCredentials: true});
        /*} catch {
          setError("Failed to send comment.");
        } */  
    }
    return (
      <ListItem>
        <ListItemText
          id="title"
          primaryTypographyProps={{fontSize: '30px'}}
          primary={props.title}
        />
        <ListItemText
          id="author"
          primary={"By: " + props.author.displayName}
        />
        {(props.contentType == "text/markdown" || props.contentType == "text/plain") && <ListItemText
          primary={props.content}
        />}
        {(props.contentType == "application/base64" || props.contentType == "image/png;base64" || props.contentType == "image/jpeg;base64") && <ImageListItem
          children={<img src={props.content}></img>}
        />}
        <ListItemText
          id="description"
          primary={props.description}
        />
        <div id="comment-like-section">
            <Button 
            id="like-button"
            startIcon={<ThumbUp />}
            onClick={like}>
                Like
            </Button>
            <span id="comment-section">
                <TextField id="commentBox" label="Comment" variant="filled" defaultValue="" onChange={e => {setCommentText(e.target.value)}}/>
                <Button
                id="comment-button" 
                startIcon={<Send />}
                onClick={comment}>
                    Comment
                </Button>
            </span>
        </div>
      </ListItem>
    );
}
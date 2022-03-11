import React, {useState, useEffect} from "react";
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
import ReactMarkdown from 'react-markdown'
import ThumbUp from '@mui/icons-material/ThumbUp'
import Send from '@mui/icons-material/Send'

// assuming props contains all the post attributes
export default function Post(props) {
    const [error, setError] = useState("");
    const [commentText, setCommentText] = useState("")
    const [liked, setLiked] = useState(false)

    const styles = theme => ({
        listItemText:{
          fontSize: '1',
        }
      });

    const like = async () => {
        // send POST request to authors/{authorId}/inbox/ with a like
        try {
          const data = {
            summary: `${props.currentUser.displayName} likes your post.`,
            type: "Like",
            author: props.currentUser.id,
            _object: `${props.author.id}/posts/${props.post.id}`
          }
          // prevents sending a like twice when liking your own post
          if (props.currentUser.id != props.author.id){
            const response = await requests.post(`service/authors/${props.author.id}/inbox/`,
              data,
              {headers: {
                Authorization: localStorage.getItem('access_token'),
                accept: 'application/json',
              }},
              {withCredentials: true});
          }
          
          // change summary of like, to send like to your own inbox
          data.summary = `You liked ${props.author.displayName}'s post.`
          sendToSelf(data);
         setLiked(true)
        } catch (e) {
          console.log(e)
          setError("Failed to send like.");
        }   
    }

    const comment = async () => {
        // send POST request to authors/{authorId}/posts/{postId}/comments/ with a comment
        try {
            const response = await requests.post(`service/authors/${props.author.id}/posts/${props.post.id}/comments/`,
              {
              post_id: props.post.id,
              comment: commentText,
              contentType: "text/markdown",
              author: props.currentUser.id,
              type: "comment"
              },
              {headers: {
                  Authorization: localStorage.getItem('access_token'),
                  accept: 'application/json',
                }
              },
              {withCredentials: true});
            sendToSelf(response.data);
            // send to recipients inbox
            const response_recipient = await requests.post(`service/authors/${props.author.id}/inbox/`,
            response.data,
            {headers: {
              Authorization: localStorage.getItem('access_token'),
              accept: 'application/json',
            }
            },
          {withCredentials: true})
        } catch(e) {
          setError("Failed to send comment.");
          console.log(e)
        }   
    }
  
    const sendToSelf = async (my_item) => {
      const response_self = await requests.post(
        `service/authors/${props.currentUser.id}/inbox/`,
        my_item,
        {headers: {
          Authorization: localStorage.getItem('access_token'),
          accept: 'application/json',
        }},
        {withCredentials:true});
    };

    useEffect(() => {
      setLiked(props.likedByCurrent);
    }, [])

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
        {props.contentType == "text/markdown" && <ReactMarkdown>
          {props.content}
          </ReactMarkdown>}
        {(props.contentType == "text/plain") && <ListItemText
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
        {liked ? (<Button
                    disabled
                    variant="contained">
                      Liked
                    </Button>)  
            : (<Button 
              id="like-button"
              startIcon={<ThumbUp />}
              onClick={like}>
                  Like
              </Button>)}
            
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
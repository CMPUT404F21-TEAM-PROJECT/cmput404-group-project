import React, {useState, useEffect} from "react";
import requests from "../../requests";
import CommentDialogButton from "../Posts/CommentDialog";
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
import ShareIcon from '@mui/icons-material/Share';
import { ClassNames } from "@emotion/react";

// assuming props contains all the post attributes
export default function Post(props) {
  const [message, setMessage] = useState({});
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
            object: `${props.post.author.id}/posts/${props.post.id}`
          }
          // prevents sending a like twice when liking your own post
          if (props.currentUser.id != props.post.author.id){
            const response = await requests.post(`authors/${props.post.author.id}/inbox/`,
              data,
              {headers: {
                Authorization: localStorage.getItem('access_token'),
                accept: 'application/json',
              }},
              {withCredentials: true});
          }
          
          // change summary of like, to send like to your own inbox
          data.summary = `You liked ${props.post.author.displayName}'s post.`
          sendToSelf(data);
         setLiked(true)
        } catch (e) {
          console.log(e)
          setMessage({message: "Failed to send like.", severity: "error"});
        }   
    }

    const share = async () => {
      try {
        // if post is public, send to followers
        if (props.isPublic) {
          // add type to data
          props.post.type = 'post'
          sendToFollowers(props.post);
        // if post is private, make a copy then send to followers
        } else {
          const url = "authors/" + props.currentUser.id + "/posts/";
          const response = await requests.post(url, {
          headers: {
            accept: "application/json",
          },
          title: props.post.title,
          author: props.currentUser.id,
          contentType: props.post.contentType,
          content: props.post.content,
          description: props.post.description,
          visibility: props.post.visibility,
          unlisted: props.post.unlisted,
          categories: props.post.categories,
          viewableBy: '',
        });

        response.data.type = 'post'
        sendToSelf(response.data)
        sendToFollowers(response.data);
        }
      setMessage({message: "Shared post to followers.", severity: "success"});
      } catch(e) {
        setMessage({message: "Failed to share post.", severity: "error"});
      }

    }

    const sendToFollowers = async (my_post) => {
      // Get Followers
      const response = await requests.get(
        `authors/${props.currentUser.id}/followers/`
      );
      const followerList = response.data.items;
  
      // For each follower: send post to inbox
      for (let index = 0; index < followerList.length; ++index) {
        const follower = followerList[index];
        await requests.post(
          `authors/${follower.id}/inbox/`,
          my_post,
          {headers: {
            Authorization: localStorage.getItem('access_token'),
            accept: 'application/json',
          }},
          {withCredentials:true});
      }
    };
  
    // send a like or comment notification to your own inbox
    const sendToSelf = async (my_item) => {
      const response_self = await requests.post(
        `authors/${props.currentUser.id}/inbox/`,
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
          primary={props.post.title}
        />
        <ListItemText
          id="author"
          primary={"By: " + props.post.author.displayName}
        />
        {props.post.contentType == "text/markdown" && <ReactMarkdown>
          {props.post.content}
          </ReactMarkdown>}
        {(props.post.contentType == "text/plain") && <ListItemText
          primary={props.post.content}
        />}
        {(props.post.contentType == "application/base64" || props.post.contentType == "image/png;base64" || props.post.contentType == "image/jpeg;base64") && <ImageListItem
          children={<img src={props.post.content}></img>}
        />}
        <ListItemText
          id="description"
          primary={props.post.description}
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
                <CommentDialogButton
                current_author = {props.currentUser.id}
                post_id = {props.post.id}
                author_id = {props.post.author}/>
            </span>
            <span id="share-section">
              <Button
                variant="contained"
                startIcon={<ShareIcon />}
                onClick={share}>
                  Share
              </Button>
            </span>
        {message.message && (
        <Alert severity={message.severity}>
          {message.message}
        </Alert>
        )}
        </div>
      </ListItem>
    );
}
import React, {useState, useEffect} from "react";
import requests from "../../requests";
import CommentDialogButton from "./CommentDialog";
import './Post.css'
import {utcToLocal} from "../../date"
import EditPost from './EditPostDialog';

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
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { ClassNames } from "@emotion/react";
import { Link } from 'react-router-dom';
import { getAuthHeaderForNode } from "../../util";


// assuming props contains all the post attributes
export default function Post(props) {
  const [message, setMessage] = useState({});
    const [commentText, setCommentText] = useState("")
    const [liked, setLiked] = useState(false)

    const like = async () => {
        // send POST request to authors/{authorId}/inbox/ with a like
        try {
          const data = {
            summary: `${props.currentUser.displayName} likes your post.`,
            type: "Like",
            author: props.currentUser.id,
            object: `${props.post.id}`
          }
          // prevents sending a like twice when liking your own post
          if (props.currentUser.id != props.post.author.id){
            const url = `${props.post.author.id}/inbox/`;
            const response = await requests.post(url,
              data,
              getAuthHeaderForNode(url),
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
          const url = props.currentUser.id + "/posts/";
          const response = await requests.post(url, {
          title: props.post.title,
          author: props.currentUser.id,
          contentType: props.post.contentType,
          content: props.post.content,
          description: props.post.description,
          visibility: props.post.visibility,
          unlisted: props.post.unlisted,
          categories: props.post.categories,
          viewableBy: '',
        }, getAuthHeaderForNode(url));

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
        `${props.currentUser.id}/followers/`
      );
      const followerList = response.data.items;
  
      // For each follower: send post to inbox
      for (let index = 0; index < followerList.length; ++index) {
        const follower = followerList[index];
        const url = `${follower.id}/inbox/`;
        await requests.post(
          url,
          my_post,
          getAuthHeaderForNode(url),
          {withCredentials:true});
      }
    };
  
    // send a like or comment notification to your own inbox
    const sendToSelf = async (my_item) => {
      const url = `${props.currentUser.id}/inbox/`;
      const response_self = await requests.post(
        url,
        my_item,
        getAuthHeaderForNode(url),
        {withCredentials:true});
    };



    const deletePost = async () => {
      if (window.confirm("Do you really want to delete this post?")) {
        // Send DELETE request to authors/{AUTHOR_ID}/posts/{POST_ID}
        // let authorID = props.post.author.id;
        let postID = props.post.id;
        let url = `${postID}/`;
        const response = await requests.delete(url);
        window.location.reload();
      }
    }

    useEffect(() => {
      setLiked(props.likedByCurrent);
    }, [])

    return (
      <ListItem class="post">
        <ListItemText
          id="title"
          primaryTypographyProps={{fontSize: '30px'}}
          primary={props.post.title}
        />
        <div class="avatar">
          <ListItemAvatar>
            <Avatar alt="" src={`${props.post.author.profileImage}`} />
          </ListItemAvatar>
          <ListItemText
            id="author"
            primary={props.post.author.displayName}
            secondary={utcToLocal(props.post.published)}
          />
        </div>
        {props.post.contentType == "text/markdown" && <ReactMarkdown>
          {props.post.content}
          </ReactMarkdown>}
        {(props.post.contentType == "text/plain") && <ListItemText
          primary={props.post.content}
        />}
        {(props.post.contentType == "application/base64" || props.post.contentType == "image/png;base64" || props.post.contentType == "image/jpeg;base64") && <ImageListItem
          children={<img src={props.post.content}></img>}
        />}
        {props.post.contentType == "text/markdown" && <ReactMarkdown>
          {props.post.description}
          </ReactMarkdown>}
        {props.post.contentType != "text/markdown" && <ListItemText
          id="description"
          primary={props.post.description}
        />}
        <hr/>
        <div id="comment-like-section">
        {liked ? (<Button
                    disabled
                    variant="contained">
                      Liked
                    </Button>)  
            : (<Button 
              id="like-button"
              variant="contained"
              color="success"
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
            <div id="edit-section" hidden={props.post.author.id === props.currentUser.id ? false : true}> 
              <EditPost 
                current_author = {props.currentUser.id}
                post = {props.post}/>
            </div>
            <div id="delete-section" hidden={props.post.author.id === props.currentUser.id ? false : true}>
              <Button
                variant="contained"
                color="error"
                startIcon={<DeleteIcon/>}
                onClick={deletePost}
              >
                Delete
              </Button>
            </div>
        {message.message && (
        <Alert severity={message.severity}>
          {message.message}
        </Alert>
        )}
        </div>
        <ListItemText
          id="post-id"
          secondary={<p>Post Id: <a href={props.post.id}>{props.post.id}</a></p>}
        />
      </ListItem>
    );
}
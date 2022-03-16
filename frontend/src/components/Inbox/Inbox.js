import React from "react";
import requests from "../../requests";
import { Alert, Button, List, Grid, Box, TextField, Stack, ListItemText } from "@mui/material";
import FollowRequest from "../Followers/FollowRequest";
import LikeNotification from "./LikeNotification";
import CommentNotification from "./CommentNotification";
import Post from "./Post";
import DeleteIcon from '@mui/icons-material/Delete';

  
class Inbox extends React.Component {
  constructor(props){
    super(props);
    this.state = {
        currentUser: {},
        inboxList: [],
    }
}

  componentDidMount() {
      this.initializeDetails();
  }

  initializeDetails = async () => {
      try {
          // Get the author details
          const response = await requests.get('get-user/', {headers: {
              Authorization: localStorage.getItem('access_token'),
              accept: 'application/json',
          }});

          this.setState({ currentUser: {
            id: response.data.id ? response.data.id : '',
            url: response.data.url ? response.data.url : '',
            host: response.data.host ? response.data.host : '',
            displayName: response.data.displayName ? response.data.displayName : '',
            github: response.data.github ? response.data.github : '',
            profileImage: response.data.profileImage ? response.data.profileImage : ''
          }});

          const response_inbox = await requests.get(`authors/${this.state.currentUser.id}/inbox/`,
            {headers: {
              Authorization: localStorage.getItem('access_token'),
              accept: 'application/json',
              }},
              {withCredentials:true})


          // get list of likes for each post
          const inboxPromises = response_inbox.data.items.map(async (item) => {
            if (item.type === 'post') {
              const response = await requests.get(`authors/${item.author.id}/posts/${item.id}/likes/`);
              item.likes = response.data.items;
              item.likedByCurrent = false;
              // check if current viewer liked the post
              item.likes.forEach((like) => {
                if (like.author === this.state.currentUser.id) {
                  item.likedByCurrent = true;
                }
              })
            }
            return item;
          })
          // wait for promises then set inbox list
          const inboxList = await Promise.all(inboxPromises)
          this.setState({inboxList: inboxList})
      } catch(error) {
          console.log(error)
      }
  }

  clearInbox = async () => {
    try {
      await requests.delete(`authors/${this.state.currentUser.id}/inbox/`,
            {headers: {
              Authorization: localStorage.getItem('access_token'),
              accept: 'application/json',
              }},
              {withCredentials:true})
      this.setState({inboxList: []})
    } catch(error) {
        console.log(error)
    }
  }

  renderInboxItems() {
    return this.state.inboxList.map((item) => {
        if (item.type === 'post') {
          return (
            <Grid item xs={8}>
              <Post
              post= {item}
              currentUser={this.state.currentUser}
              likes={item.likes}
              likedByCurrent={item.likedByCurrent}
              isPublic={item.visibility === 'PUBLIC' && item.viewableBy === ''}
              />
            </Grid>
          );
        } else if (item.type === 'Follow') {
          return (
            <Grid item xs={8}>
            <FollowRequest
                displayName={item.actor.displayName}
                profileImage={item.actor.profileImage}
                currentUserId={this.state.currentUser.id}
                id={item.actor.id}
                accepted={item.accepted}
            />
            </Grid>
          );
        } else if (item.type === 'Like') {
          return (
            <Grid item xs={8}>
            <LikeNotification
              summary={item.summary}
              profileImage={item.author.profileImage}
              object={item.object}
            />
            </Grid>
          );
        } else if (item.type === 'comment') {
          return (
          <Grid item xs={8}>
            <CommentNotification
              profileImage={item.author.profileImage}
              displayName={item.author.displayName}
              owned={item.author.id === this.state.currentUser.id}
              id={item.id}
            />
            </Grid>);
        }
    });
  }

  render(){
      return (
          <div className="inbox">
            <Grid container p={2}
            justifyContent="center"
            alignItem="center"
            direction="column">
              <Button 
              variant="outlined"
              startIcon={<DeleteIcon />}
              onClick={this.clearInbox}>
                Clear inbox
              </Button>
            </Grid>
          <Grid container spacing={2} justifyContent="center" alignItem="center">
            {this.state.inboxList.length ? this.renderInboxItems() : <h2>Inbox is empty</h2>}
          </Grid>
          </div>
      )
  }
}

export default Inbox;

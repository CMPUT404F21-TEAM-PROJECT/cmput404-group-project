import React from "react";
import requests from "../../requests";
import { Alert, Button, List, Grid, Box, TextField, Stack, ListItemText } from "@mui/material";
import FollowRequest from "../Followers/FollowRequest";
import LikeNotification from "./LikeNotification";
import CommentNotification from "./CommentNotification";
import Post from "../Posts/Post";
import DeleteIcon from '@mui/icons-material/Delete';
import { BACKEND_URL } from "../../constants";
import { getAuthHeaderForNode } from "../../util";
  
class Inbox extends React.Component {
  constructor(props){
    super(props);
    this.state = {
        currentUser: {},
        inboxList: [],
        notificationList: []
    }
}

  componentDidMount() {
      this.initializeDetails();
  }

  initializeDetails = async () => {
      try {
          // Get the author details
          const response = await requests.get(BACKEND_URL + "/get-user/", {timeout:500});

          this.setState({ currentUser: {
            id: response.data.id ? response.data.id : '',
            url: response.data.url ? response.data.url : '',
            host: response.data.host ? response.data.host : '',
            displayName: response.data.displayName ? response.data.displayName : '',
            github: response.data.github ? response.data.github : '',
            profileImage: response.data.profileImage ? response.data.profileImage : ''
          }});

          const response_inbox = await requests.get(`${this.state.currentUser.id}/inbox/`, {withCredentials:true})


          // get list of likes for each post
          const inboxPromises = response_inbox.data.items.map(async (item) => {
            try {
              if (item.type === 'post') {
                const url = `${item.id}/likes/`;
                const response = await requests.get(url, getAuthHeaderForNode());
                item.likes = response.data.items;
                item.likedByCurrent = false;
                // check if current viewer liked the post
                item.likes.forEach((like) => {
                  if (like.author === this.state.currentUser.id) {
                    item.likedByCurrent = true;
                  }
                })
              }
            } catch(e) {
              console.log(e);
            }
            return item;
          })
          // wait for promises then set inbox list
          const inboxList = await Promise.all(inboxPromises)
          this.setState({inboxList: inboxList.filter(msg => msg.type === 'post')})
          this.setState({notificationList: inboxList.filter(msg => msg.type !== 'post')})
      } catch(error) {
          console.log(error)
      }
  }

  clearInbox = async () => {
    try {
      await requests.delete(`${this.state.currentUser.id}/inbox/`, {withCredentials:true})
      this.setState({inboxList: []})
      this.setState({notificationList: []})
    } catch(error) {
        console.log(error)
    }
  }

  renderPostItems() {
    return this.state.inboxList.sort((a,b) => (a.published < b.published ? 1 : -1)).map((item) => {
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
    });
  }

  renderNotificationItems() {
    return this.state.notificationList.map((item) => {
     if (item.type === 'Follow') {
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
      }; 
  });
};

  render(){
      return (
          <div className="inbox">
            <Grid container 
            pt={2}
            pb={4}
            pl={"16.75%"}
            pr={"16.75%"}
            justifyContent="center"
            alignitem="center"
            direction="column"
            >
              <Button item
              variant="outlined"
              startIcon={<DeleteIcon />}
              onClick={this.clearInbox}>
                Clear inbox
              </Button>
            </Grid>
          <Grid container spacing={2} paddingBottom="30px" justifyContent="center" alignItem="center">
            {this.state.inboxList.length || this.state.notificationList.length ? [this.renderPostItems(), this.renderNotificationItems()] : <h2>Inbox is empty</h2>}
          </Grid>
          </div>
      )
  }
}

export default Inbox;
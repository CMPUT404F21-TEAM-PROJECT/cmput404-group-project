import React from "react";
import requests from "../../requests";
import { Alert, Button, List, Grid, Box, TextField, Stack, ListItemText } from "@mui/material";
import FollowRequest from "../Followers/FollowRequest";
import LikeNotification from "./LikeNotification";
import CommentNotification from "./CommentNotification";
  
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
          const response = await requests.get('service/get-user/', {headers: {
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

          const response_inbox = await requests.get(`service/authors/${this.state.currentUser.id}/inbox/`,
            {headers: {
              Authorization: localStorage.getItem('access_token'),
              accept: 'application/json',
              }},
              {withCredentials:true})
          this.setState({inboxList: response_inbox.data.items})
          console.log(this.state.inboxList)

      } catch(error) {
          console.log(error)
      }
  }

  renderInboxItems() {
    return this.state.inboxList.map((item) => {
        console.log('item', item)
        if (item.type === 'post') {
          return (<p>a post</p>);
        } else if (item.type === 'Follow') {
          return (
            <Grid item xs={6}>
            <FollowRequest
                displayName={item.actor.displayName}
                profileImage={item.actor.profileImage}
                currentUserId={this.state.currentUser.id}
                id={item.actor.id}
                accepted={item.accepted}
            />
            </Grid>
          );
        } else if (item.type === 'like') {
          return (
            <Grid item xs={6}>
            <LikeNotification
              summary={item.summary}
              profileImage={item.author.profileImage}
              object={item.object}
            />
            </Grid>
          );
        } else if (item.type === 'comment') {
          return (
          <Grid item xs={6}>
            <CommentNotification
              profileImage={item.author.profileImage}
              displayName={item.author.displayName}
              id={item.id}
            />
            </Grid>);
        }
    });
  }

  render(){
      return (
          <div className="inbox">
          <Grid container spacing={2} justifyContent="center" alignItem="center">
            {this.renderInboxItems()}
          </Grid>
          </div>
      )
  }
}

export default Inbox;

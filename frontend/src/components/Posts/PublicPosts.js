import React from "react";
import requests from "../../requests";
import { Grid } from "@mui/material";
import Post from "../Inbox/Post";

  
class PublicPosts extends React.Component {
  constructor(props){
    super(props);
    this.state = {
        currentUser: {},
        allPosts: {},
    }
}

  componentDidMount() {
      this.initializeDetails();
  }

  getAllPosts = async () => {
    try {
        // Get all the author details
        const response = await requests.get(`authors/${this.state.currentUser.id}/posts/`, {headers: {
            Authorization: localStorage.getItem('access_token'),
            accept: 'application/json',
        }});
        
        // get list of likes for each post
        const postPromises = response.data.items.map(async (item) => {
          if (item.type === 'post') {
            const like_response = await requests.get(`authors/${item.author.id}/posts/${item.id}/likes/`);
            item.likes = like_response.data.items;
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
        const postList = await Promise.all(postPromises)
        this.setState({ allPosts: postList });
    } catch(error) {
        console.log(error)
    }
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

        this.getAllPosts();

      } catch(error) {
          console.log(error)
      }
  }

  renderInboxItems() {
    return this.state.allPosts.map((item) => {
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
        }
    });
  }

  render(){
      return (
          <div className="PublicPosts">
            <Grid container p={2}
            justifyContent="center"
            alignItem="center"
            direction="column">
            </Grid>
          <Grid container spacing={2} justifyContent="center" alignItem="center">
            {this.state.allPosts.length ? this.renderInboxItems() : <h2>Inbox is empty</h2>}
          </Grid>
          </div>
      )
  }
}

export default PublicPosts;

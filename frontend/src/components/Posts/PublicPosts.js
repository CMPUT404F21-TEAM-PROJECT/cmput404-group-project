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
        const response = await requests.get(`service/authors/${this.state.currentUser.id}/posts/`, {headers: {
            Authorization: localStorage.getItem('access_token'),
            accept: 'application/json',
        }});
        this.setState({ allPosts: response.data.items });
        console.log(this.state.allPosts)
    } catch(error) {
        console.log(error)
    }
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

        this.getAllPosts();

      } catch(error) {
          console.log(error)
      }
  }

  renderInboxItems() {
    return this.state.allPosts.map((item) => {
        console.log('item', item)
        if (item.type === 'post') {
          return (
            <Grid item xs={8}>
              <Post author= {item.author}
              title={item.title}
              contentType={item.contentType}
              content= {item.content}
              description= {item.description}
              post= {{id: item.id}}
              currentUser={this.state.currentUser}
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

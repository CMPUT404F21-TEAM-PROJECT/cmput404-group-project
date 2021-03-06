import React, { Component } from "react";
// import './App.css';
import {
  Button,
  TextField,
  MenuItem,
  FormControl,
  FormGroup,
  Grid,
  Typography
} from "@mui/material";
import requests from "../../requests";
import { Redirect } from "react-router-dom";
import FileBase64 from "react-file-base64";
import { BACKEND_URL } from "../../constants";
import { getAuthHeaderForNode } from "../../util";
// TODO: Add form validation
//import { ValidatorForm, TextValidator } from "react-material-ui-form-validator";

// TODOS:
// Form validation
// print error messages

class NewPost extends Component {
  constructor(props) {
    super(props);
    this.getAuthorId();
  }

  state = {
    title: "",
    description: "",
    content_type: "text/plain",
    content: "",
    categories: "",
    visibility: "PUBLIC",
    unlisted: false,
    successful_post: false,
    author_id: "",
    viewableBy: "",
    jwt: localStorage.getItem("access_token"),
  };

  getAuthorId = async () => {
    const response = await requests.get(BACKEND_URL + "/get-user/", {timeout:500});
    this.setState({
      author_id: response.data.id ? response.data.id : "",
    });
  };

  handleSubmit = async () => {
    try {
      const url = this.state.author_id + "/posts/";
      const response = await requests.post(url, {
        title: this.state.title,
        author: this.state.author_id,
        contentType: this.state.content_type,
        content: this.state.content,
        description: this.state.description,
        visibility: this.state.visibility,
        unlisted: this.state.unlisted,
        categories: this.state.categories,
        viewableBy: this.state.viewableBy,
      },
      getAuthHeaderForNode(url));
      this.setState({ successful_post: true });
      response.data.type = 'post'
      if (!response.data.unlisted) {
        this.sendToSelf(response.data)
        this.sendToFollowers(response.data);
      }
    } catch (error) {
      console.log(error);
    }
  };

  sendToSelf = async (my_post) => {
    const url = `${this.state.author_id}/inbox/`;
    await requests.post(
      url,
      my_post,
      getAuthHeaderForNode(url),
      {withCredentials:true});
  };

  sendToFollowers = async (my_post) => {
    // Get Followers
    const response = await requests.get(
      `${my_post.author.id}/followers/`
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

  render() {
    return (
      <Grid container pb={"30px"} justifyContent="center">
        <FormControl
          component="fieldset"
          variant="filled"
          disabled
          style={{ width: "35em" }}
        >
          <Typography fontWeight="bold" fontSize="2em" textAlign="center" paddingTop="20px" paddingBottom="35px">New Post</Typography>
          <FormGroup>
            <span>Post Details</span>
            <br></br>
            <TextField
              className="text-input"
              size="small"
              type="text"
              fullWidth={true}
              label="Title"
              value={this.state.title}
              onChange={({ target }) =>
                this.setState({
                  title: target.value,
                })
              }
            />
            <br />
            <TextField
              className="text-input"
              size="small"
              type="text"
              fullWidth={true}
              label="Description"
              value={this.state.description}
              onChange={({ target }) =>
                this.setState({
                  description: target.value,
                })
              }
            />
            <br />
            <TextField
              select
              value={this.state.content_type}
              label="Content Type"
              fullWidth={true}
              onChange={({ target }) =>
                this.setState({
                  content_type: target.value,
                })
              }
            >
              <MenuItem value="text/plain">text/plain</MenuItem>
              <MenuItem value="text/markdown">text/markdown</MenuItem>
              <MenuItem value="application/base64">application/base64</MenuItem>
              <MenuItem value="image/png;base64">image/png</MenuItem>
              <MenuItem value="image/jpeg;base64">image/jpeg</MenuItem>
            </TextField>
            <br />
            {this.state.content_type === "image/jpeg;base64" ||
            this.state.content_type === "image/png;base64" ? (
              <FileBase64
                className="image-input"
                type="file"
                accept=".png,.jpeg,.jpg"
                label="Content"
                value={this.state.content}
                onDone={({ base64 }) => {
                  this.setState({
                    // base64 includes data:image/png;base64, before content. So split.
                    content: base64,
                  });
                }}
              />
            ) : (
              <TextField
                className="text-input"
                size="medium"
                multiline={true}
                type="text"
                fullWidth={true}
                label="Content"
                value={this.state.content}
                onChange={({ target }) =>
                  this.setState({
                    content: target.value,
                  })
                }
              />
            )}
            <br />
            <TextField
              className="text-input"
              type="text"
              label="Categories"
              fullWidth={true}
              value={this.state.categories}
              onChange={({ target }) =>
                this.setState({
                  categories: target.value,
                })
              }
            />
            <br />
            <p>Visibility</p>
            <TextField
              select
              fullWidth={true}
              value={this.state.visibility}
              label="Visibility"
              defaultValue="PUBLIC"
              onChange={({ target }) =>
                this.setState({
                  visibility: target.value,
                })
              }
            >
              <MenuItem value="PUBLIC">Public</MenuItem>
              <MenuItem value="FRIENDS">Friends</MenuItem>
            </TextField>
            <br />
            <TextField
              className="text-input"
              defaultValue=""
              size="small"
              type="text"
              fullWidth={true}
              label="Post only to"
              value={this.state.viewableBy}
              onChange={({ target }) =>
                this.setState({
                  viewableBy: target.value,
                })
              }
            />
            <br />
            <p>Unlisted</p>
            <input 
              type='checkbox'
              value={this.state.unlisted}
              label="Unlisted"
              onChange={() =>
                this.setState({
                  unlisted: !this.state.unlisted,
                })
              }
            />
            <br />
            <Button
              variant="contained"
              onClick={this.handleSubmit}
              ref={(node) => (this.btn = node)}
            >
              Post
            </Button>
            {this.state.successful_post && <Redirect to="/inbox" />}
          </FormGroup>
        </FormControl>
      </Grid>
    );
  }
}

export default NewPost;

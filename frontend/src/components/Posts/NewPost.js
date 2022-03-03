import React, { Component } from "react";
// import './App.css';
import { Button, TextField, Select, MenuItem } from "@mui/material";
import "../../styles/new-post.css";
import requests from "../../requests";
import { Redirect } from "react-router-dom";
// TODO: Add form validation
//import { ValidatorForm, TextValidator } from "react-material-ui-form-validator";

class NewPost extends Component {
  constructor(props) {
    super(props);
    this.getAuthorId();
  }

  state = {
    title: "",
    description: "",
    content: "",
    categories: "",
    visibility: "",
    successful_post: false,
    author_id: "",
    jwt: localStorage.getItem("access_token"),
  };

  getAuthorId = async () => {
    const response = await requests.get("service/get-user/", {
      headers: {
        Authorization: this.state.jwt,
        accept: "application/json",
      },
    });
    this.setState({
      author_id: response.data.id ? response.data.id : "",
    });
  };

  handleSubmit = async () => {
    console.log(this.state);
    requests.defaults.headers['Authorization'] = this.state.jwt;
    try {
      const url = "service/authors/" + this.state.author_id + "/posts/";
      const response = await requests.post(url, {
        headers: {
          accept: "application/json",
        },
        title: this.state.title,
        author: this.state.author_id,
        contentType: "text/plain",
        content: this.state.content,
        description: this.state.description,
        visibility: this.state.visibility,
        categories: this.state.categories,
      });
      console.log(response.data);
      this.setState({ successful_post: true });
    } catch (error) {
      console.log(error);
    }
  };

  render() {
    return (
      <div className="background">
        <div className="form">
          <h1>New Post</h1>
          <div className="wrapper">
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
            <Select
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
            </Select>
            <br />
            <Button
              variant="contained"
              onClick={this.handleSubmit}
              ref={(node) => (this.btn = node)}
            >
              Post
            </Button>
            {this.state.successful_post && <Redirect to="/inbox" />}
          </div>
        </div>
      </div>
    );
  }
}

export default NewPost;

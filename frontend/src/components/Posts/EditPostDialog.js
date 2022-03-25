import * as React from "react";
import {
  Button,
  TextField,
  MenuItem,
  FormControl,
  FormGroup,
  Grid,
} from "@mui/material";
import requests from "../../requests";
import { Redirect } from "react-router-dom";
import FileBase64 from "react-file-base64";
import PropTypes from "prop-types";
import DialogTitle from "@mui/material/DialogTitle";
import Dialog from "@mui/material/Dialog";
import EditIcon from "@mui/icons-material/Edit";
import "./CommentDialog.css";
import { EditComment, AddCommentListItem } from "./AddComment";
import { usePreviousProps } from "@mui/utils";
import { getAuthHeaderForNode } from "../../util";

export default function EditPost(props) {
  const [open, setOpen] = React.useState(false);

  const handleClickOpen = async () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Button
        variant="contained"
        startIcon={<EditIcon />}
        onClick={handleClickOpen}
      >
        Edit
      </Button>
      <EditPostDialog
        current_author={props.current_author}
        open={open}
        onClose={handleClose}
        post={props.post}
      />
    </div>
  );
}

function EditPostDialog(props) {
  const { onClose, selectedValue, open } = props;

  const [title, setTitle] = React.useState(props.post.title);
  const [description, setDescription] = React.useState(props.post.description);
  const [content_type, setContentType] = React.useState(
    props.post.contentType
  );
  const [content, setContent] = React.useState(props.post.content);
  const [categories, setCategories] = React.useState(props.post.categories);
  const [visibility, setVisibility] = React.useState(props.post.visibility);
  const [unlisted, setUnlisted] = React.useState(props.post.unlisted);
  const [viewable_by, setViewableBy] = React.useState(props.post.viewableBy);
  const [successful_post, setSuccessfulPost] = React.useState(false);
  const jwt = localStorage.getItem("access_token");

  const handleClose = () => {
    onClose(selectedValue);
  };

  const handleSubmit = async () => {
    try {
      const url = props.post.id + "/";
      const response = await requests.post(url, {
        id: props.post.id,
        title: title,
        author: props.current_author,
        contentType: content_type,
        content: content,
        description: description,
        visibility: visibility,
        unlisted: unlisted,
        categories: categories,
        viewableBy: viewable_by,
      }, getAuthHeaderForNode(url));
      setSuccessfulPost(true);
      response.data.type = "post";
      if (!response.data.unlisted) {
        sendToSelf(response.data);
        sendToFollowers(response.data);
      }
      window.location.reload();
    } catch (error) {
      console.log(error);
    }
  };

  const sendToSelf = async (my_post) => {
    const url = `${props.current_author}/inbox/`;
    await requests.post(
      url,
      my_post,
      getAuthHeaderForNode(url),
      { withCredentials: true }
    );
  };

  const sendToFollowers = async (my_post) => {
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
        { withCredentials: true }
      );
    }
  };

  return (
    <Dialog onClose={handleClose} maxWidth="800px" open={open}>
      <DialogTitle className="edit-post-dialog">Edit Post</DialogTitle>
      <Grid container justifyContent="center">
        <FormControl
          component="fieldset"
          variant="filled"
          disabled
          style={{ width: "35em" }}
        >
          <FormGroup>
            <TextField
              className="text-input"
              size="small"
              type="text"
              fullWidth={true}
              label="Title"
              value={title}
              onChange={({ target }) => setTitle(target.value)}
            />
            <br />
            <TextField
              className="text-input"
              size="small"
              type="text"
              fullWidth={true}
              label="Description"
              value={description}
              onChange={({ target }) => setDescription(target.value)}
            />
            <br />
            <TextField
              select
              label="Content Type"
              fullWidth={true}
              value={content_type}
              onChange={({ target }) => setContentType(target.value)}
            >
              <MenuItem value="text/plain">text/plain</MenuItem>
              <MenuItem value="text/markdown">text/markdown</MenuItem>
              <MenuItem value="application/base64">application/base64</MenuItem>
              <MenuItem value="image/png;base64">image/png</MenuItem>
              <MenuItem value="image/jpeg;base64">image/jpeg</MenuItem>
            </TextField>
            <br />
            {content_type === "image/jpeg;base64" ||
            content_type === "image/png;base64" ? (
              <FileBase64
                className="image-input"
                type="file"
                accept=".png,.jpeg,.jpg"
                label="Content"
                value={content}
                onDone={({ base64 }) => {
                  setContent(base64);
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
                value={content}
                onChange={({ target }) =>
                  setContent(target.value)
                }
              />
            )}
            <br />
            <TextField
              className="text-input"
              type="text"
              label="Categories"
              fullWidth={true}
              value={categories}
              onChange={({ target }) =>
                setCategories(target.value)
              }
            />
            <br />
            <p>Visibility</p>
            <TextField
              select
              fullWidth={true}
              label="Visibility"
              defaultValue="PUBLIC"
              value={visibility}
              onChange={({ target }) =>
              setVisibility(target.value)
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
              value={viewable_by}
              onChange={({ target }) =>
                setViewableBy(target.value)
              }
            />
            <br />
            <p>Unlisted</p>
            <input
              type="checkbox"
              label="Unlisted"
              value={unlisted}
              onChange={() =>
                setUnlisted(!unlisted)
              }
            />
            <br />
            <Button
              variant="contained"
              onClick={handleSubmit}
            >
              Post
            </Button>
            {successful_post && handleClose()}
          </FormGroup>
        </FormControl>
      </Grid>
    </Dialog>
  );
}

EditPostDialog.propTypes = {
  onClose: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
};

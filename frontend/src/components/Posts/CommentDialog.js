import * as React from 'react';
import PropTypes from 'prop-types';
import Button from '@mui/material/Button';
import Avatar from '@mui/material/Avatar';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import DialogTitle from '@mui/material/DialogTitle';
import Dialog from '@mui/material/Dialog';
import PersonIcon from '@mui/icons-material/Person';
import { blue } from '@mui/material/colors';
import DeleteIcon from '@mui/icons-material/Delete'
import './CommentDialog.css';
import {EditComment, AddCommentListItem} from './AddComment';
import requests from '../../requests';
import { usePreviousProps } from '@mui/utils';

export default function CommentDialogButton(props) {
  const [open, setOpen] = React.useState(false);
  const [comments, setComments] = React.useState(0);
  const [commenters, setCommenters] = React.useState(0);
  const [ids, setCommentIds] = React.useState(0); 

  const getComments = async () => {
    try {
      const response = await requests.get(`authors/${props.author_id}/posts/${props.post_id}/comments/`,
      {headers: {
      Authorization: localStorage.getItem('access_token'),
      accept: 'application/json',
      }},
      {withCredentials:true});
      console.log(response.data.items);
      var ids = [];
      var commenter_ids = [];
      var comment_ids = [];
      response.data.items.forEach((comment) =>  {
        ids.push(comment.comment);
        commenter_ids.push(comment.author);
        comment_ids.push(comment.id);
      });
      setComments(ids);
      setCommenters(commenter_ids);
      setCommentIds(comment_ids);
    }
    catch(error) {
      console.log(error);
    }
  };

  React.useEffect(() => {
    getComments();
  }, []);


const handleClickOpen = async () => {
    setOpen(true);
};

  const handleClose = (value) => {
    setOpen(false);
  };

  return (
    <div>
      <Button variant="outlined" onClick={handleClickOpen}>
        View Comments
      </Button>
      <CommentDialog
        current_author = {props.current_author}
        author_id = {props.author_id}
        open={open}
        onClose={handleClose}
        post_id = {props.post_id}
        comments = {comments}
        commenters = {commenters}
        comment_id = {ids}
      />
    </div>
  );
}

function CommentDialog(props) {

  var authors = props.commenters ? props.commenters : [];
  var comments = props.comments ? props.comments : [];
  const { onClose, selectedValue, open } = props;
  const [commentText, setCommentText] = React.useState("")

  const handleClose = () => {
    onClose(selectedValue);
  };

  // Handles the deletion of a comment within the dialog listview after confirmation
  const handleDelete = async (index) => {
    // TODO switch to an actual confirm dialogue
    if (window.confirm("Do you really want to delete this comment?")) {
    try {
      var comment_id = props.comment_id[index]
      const response = await requests.delete(`authors/${props.author_id}/posts/${props.post_id}/comments/${comment_id}/`,
      {headers: {
      Authorization: localStorage.getItem('access_token'),
      accept: 'application/json',
      }},
      {withCredentials:true});
    }
    catch(error) {
      console.log(error);
    }
  }
}

  return (
    <Dialog onClose={handleClose} maxWidth="800px" open={open}>
      <DialogTitle className="comment-dialog">Comments</DialogTitle>
      <List sx={{ pt: 0 }}>
        {authors.map((author, index) => (
          <ListItem button key={author}>
            <ListItemAvatar>
              <Avatar sx={{ bgcolor: blue[100], color: blue[600] }}>
                <PersonIcon />
              </Avatar>
            </ListItemAvatar>
            <ListItemText primary={`${author}: ${comments[index]}`} />
            {author === props.current_author ? 
            <EditComment
              current_author = {props.current_author}
              post_author = {props.author_id}
              post_id = {props.post_id}
              comment_id = {props.comment_id[index]}/> : ''}
            {author === props.current_author ? <Button className = "comment-button" color = "error" variant="contained" startIcon={<DeleteIcon />} onClick={() => handleDelete(index)}>
              Delete
            </Button> : ''}
          </ListItem>
        ))}
        <AddCommentListItem
        current_author = {props.current_author}
        post_author = {props.author_id}
        post_id = {props.post_id}/>
      </List>
    </Dialog>
  );
}

CommentDialog.propTypes = {
  onClose: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired
};
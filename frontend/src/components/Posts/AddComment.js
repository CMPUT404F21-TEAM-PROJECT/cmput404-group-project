import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import './CommentDialog.css';
import requests from '../../requests';
import EditIcon from '@mui/icons-material/Edit';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import Avatar from '@mui/material/Avatar';
import AddIcon from '@mui/icons-material/Add';

export function EditComment(props) {
  const [open, setOpen] = React.useState(false);
  const [comment, setComment] = React.useState('');

  const handleClickOpen = () => {
    setOpen(true);
    setComment('');
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleEdit = async () => {
        // send PUT request to authors/{authorId}/posts/{postId}/comments/{commentId} with new comment
        try {
        const response = await requests.put(`authors/${props.post_author}/posts/${props.post_id}/comments/${props.comment_id}/`,
            {
            comment: comment
            },
            {headers: {
                Authorization: localStorage.getItem('access_token'),
                accept: 'application/json',
            }
            },
            {withCredentials: true});
    } catch(e) {
        console.log(e)
    }
    handleClose();
  }

  return (
    <div>
      <Button variant="contained" onClick={handleClickOpen} endIcon={<EditIcon />}>
        Edit
      </Button>
      <Dialog open={open} minWidth="800px" maxWidth="800px" hideBackdrop={true} onClose={handleClose}>
        <DialogTitle className="comment-dialog">Edit Comment</DialogTitle>
        <DialogContent>
          <TextField
            defaultValue="Normal"
            autoFocus
            margin="dense"
            id="name"
            label="Comment"
            type="email"
            fullWidth
            variant="standard"
            value={comment}
            onChange={(event) => {setComment(event.target.value)}}
          />
        </DialogContent>
        <DialogActions>
          <Button variant="contained" onClick={handleClose}>Cancel</Button>
          <Button variant="contained" onClick={handleEdit}>Update</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export function AddCommentListItem(props) {
    const [open, setOpen] = React.useState(false);
    const [comment, setComment] = React.useState('');
  
    const handleClickOpen = () => {
      setOpen(true);
      setComment('');
    };
  
    const handleClose = () => {
      setOpen(false);
    };
  
    const handleSend = async () => {
        // send POST request to authors/{authorId}/posts/{postId}/comments/ with a comment
        try {
            const response = await requests.post(`authors/${props.post_author}/posts/${props.post_id}/comments/`,
              {
              post_id: props.post_id,
              comment: comment,
              contentType: "text/markdown",
              author: props.current_author,
              type: "comment"
              },
              {headers: {
                  Authorization: localStorage.getItem('access_token'),
                  accept: 'application/json',
                }
              },
              {withCredentials: true});
            sendToSelf(response.data);
            // send to recipients inbox
            const response_recipient = await requests.post(`authors/${props.post_author}/inbox/`,
            response.data,
            {headers: {
              Authorization: localStorage.getItem('access_token'),
              accept: 'application/json',
            }
            },
          {withCredentials: true})
        } catch(e) {
          console.log(e)
        }
        handleClose();
    }
  
    const sendToSelf = async (my_item) => {
      const response_self = await requests.post(
        `authors/${props.current_author}/inbox/`,
        my_item,
        {headers: {
          Authorization: localStorage.getItem('access_token'),
          accept: 'application/json',
        }},
        {withCredentials:true});
    };
  
    return (
      <div>
        <ListItem autoFocus button onClick={() => handleClickOpen()}>
          <ListItemAvatar>
            <Avatar>
              <AddIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText primary="Add Comment" />
        </ListItem>
        <Dialog open={open} minWidth="800px" maxWidth="800px" hideBackdrop={true} onClose={handleClose}>
        <DialogTitle className="comment-dialog">Add new comment</DialogTitle>
        <DialogContent>
          <TextField
            defaultValue="Normal"
            placeholder="Write a comment..."
            autoFocus
            margin="dense"
            id="name"
            label="Comment"
            type="email"
            fullWidth
            variant="standard"
            value={comment}
            onChange={(event) => {setComment(event.target.value)}}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleSend}>Send</Button>
        </DialogActions>
      </Dialog>
      </div>
    );
  }
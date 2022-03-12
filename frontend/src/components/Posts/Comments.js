// import * as React from 'react';
// import PropTypes from 'prop-types';
// import Button from '@mui/material/Button';
// import Avatar from '@mui/material/Avatar';
// import List from '@mui/material/List';
// import ListItem from '@mui/material/ListItem';
// import ListItemAvatar from '@mui/material/ListItemAvatar';
// import ListItemText from '@mui/material/ListItemText';
// import DialogTitle from '@mui/material/DialogTitle';
// import Dialog from '@mui/material/Dialog';
// import PersonIcon from '@mui/icons-material/Person';
// import AddIcon from '@mui/icons-material/Add';
// import Typography from '@mui/material/Typography';
// import { blue } from '@mui/material/colors';
// import DeleteIcon from '@mui/icons-material/Delete'
// import EditIcon from '@mui/icons-material/Edit';
// import './SimpleDialog.css';
// import requests from '../../requests';

// const authors = ['username@gmail.com', 'user02@gmail.com'];

// class Comments extends Component {
//     constructor(props){
//         super(props);
//         this.state = {
//             currentUser: {},
//             followerList: [],
//             followingList: [],
//             addFollowerId: '',
//             addFollowerError: '',
//         }
//     }
//   const { onClose, selectedValue, open } = props;
//   const [commentText, setCommentText] = React.useState("")

//   const handleClose = () => {
//     onClose(selectedValue);
//   };

//   const handleListItemClick = (value) => {
//     // onClose(value);
//   };

//   const handleEdit = (value) => {
//     alert("Edit Clicked");
//   }

//   const handleDelete = (value) => {
//     alert("Delete Clicked");
//   }

//   return (
//     <Dialog onClose={handleClose} maxWidth="800px" open={open}>
//       <DialogTitle className="comment-dialog">Comments</DialogTitle>
//       <List sx={{ pt: 0 }}>
//         {authors.map((author) => (
//           <ListItem button key={author}>
//             <ListItemAvatar>
//               <Avatar sx={{ bgcolor: blue[100], color: blue[600] }}>
//                 <PersonIcon />
//               </Avatar>
//             </ListItemAvatar>
//             <ListItemText primary={`${author}: SWAG`} />
//             <Button className = "edit-button" variant="contained" endIcon={<EditIcon />} onClick={handleEdit}>
//               Edit
//             </Button>  
//             <Button className = "comment-button" color = "error" variant="contained" startIcon={<DeleteIcon />} onClick={handleDelete}>
//               Delete
//             </Button>
//           </ListItem>
//         ))}

//         <ListItem autoFocus button onClick={() => handleListItemClick('addAccount')}>
//           <ListItemAvatar>
//             <Avatar>
//               <AddIcon />
//             </Avatar>
//           </ListItemAvatar>
//           <ListItemText primary="Add Comment" />
//         </ListItem>
//       </List>
//     </Dialog>
//   );
// }

// SimpleDialog.propTypes = {
//   onClose: PropTypes.func.isRequired,
//   open: PropTypes.bool.isRequired,
//   selectedValue: PropTypes.string.isRequired,
// };

// export default function SimpleDialogDemo(props) {
//   const [open, setOpen] = React.useState(false);
//   const [selectedValue, setSelectedValue] = React.useState(authors[1]);
//   const comments = {}


// const handleClickOpen = () => {
//   try {
//     const response = requests.get(`service/authors/${props.author_id}/posts/${props.post_id}/comments/`,
//     {headers: {
//     Authorization: localStorage.getItem('access_token'),
//     accept: 'application/json',
//     }},
//     {withCredentials:true}).then(data => console.log(data.data.items));
//     // console.log(response);
//     setOpen(true);
//   }
//   catch(error) {
//     console.log(error);
//   }
// };

//   const handleClose = (value) => {
//     setOpen(false);
//     setSelectedValue(value);
//   };

//   return (
//     <div>
//       <Typography variant="subtitle1" component="div">
//         Selected: {selectedValue}
//       </Typography>
//       <br />
//       <Button variant="outlined" onClick={handleClickOpen}>
//         View Comments
//       </Button>
//       <SimpleDialog
//         selectedValue={selectedValue}
//         open={open}
//         onClose={handleClose}
//         post_id = {props.post_id}
//       />
//     </div>
//   );
// }
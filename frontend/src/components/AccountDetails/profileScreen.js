import React from 'react'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import Alert from '@mui/material/Alert'
import Typography from '@mui/material/Typography'
import requests from "../../requests";
import Table from "@mui/material/Table"
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import './profileScreen.css'

class ProfileScreen extends React.Component {
    constructor(props){
        super(props);
        this.getAuthorDetails();
    }
    state = {author: {}, showSuccess: false};

    getAuthorDetails = async () => {
        // Get the author details
        const response = await requests.get('get-user/', {headers: {
            Authorization: localStorage.getItem('access_token'),
            accept: 'application/json',
          }});
        this.setState({author: {
            id: response.data.id ? response.data.id : '',
            url: response.data.url ? response.data.url : '',
            host: response.data.host ? response.data.host : '',
            displayName: response.data.displayName ? response.data.displayName : '',
            github: response.data.github ? response.data.github : '',
            profileImage: response.data.profileImage ? response.data.profileImage : ''
        }});
    }

    saveChangesPressed = async () => {
        var updatesDict = {"id": this.state.author.id}
        if (document.getElementById('url-input').value){
            updatesDict["url"] = document.getElementById('url-input').value;
        }
        if (document.getElementById('host-input').value){
            updatesDict["host"] = document.getElementById('host-input').value;
        }
        if (document.getElementById('displayName-input').value){
            updatesDict["displayName"] = document.getElementById('displayName-input').value;
        }
        if (document.getElementById('github-input').value){
            updatesDict["github"] = document.getElementById('github-input').value;
        }
        if (document.getElementById('profileImage-input').value){
            updatesDict["profileImage"] = document.getElementById('profileImage-input').value;
        }
        const response = await requests.post('authors/' + this.state.author.id + '/', updatesDict, {WithCredentials: true})

        // Keep values that were not updated
        const allKeys = Object.keys(this.state.author);
        const updatedKeys = Object.keys(updatesDict);
        for (let i = 0; i < allKeys.length; i++){
            if (!updatedKeys.includes(allKeys[i])){
                updatesDict[allKeys[i]] = this.state.author[allKeys[i]];
            }
        }
            
        // Update state
        this.setState({author: updatesDict, showSuccess: true});
        setTimeout(() => {
            this.setState({showSuccess: false});
        }, 2000);
    }

    createData(field, value) {
        return { field, value };
      }

    render(){
        var rows = [
            this.createData('Url:', this.state.author.url),
            this.createData('Host:', this.state.author.host),
            this.createData('Display Name:', this.state.author.displayName),
            this.createData('GitHub:', this.state.author.github),
            this.createData('Profile Image:', this.state.author.profileImage),
        ]
        return (
            <div className='ProfileScreen'>
                <h1>My Profile</h1>
                <span id='my-profile'>
                    <img alt="Profile Image" src={this.state.author.profileImage}></img>
                    <div id='labels'>
                    <Table sx={{ minWidth: 200 }} aria-label="simple table">
                        <TableBody>
                        {rows.map((row) => (
                            <TableRow
                            key={row.field}
                            sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                            >
                            <TableCell component="th" scope="row">
                                {row.field}
                            </TableCell>
                            <TableCell align="left">{row.value}</TableCell>
                            </TableRow>
                        ))}
                        </TableBody>
                    </Table>
                    </div>
                </span>
                <h1>Edit Profile</h1>
                <div id='inputs'>
                    <TextField id="url-input" label="New Url" variant="filled" defaultValue=""/>
                    <TextField id="host-input" label="New Host" variant="filled" defaultValue=""/>
                    <TextField id="displayName-input" label="New Display Name" variant="filled" defaultValue=""/>
                    <TextField id="github-input" label="New GitHub" variant="filled" defaultValue=""/>
                    <TextField id="profileImage-input" label="New ProfileImage" variant="filled" defaultValue=""/>
                </div>
                <Button onClick={this.saveChangesPressed} variant="contained">Save Changes</Button>
                {this.state.showSuccess && <Alert severity="success">
                    Changes saved successfully
                </Alert>}
            </div>
        )
    }
}

export default ProfileScreen
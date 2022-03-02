import React, { useEffect } from 'react'
import ReactDom from 'react-dom'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import requests from "../../requests";

class ProfileScreen extends React.Component {
    constructor(props){
        super(props);
        this.getAuthorDetails();
    }
    state = {author: {}}

    getAuthorDetails = async () => {
        // Get the author details
        const response = await requests.get('service/get-user/', {headers: {
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
        console.log(this.state.author)
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
        await requests.post('service/authors/' + this.state.author.id + '/', updatesDict, {WithCredentials: true});
        this.setState({author: {}});
    }

    render(){
        return (
            <div className='ProfileScreen'>
                <img alt="Profile Image" src=""></img>
                <div>
                    <span>
                        <label id="current-url-label">Current Url: </label>
                        <label id="current-url">{this.state.author.url}</label>
                    </span>
                    <span>
                        <label id="current-host-label">Current Host: </label>
                        <label id="current-host">{this.state.author.host}</label>
                    </span>
                    <span>
                        <label id="current-displayName-label">Current Display Name: </label>
                        <label id="current-displayName">{this.state.author.displayName}</label>
                    </span>
                    <span>
                        <label id="current-github-label">Current GitHub: </label>
                        <label id="current-github">{this.state.author.github}</label>
                    </span>
                    <span>
                        <label id="current-profileImage-label">Current Profile Image: </label>
                        <label id="current-profileImage">{this.state.author.profileImage}</label>
                    </span>
                </div>
                <div>
                    <TextField id="url-input" label="New Url" variant="filled" defaultValue=""/>
                    <TextField id="host-input" label="New Host" variant="filled" defaultValue=""/>
                    <TextField id="displayName-input" label="New Display Name" variant="filled" defaultValue=""/>
                    <TextField id="github-input" label="New GitHub" variant="filled" defaultValue=""/>
                    <TextField id="profileImage-input" label="New ProfileImage" variant="filled" defaultValue=""/>
                </div>
                <Button onClick={this.saveChangesPressed} variant="contained">Save Changes</Button>
            </div>
        )
    }
}

export default ProfileScreen
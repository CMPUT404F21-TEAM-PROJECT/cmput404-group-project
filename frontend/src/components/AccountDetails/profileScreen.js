import React from 'react'
import AuthorDetailsEditable from "./authorDetailsEditable"
import Button from '@mui/material/Button'
import requests from "../../requests";

class ProfileScreen extends React.Component {
    state = {author : "empty", token : this.props.token};

    getAuthorDetails = async () => {
        // Get the author details
        const response = await requests.get('service/get-user/', {withCredentials: true});

        // Update author details
        this.state.author = {
            url: response.data.url,
            host: response.data.host,
            displayName: response.data.displayName,
            github: response.data.github,
            profileImage: response.data.profileImage};
    }
    
    diagnostics = () => {
        console.log(this.state.author);
    }
    

    saveChangesPressed = async () => {
        this.getAuthorDetails();
        this.diagnostics();
        const response = await requests.post(`service/authors/408af503-e10f-4dcf-bbd3-f81f571fa85a/`, {
            id: "408af503-e10f-4dcf-bbd3-f81f571fa85a",
            url: this.state.author.url,
            host: this.state.author.host,
            displayName: this.state.author.displayName,
            github: this.state.author.github,
            profileImage: this.state.author.profileImage
            }, {withCredentials: true});
    }

    render(){
        return (
            <div className='ProfileScreen'>
                <img alt="Profile Image" src=""></img>
                <AuthorDetailsEditable input="408af503-e10f-4dcf-bbd3-f81f571fa85a"></AuthorDetailsEditable>
                <Button onClick={this.saveChangesPressed} variant="contained">Save Changes</Button>
            </div>
        )
    }
}

export default ProfileScreen
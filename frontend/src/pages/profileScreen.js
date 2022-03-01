import React from 'react'
import AuthorDetailsEditable from "../components/authorDetailsEditable"
import Button from '@mui/material/Button'

class ProfileScreen extends React.Component {
    render(){
        return (
            <>
                <img alt="Profile Image" src=""></img>
                <AuthorDetailsEditable></AuthorDetailsEditable>
                <Button variant="contained">Save Changes</Button>
            </>
        )
    }
}

export default ProfileScreen
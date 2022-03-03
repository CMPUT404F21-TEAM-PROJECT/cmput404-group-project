import React from "react";
import requests from "../../requests";
import { Alert, Button, List, Grid, Box, TextField } from "@mui/material";
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import Follower from "./Follower";
import Following from "./Following";


class FriendsPage extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            currentUser: {},
            followerList: [],
            followingList: [],
            addFollowerId: '',
            addFollowerError: '',
        }
    }

    componentDidMount() {
        this.initializeDetails();
    }

    initializeDetails = async () => {
        try {
            // Get the author details
            const response = await requests.get('service/get-user/', {headers: {
                Authorization: localStorage.getItem('access_token'),
                accept: 'application/json',
            }});
            this.setState({ currentUser: {
                id: response.data.id ? response.data.id : '',
                url: response.data.url ? response.data.url : '',
                host: response.data.host ? response.data.host : '',
                displayName: response.data.displayName ? response.data.displayName : '',
                github: response.data.github ? response.data.github : '',
                profileImage: response.data.profileImage ? response.data.profileImage : ''
            }});

            const response_follower = await requests.get(`service/authors/${this.state.currentUser.id}/followers/`)
            this.setState({followerList: response_follower.data.items})

            const response_following = await requests.get(`service/authors/${this.state.currentUser.id}/following/`)
            this.setState({followingList: response_following.data.items})
        } catch(error) {
            console.log(error)
        }
        
    }

    sendFollowRequest = async () => {
        try {
            const data = {
                type: 'follow',
                summary: `${this.state.currentUser} wants to follow ${this.state.addFollowerId}`,
            }
            const response = await requests.post(`service/authors/${this.state.addFollowerId}/inbox/`,
                data,
                {headers: {
                Authorization: localStorage.getItem('access_token'),
                accept: 'application/json',
                }},
                {withCredentials:true})
        } catch(error) {
            this.setState({addFollowerError: "Failed to Send Follow Request"});
        }
    }

    setAddFollowerId = (e) => {
        this.setState({addFollowerId: e.target.value});
    }

    renderFollowers() {
        return this.state.followerList.map((follower) => {
            return (
                <Follower
                    displayName={follower.displayName}
                    profileImage={follower.profileImage}
                    currentUserId={this.state.currentUser.id}
                    id={follower.id}
                />
            );
        });
    }

    renderFollowing() {
        return this.state.followingList.map((follower) => {
            return (
                <Following
                    displayName={follower.displayName}
                    profileImage={follower.profileImage}
                    currentUserId={this.state.currentUser.id}
                    id={follower.id}
                />
            );
        });
    }

    render(){
        return (
            <div className="friendsPage">
            <Box sx={{ display: 'flex',
                       flexDirection: 'row',
                       p: 1,
                       m: 1,
                       justifyContent: 'center'
                    }}>
                Send a Follow Request To:
                <TextField id="outlined-basic" onChange={this.setAddFollowerId}/>
                <Button 
                startIcon={<PersonAddIcon />}
                onClick={this.sendFollowRequest}>
                Send
                </Button>
                {this.state.addFollowerError && (
                <Alert severity="error">
                {this.state.addFollowerError}
                </Alert>
                )}
            </Box>
            <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                    <h2>Followers</h2>
                    <List>
                        {this.renderFollowers()}
                    </List>
                </Grid>
                <Grid item xs={12} md={6}>
                    <h2>Following</h2>
                    <List>
                        {this.renderFollowing()}
                    </List>
                </Grid>
            </Grid>
            </div>
        )
    }
}

export default FriendsPage
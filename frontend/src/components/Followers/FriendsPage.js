import React from "react";
import requests from "../../requests";
import { Alert, Button, List, Grid, Box, TextField } from "@mui/material";
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import Follower from "./Follower";
import Following from "./Following";
import { BACKEND_URL } from "../../constants";
import getUuidFromAuthorUrl, { getAuthHeaderForNode } from "../../util";

class FriendsPage extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            currentUser: {},
            followerList: [],
            followingList: [],
            addFollowerId: '',
            addFollowerResult: {message:'', severity:''},
        }
    }

    componentDidMount() {
        this.initializeDetails();
    }

    initializeDetails = async () => {
        try {
            // Get the author details
            const response = await requests.get(BACKEND_URL + "/get-user/", {timeout:500});
            this.setState({ currentUser: {
                id: response.data.id ? response.data.id : '',
                url: response.data.url ? response.data.url : '',
                host: response.data.host ? response.data.host : '',
                displayName: response.data.displayName ? response.data.displayName : '',
                github: response.data.github ? response.data.github : '',
                profileImage: response.data.profileImage ? response.data.profileImage : ''
            }});

            const response_follower = await requests.get(`${this.state.currentUser.id}/followers/`)
            this.setState({followerList: response_follower.data.items})

            const response_following = await requests.get(`${this.state.currentUser.id}/following/`)
            this.setState({followingList: response_following.data.items})
        } catch(error) {
            console.log(error)
        }
        
    }

    sendFollowRequest = async () => {
        try {
            var data = {
                type: 'follow',
                summary: `${this.state.currentUser.displayName} wants to follow ${this.state.addFollowerId}`,
                object: `${this.state.addFollowerId}`,
                actor: `${this.state.currentUser.id}`,
            }
            // adapter for tik-tak-toe, remove when they fix their implementation
            if (this.state.addFollowerId.includes("http://tik-tak-toe-cmput404.herokuapp.com")) {
                // Create remote Followers object
                var follower_url = this.state.addFollowerId + "/followers/" + getUuidFromAuthorUrl(this.state.currentUser.id) + "/";
                const response = await requests.put(follower_url,
                    {},
                    getAuthHeaderForNode(follower_url),
                    {withCredentials: true});

                // Post follow to remote inbox
                data = {
                    type: "follow",
                    id: follower_url
                }
            }
            const url = `${this.state.addFollowerId}/inbox/`;
            const response = await requests.post(url,
                data,
                getAuthHeaderForNode(url),
                {withCredentials:true});
            this.setState({addFollowerResult: {message:"Sent Follow Request", severity:'success'}});
        } catch (e) {
            console.log(e)
            this.setState({addFollowerResult: {message:"Failed to send Follow Request", severity:'error'}});
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
            <Box
                sx={{ display: 'flex',
                       flexDirection: 'row',
                       p: 2,
                       m: 2,
                       ml: 10,
                       mr: 10,
                       justifyContent: 'center'
                    }}>
                Send a Follow Request To:
                <TextField 
                    fullWidth
                    placeholder="Enter author ID" 
                    id="outlined-basic"
                    onChange={this.setAddFollowerId}/>
                <Button 
                sx={{ml: 2}}
                startIcon={<PersonAddIcon />}
                onClick={this.sendFollowRequest}>
                Send
                </Button>
                {this.state.addFollowerResult && (
                <Alert severity={this.state.addFollowerResult.severity}>
                {this.state.addFollowerResult.message}
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
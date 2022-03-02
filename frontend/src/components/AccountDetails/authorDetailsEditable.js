import TextField from '@mui/material/TextField'
import React from 'react'

class AuthorDetailsEditable extends React.Component{
    render(){
        return (
            <div className='AuthorDetailsEditable'>
                <TextField id="url-input" label="Url" variant="outlined" />
                <TextField id="host-input" label="Host" variant="outlined" />
                <TextField id="displayName-input" label="Display Name" variant="outlined" />
                <TextField id="github-input" label="GitHub" variant="outlined" />
                <TextField id="profileImage-input" label="ProfileImage" variant="outlined"/>
            </div>
        );
    }
}

export default AuthorDetailsEditable
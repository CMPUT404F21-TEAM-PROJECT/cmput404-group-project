import TextField from '@mui/material/TextField'
import React from 'react'

class AuthorDetailsEditable extends React.Component{
    render(){
        return (
            <>
                <TextField id="url-input" label="Outlined" variant="outlined" />
                <TextField id="host-input" label="Outlined" variant="outlined" />
                <TextField id="displayName-input" label="Outlined" variant="outlined" />
                <TextField id="github-input" label="Outlined" variant="outlined" />
                <TextField id="profileImage-input" label="Outlined" variant="outlined" />
            </>
        );
    }
}

export default AuthorDetailsEditable
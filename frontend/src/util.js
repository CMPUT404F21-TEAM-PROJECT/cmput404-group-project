import { BACKEND_URL } from "./constants";

export default function getUuidFromAuthorUrl(url){
    // local url so get uuid only
    if (url.startsWith(BACKEND_URL)) {
        console.log("url from getuuid", url)
        var startIndex = url.indexOf("authors/") + 8;
        return url.substring(startIndex);
    // remote url so keep the whole thing
    } else {
        return url
    }
    
}

export function getAuthHeaderForNode(url){
    // this function extracts the node origin from the url
    // it then returns the auth_header required for that node 

    // dictionary to hold username:password for remote nodes
    const nodeAuthDict = {
        'http://tik-tak-toe-cmput404.herokuapp.com':'admin:tX7^iS8a5Ky$^S',
    }
    
    // extract node from url
    const url_obj = new URL(url)
    let auth_header = {};

    if (url_obj.origin == BACKEND_URL) {
        // Our own server
        auth_header = {headers: {
            Authorization: localStorage.getItem('access_token'),
            accept: 'application/json',
        }};
    } else if (url_obj.origin in nodeAuthDict) {
        auth_header = {headers: {
            Authorization: 'Basic ' + btoa(nodeAuthDict[url_obj.origin]),
            accept: 'application/json',
        }};
    } else {
        console.log(`auth not found for: ${url} with origin ${url_obj.origin}`);
    }
    console.log(`made auth header: ${auth_header}`);
    return auth_header
}

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
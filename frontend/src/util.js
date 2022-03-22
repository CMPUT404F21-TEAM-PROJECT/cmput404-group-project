function getUuidFromAuthorUrl(url){
    var startIndex = url.indexOf("authors/") + 8;
    return url.substring(startIndex);
}
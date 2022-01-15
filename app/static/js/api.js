function getApiToken() {
    return document.cookie.replace(/(?:^|.*;\s*)api_token\s*=\s*([^;]*).*$|^.*$/, "$1");
}
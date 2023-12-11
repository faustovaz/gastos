function post_to(link, kv_data, link_to_go) {
    fetch(link, {
        method: 'POST',
        contentType: 'application/json',
        body: JSON.stringify(kv_data)
    }).then((_res) => {
        window.location = link_to_go;
    });
}
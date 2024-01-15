function post_to(link, kv_data, link_to_go) {
    fetch(link, {
        method: 'POST',
        contentType: 'application/json',
        body: JSON.stringify(kv_data)
    }).then((_res) => {
        window.location = link_to_go;
    });
}

function delete_to(link, link_to_go) {
    let to_delete = confirm('Tem certeza que deseja remover o registro?');
    if (to_delete){
        fetch(link, {
            method: 'DELETE', 
            contentType: 'application/json'
        }).then((_res) => {
                window.location = link_to_go;
        });
    }
}
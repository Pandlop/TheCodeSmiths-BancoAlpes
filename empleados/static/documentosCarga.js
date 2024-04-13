function eliminarDoc(docId, row){
    let table = row.parentNode.parentNode;
    table.deleteRow(row.rowIndex);
    fetch(`${docId}`,{
        method:"DELETE"
    })
    .then(response => response.json())
    .then(data => console.log(data[0]))
    .catch(error => console.log(error));
}

function editarDoc(docId, row){
    let table = row.parentNode.parentNode;

    let doc;
    let docElem = document.getElementById("updateFile");
    docElem.addEventListener('change', function(event) {
        doc = event.target.files[0];
        if(doc){
            fetch(`${docId}`,{
                method:"PUT",
                body:doc
            })
            .then(response => response.json())
            .then(data => console.log(data[0]))
            .catch(error => console.log(error));
        }   
    });
    
}
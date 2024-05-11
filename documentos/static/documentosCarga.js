
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


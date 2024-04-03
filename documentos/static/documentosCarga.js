function eliminarDoc(docId, row){
    let table = row.parentNode.parentNode;
    table.deleteRow(row.rowIndex);
    fetch(`${docId}`,{
        method:"GET"
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.log(error));
}
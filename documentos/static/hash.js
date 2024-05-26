const llave_publica_endpoint = '/llave_publica_servidor/'; 

                        async function llaves() {
                            let inputs = document.querySelectorAll('input[type="file"]'); 
            
                            //Iniciar hash
                            var md = forge.md.sha256.create();
                            
                            //Form Data
                            let formData = new FormData();
                            
                            for (let input of inputs) {
                                let file = input.files[0];
                                let listaForm = {}
                                    
                                //Cifrar file
                                if (file) { // Asegúrate de que haya un archivo seleccionado
                                    await new Promise((resolve, reject) => {
                                        let reader = new FileReader();
                                        reader.onload = function(event) {
                                            const data = event.target.result;

                                            // Crear hash del archivo
                                            let md = forge.md.sha256.create();
                                            md.update(data);
                                            let hashFile = md.digest().toHex();                          
                                            
                                            formData.append(input.id + '_file', file);  // Agregar archivo como un campo aparte
                                            formData.append(input.id + '_hash', hashFile); // Agregar hash como otro campo // Agrega el archivo cifrado al formData
                                            resolve();
                                        };
                                        reader.onerror = () => reject(reader.error);
                                        reader.readAsBinaryString(file);
                                    });
                                }
                            }

                            
                            fetch('/documentos/documentosCarga/', {
                                method: 'POST',
                                body: formData,
                            })
                            .then(response => {
                                window.location.reload();
                                return response.json();  // Si todo va bien, continua procesando la respuesta
                            })
                            .then(data => {
                                console.log('Success:', data);
                            })
                            .catch(error => {
                                console.error('Error:', error);
                            });
                            
                            
                        }
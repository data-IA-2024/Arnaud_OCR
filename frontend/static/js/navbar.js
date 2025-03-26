

document.addEventListener("DOMContentLoaded", function() {
    const uploadLink = document.getElementById("invoice-upload-link");
    const fileInput = document.createElement("input");
    const dropZone = document.getElementById("drop-zone");
    const ocr_button = document.getElementById("OCR-button");

    fileInput.type = "file";
    fileInput.id = "name"
    fileInput.accept = "image/png, image/jpeg, image/jpg, image/webp";
    fileInput.style.display = "none";
    document.body.appendChild(fileInput);

    if (uploadLink) {
        uploadLink.addEventListener("click", function(e) {
            e.preventDefault();
            fileInput.click();
        });

    }
    if (ocr_button){
        ocr_button.addEventListener("click", () => send_file(),{once: true})
    }

    if (dropZone) {
        dropZone.addEventListener("click", function() {
            fileInput.click();
        });

        dropZone.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropZone.classList.add("dragover");
        });

        dropZone.addEventListener("dragleave", () => {
            dropZone.classList.remove("dragover");
        });

        dropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropZone.classList.remove("dragover");
            handleFile(e.dataTransfer.files[0]);
        });
    } else {
        console.error("Element #drop-zone non trouvé");
    }

    fileInput.addEventListener("change", function() {
        if (this.files && this.files[0]) {
            handleFile(this.files[0]);
        }
    });

    function handleFile(file) {
        if (file) {
            const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
            if (allowedTypes.includes(file.type)) {
                displayPreview(file);
            } else {
                alert("Veuillez sélectionner une image au format PNG, JPEG, JPG ou WebP.");
            }
        }
    }

    function displayPreview(file) {
        console.log("Fichier sélectionné :", file.name);
        
        const container = document.createElement("div");
        container.className = "d-flex align-items-start";
        
        const imageContainer = document.createElement("div");
        imageContainer.className = "position-relative me-3";
        imageContainer.style.width = "300px";
        imageContainer.style.height = "300px";
        
        const img = document.createElement("img");
        img.id = "image"
        img.style.width = "300%";
        img.style.height = "300%";
        img.style.objectFit = "contain";
        img.classList.add("border")
        img.classList.add("border-dark")

    
        const reader = new FileReader();
        console.log("reader initialiséé :");
        reader.onload = function(e) {
            console.log("loading file");
            img.src = e.target.result;
            imageContainer.appendChild(img);

                // Ajoutez ici la logique pour lancer le processus OCR
        };
            
        container.appendChild(imageContainer);
            //container.appendChild(ocrButton);
            /*
unable button when image loaded

            */
            
        if (dropZone) {
            dropZone.innerHTML = '';
            dropZone.appendChild(container);
        } else {
            console.error("Element #drop-zone non trouvé lors de l'affichage de l'aperçu");
        }
        imageData=reader.readAsDataURL(file);
        document.getElementById("OCR-button").classList.remove("disabled");
    };
    async function send_file(){
        let image = document.getElementById("name").files[0];
        let form_Data = new FormData();
        form_Data.append("file", image)
        let picture = fetch('/OCR',{method: "POST", body: form_Data}).then(response => {
            if (!response.ok) {
                throw new Error('OCR extraction failed');
            }
            return response.json();
        })
        .then(result => {
            console.log('OCR extraction successful:', result);
            console.log('OCR Text: ' + result.filename);
        })
        .catch(error => {
            console.error('Error during OCR extraction:', error);
            console.error('OCR extraction failed: ' + error.message);
        });;
    }
    
    
});
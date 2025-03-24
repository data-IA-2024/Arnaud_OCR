document.addEventListener("DOMContentLoaded", function() {
    const uploadLink = document.getElementById("invoice-upload-link");
    const fileInput = document.createElement("input");
    const dropZone = document.getElementById("drop-zone");

    fileInput.type = "file";
    fileInput.accept = "image/png, image/jpeg, image/jpg, image/webp";
    fileInput.style.display = "none";
    document.body.appendChild(fileInput);

    if (uploadLink) {
        uploadLink.addEventListener("click", function(e) {
            e.preventDefault();
            fileInput.click();
        });
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
        img.style.width = "300%";
        img.style.height = "300%";
        img.style.objectFit = "contain";
    
        const reader = new FileReader();
        reader.onload = function(e) {
            img.src = e.target.result;
            imageContainer.appendChild(img);
    ;
                // Ajoutez ici la logique pour lancer le processus OCR
            };
            
            container.appendChild(imageContainer);
            container.appendChild(ocrButton);
            
            if (dropZone) {
                dropZone.innerHTML = '';
                dropZone.appendChild(container);
            } else {
                console.error("Element #drop-zone non trouvé lors de l'affichage de l'aperçu");
            }
        };
        
        reader.readAsDataURL(file);
    
});

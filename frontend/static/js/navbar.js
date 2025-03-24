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

    dropZone.addEventListener("click", function() {
        fileInput.click();
    });

    fileInput.addEventListener("change", function() {
        if (this.files && this.files[0]) {
            handleFile(this.files[0]);
        }
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
        
        // Créer un conteneur flex pour l'image et le bouton
        const container = document.createElement("div");
        container.className = "d-flex align-items-start";
        
        // Créer le conteneur de l'image
        const imageContainer = document.createElement("div");
        imageContainer.className = "position-relative";
        imageContainer.style.width = "300px";
        imageContainer.style.height = "300px";
        
        const img = document.createElement("img");
        img.style.width = "163%";
        img.style.height = "214%";
        img.style.objectFit = "cover";

        
        const reader = new FileReader();
        reader.onload = function(e) {
            img.src = e.target.result;
            imageContainer.appendChild(img);
            
            // Créer le bouton OCR
            const ocrButton = document.createElement("button");
            ocrButton.textContent = "OCR";
            ocrButton.className = "btn btn-primary"; // ms-3 ajoute une marge à gauche
            ocrButton.onclick = function() {
                console.log("Lancement du processus OCR");
                // Ajoutez ici la logique pour lancer le processus OCR
            };
            
            // Ajouter l'image et le bouton OCR au conteneur flex
            container.appendChild(imageContainer);
            
            
            // Remplacer le contenu de la zone de dépôt
            const dropZone = document.getElementById("drop-zone");
            dropZone.innerHTML = '';
            dropZone.appendChild(container);
        };
        
        reader.readAsDataURL(file);
    }
    
    
});

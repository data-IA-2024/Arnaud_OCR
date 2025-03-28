document.addEventListener("DOMContentLoaded", function() {
    const lienUpload = document.getElementById("invoice-upload-link");
    const inputFichier = document.createElement("input");
    const zoneDepot = document.getElementById("drop-zone");
    const boutonOCR = document.getElementById("OCR-button");

    // Configuration de l'input fichier
    inputFichier.type = "file";
    inputFichier.id = "fichier-facture";
    inputFichier.accept = "image/png, image/jpeg, image/jpg, image/webp";
    inputFichier.style.display = "none";
    document.body.appendChild(inputFichier);

    // Gestionnaire pour le lien d'upload
    if (lienUpload) {
        lienUpload.addEventListener("click", function(e) {
            e.preventDefault();
            inputFichier.click();
        });
    }

    // Gestionnaire pour le bouton OCR
    if (boutonOCR) {
        boutonOCR.addEventListener("click", () => envoyerFichier());
    }

    // Gestion de la zone de dépôt
    if (zoneDepot) {
        zoneDepot.addEventListener("click", () => inputFichier.click());

        zoneDepot.addEventListener("dragover", (e) => {
            e.preventDefault();
            zoneDepot.classList.add("survol");
        });

        zoneDepot.addEventListener("dragleave", () => {
            zoneDepot.classList.remove("survol");
        });

        zoneDepot.addEventListener("drop", (e) => {
            e.preventDefault();
            zoneDepot.classList.remove("survol");
            gererFichier(e.dataTransfer.files[0]);
        });
    }

    // Gestion du changement de fichier
    inputFichier.addEventListener("change", function() {
        if (this.files && this.files[0]) {
            gererFichier(this.files[0]);
        }
    });

    function gererFichier(fichier) {
        const typesAutorises = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
        if (typesAutorises.includes(fichier.type)) {
            afficherApercu(fichier);
            boutonOCR.classList.remove("desactive");
        } else {
            alert("Format d'image non supporté. Veuillez utiliser PNG, JPEG, JPG ou WebP.");
        }
    }

    function afficherApercu(fichier) {
        const conteneur = document.createElement("div");
        conteneur.className = "apercu-facture";

        const lecteur = new FileReader();
        
        lecteur.onload = function(e) {
            const image = document.createElement("img");
            image.src = e.target.result;
            image.alt = "Aperçu de la facture";
            conteneur.appendChild(image);
            
            zoneDepot.innerHTML = '';
            zoneDepot.appendChild(conteneur);
        };
        
        lecteur.readAsDataURL(fichier);
    }

    async function envoyerFichier() {
        const inputFichier = document.getElementById('fichier-facture');
        const fichier = inputFichier.files[0];
        const formData = new FormData();
        formData.append("file", fichier);
        console.log(formData)

        try {
            const reponse = await fetch('/OCR', {
                method: "POST",
                body: formData
            });

            if (!reponse.ok) {
                throw new Error('Échec de l\'extraction OCR');
            }
            const resultat = await reponse.json();
            console.log('Résultat OCR:', resultat);
            afficherResultats(resultat);

        } catch (erreur) {
            console.error('Erreur:', erreur);
            alert("Une erreur est survenue lors du traitement de la facture");
        }
    }
    function capitalizeFirstLetter(val) {
        return String(val).charAt(0).toUpperCase() + String(val).slice(1);
    }
    function formatKey(key){
        return capitalizeFirstLetter(key.replace("_", " "))
    }


    function afficherResultats(donnees) {
        const conteneurResultats = document.getElementById("ocr-results");
        conteneurResultats.innerHTML = '<h3>Informations extraites</h3>'
        for (const [key, value] of Object.entries(donnees)){
            conteneurResultats.innerHTML +=`<p><b>${formatKey(key)}:</b> ${value}</p>`
        }
        
        /*conteneurResultats.innerHTML = `
            <h3>Informations extraites</h3>
            <p>Numéro de facture: ${donnees.numero_facture}</p>
            <p>Date: ${donnees.date}</p>
            <p>Nom: ${donnees.nom}</p>
            <p>Montant total: ${donnees.montant} €</p>
        `;*/
    }
});
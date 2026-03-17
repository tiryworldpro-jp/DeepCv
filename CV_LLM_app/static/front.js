const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('files');
const submitBtn = document.getElementById('submit');
const status = document.getElementById('status');

const zoneResultat = document.getElementById('zone-resultat');
const contenuCv = document.getElementById('contenu-cv');
const promptInput = document.getElementById('user-prompt');
const resetBtn = document.getElementById('reset-btn');

let files = [];

// Click pour ouvrir
dropzone.onclick = () => fileInput.click();

dropzone.ondragover = (e) => {
    e.preventDefault();
    dropzone.classList.add('hover');
};

dropzone.ondragleave = () => dropzone.classList.remove('hover');

dropzone.ondrop = (e) => {
    e.preventDefault();
    dropzone.classList.remove('hover');
    updateFiles(e.dataTransfer.files);
};

fileInput.onchange = (e) => updateFiles(e.target.files);


// Envoi
submitBtn.onclick = async () => {
    if (files.length === 0 && promptInput.value.trim() === "") {
        alert('Sélectionnez des fichiers ou entrez un prompt');
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Envoi...';

    const formData = new FormData();

    if (files.length > 0) {
        files.forEach(f => formData.append('cv', f));
    }

    formData.append('prompt', promptInput.value);
    try {
        const res = await fetch('/analyse', {
            method: 'POST',
            body: formData
        });

        const data = await res.json();

        if (res.ok) {
            status.textContent = data.message;
            status.className = 'success';
            
            resetBtn.style.display = 'block';

            const listeCVs = data.data;

            if (zoneResultat) {
                zoneResultat.style.display = 'block';
                zoneResultat.innerHTML = "";

                listeCVs.forEach(cv => {
                    const box_result = document.createElement('div');

                    box_result.className = 'cv-card';

                    box_result.innerHTML = `
                       <h3>${cv.nom_fichier}</h3>          
                        <div class="cv-stats">
                            <p><strong>Pertinence Max : ${cv.pertinence} %</strong></p>
                        </div>
                        <div style="background: #e6fffa; padding: 10px; border-left: 5px solid #38b2ac; margin-bottom: 15px;">
                            <p style="color: #2c7a7b; font-weight: bold; margin-bottom: 5px;">Passage le plus pertinent :</p>
                            <p style="font-style: italic;">"${cv.meilleur_extrait}"</p>
                        </div>`;
                        
                        zoneResultat.appendChild(box_result);
                    });
                }

            files = [];
            fileInput.value = '';
            dropzone.querySelector('p').textContent = 'Glissez vos fichiers ici';
        } else {
            status.textContent = 'Erreur: ' + data.error;
            status.className = 'error';
        }
    } catch (err) {
        status.textContent = 'Erreur serveur';
        status.className = 'error';
        console.log(err);
    }

    submitBtn.disabled = false;
    submitBtn.textContent = 'Sauvegarder';
};

//reintialiser la memoire
resetBtn.onclick = async () => {
    resetBtn.disabled = true;
    resetBtn.textContent = 'Nettoyage...';

    try {
        const res = await fetch('/reset', {
            method: 'POST'
        });

        const data = await res.json();

        if (res.ok) {
            status.textContent = data.message;
            status.className = 'success';
            
            if (zoneResultat) zoneResultat.style.display = 'none';
            files = [];
            dropzone.querySelector('p').textContent = 'Glissez vos fichiers ici ou parcourir';
            
            fileInput.value = ''; 
            resetBtn.style.display = 'none';

        } else {
            status.textContent = 'Erreur lors du reset';
            status.className = 'error';
        }
    } catch (err) {
        console.error(err);
        status.textContent = 'Erreur serveur';
        status.className = 'error';
    }

    resetBtn.disabled = false;
    resetBtn.textContent = 'Réinitialiser';
};

// rajout fichiers
function updateFiles(newFiles) {
    const nouveauxFichiers = Array.from(newFiles);
    nouveauxFichiers.forEach(nouveau => {
        if (!files.some(f => f.name === nouveau.name)) {
            files.push(nouveau);
        }
    });

    const p = dropzone.querySelector('p');

    if (files.length > 0) {
        p.innerHTML = `
            <span style="font-weight: bold; font-size: 1.1em; color: #2d3748;">
                ${files.length} fichier(s) prêt(s) à l'analyse
            </span>
            <br>
            <span style="font-size: 0.85em; opacity: 0.7;">
                Glissez d'autres fichiers ici ou <span class="link">parcourir</span>
            </span>
        `;
    } else {
        p.innerHTML = 'Glissez vos fichiers ici ou <span class="link">parcourir</span>';
    }
}
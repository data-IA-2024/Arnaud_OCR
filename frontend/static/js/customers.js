document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById('searchInput');
    const searchType = document.getElementById('searchType');
    const tableBody = document.getElementById('customers-table');

    const debounce = (func, delay = 300) => {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    };

    const updateTable = async (searchTerm = '') => {
        try {
            const type = searchType.value;
            const response = await fetch(`/api/customers?${type}=${encodeURIComponent(searchTerm)}`);
            if (!response.ok) throw new Error('Erreur réseau');
            
            const data = await response.json();
            
            tableBody.innerHTML = data.length > 0 
                ? data.map(customer => `
                    <tr>
                        <td>${customer.email}</td>
                        <td>${customer.name}</td>
                        <td>${customer.gender || 'N/A'}</td>
                        <td>${customer.adress || 'N/A'}</td>
                        <td>${customer.birth || 'N/A'}</td>
                    </tr>
                `).join('')
                : `<tr><td colspan="5" class="text-center">Aucun client trouvé</td></tr>`;
        } catch (error) {
            console.error('Erreur:', error);
            tableBody.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Erreur de chargement</td></tr>`;
        }
    };

    searchInput.addEventListener('input', debounce(e => updateTable(e.target.value.trim())));
    searchType.addEventListener('change', () => updateTable(searchInput.value.trim()));

    // Chargement initial
    updateTable();
});

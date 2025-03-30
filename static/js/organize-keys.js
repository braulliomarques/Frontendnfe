// Função para formatar CNPJ com pontuação correta
function formatCNPJ(cnpj) {
    return cnpj.replace(/^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/, '$1.$2.$3/$4-$5');
}

// Function to organize keys by CNPJ
function organizeKeysByCNPJ() {
    const table = document.getElementById('nfe-keys-table');
    const rows = Array.from(table.querySelectorAll('tr.key-row'));
    
    if (rows.length === 0) return;
    
    // Update total keys count
    document.getElementById('totalKeysCount').textContent = rows.length;
    
    // Remove all rows from the table
    rows.forEach(row => row.remove());
    
    // Group rows by CNPJ
    const cnpjGroups = {};
    rows.forEach(row => {
        const cnpj = row.getAttribute('data-cnpj');
        if (!cnpjGroups[cnpj]) {
            cnpjGroups[cnpj] = [];
        }
        cnpjGroups[cnpj].push(row);
    });
    
    // Add grouped rows back to the table
    Object.keys(cnpjGroups).sort().forEach(cnpj => {
        const formattedCNPJ = formatCNPJ(cnpj);
        const groupCount = cnpjGroups[cnpj].length;
        
        // Create group header
        const headerRow = document.createElement('tr');
        headerRow.className = 'cnpj-group-header';
        headerRow.setAttribute('data-cnpj', cnpj);
        headerRow.innerHTML = `
            <td colspan="7">
                <i class="fas fa-caret-right cnpj-toggle-icon"></i>
                CNPJ: <span class="cnpj-formatted">${formattedCNPJ}</span>
                <span class="badge bg-primary ms-2">${groupCount} chave(s)</span>
            </td>
        `;
        
        // Add click event to toggle group visibility
        headerRow.addEventListener('click', function() {
            const cnpj = this.getAttribute('data-cnpj');
            const icon = this.querySelector('.cnpj-toggle-icon');
            icon.classList.toggle('open');
            
            const groupRows = table.querySelectorAll(`tr.key-row[data-cnpj="${cnpj}"]`);
            groupRows.forEach(row => {
                row.classList.toggle('cnpj-group-hidden');
            });
        });
        
        table.appendChild(headerRow);
        
        // Add group rows
        cnpjGroups[cnpj].forEach(row => {
            // Hide rows by default
            row.classList.add('cnpj-group-hidden');
            table.appendChild(row);
        });
    });
}

// Garante que a função esteja disponível globalmente
window.organizeKeysByCNPJ = organizeKeysByCNPJ; 
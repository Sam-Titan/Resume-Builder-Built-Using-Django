// Add this to your existing JavaScript or create a new file
function initializeFormsetManagement() {
    const formsetConfigs = {
        education: {
            prefix: 'education',
            container: '.education-forms'
        },
        experience: {
            prefix: 'experience',
            container: '.experience-forms'
        },
        // Add similar configs for other formsets
    };

    // Handle adding new formset items
    function addFormsetItem(formsetName) {
        const config = formsetConfigs[formsetName];
        const container = document.querySelector(config.container);
        const totalForms = document.querySelector(`#id_${config.prefix}-TOTAL_FORMS`);
        
        // Clone template
        const newForm = container.querySelector('.formset-item').cloneNode(true);
        const formNum = parseInt(totalForms.value);
        
        // Update form index
        newForm.innerHTML = newForm.innerHTML.replace(
            new RegExp(`${config.prefix}-\\d+-`, 'g'),
            `${config.prefix}-${formNum}-`
        );
        
        // Clear form values
        newForm.querySelectorAll('input, textarea, select').forEach(input => {
            input.value = '';
            if (input.type === 'checkbox') {
                input.checked = false;
            }
        });
        
        // Add delete button
        const deleteBtn = document.createElement('button');
        deleteBtn.type = 'button';
        deleteBtn.className = 'delete-formset';
        deleteBtn.innerHTML = '&times;';
        deleteBtn.onclick = () => deleteFormsetItem(newForm, formsetName);
        newForm.appendChild(deleteBtn);
        
        // Update total forms
        totalForms.value = formNum + 1;
        
        // Add to container
        container.appendChild(newForm);
        
        // Trigger preview update
        updatePreview();
    }

    // Handle deleting formset items
    function deleteFormsetItem(item, formsetName) {
        const config = formsetConfigs[formsetName];
        const container = item.closest(config.container);
        
        // Don't delete if it's the last form
        if (container.querySelectorAll('.formset-item').length > 1) {
            // Mark for deletion if the form is part of an existing record
            const deleteInput = item.querySelector(`input[name$="-DELETE"]`);
            if (deleteInput) {
                deleteInput.value = 'on';
                item.style.display = 'none';
            } else {
                item.remove();
            }
            
            // Trigger preview update
            updatePreview();
        }
    }

    // Initialize add buttons
    Object.keys(formsetConfigs).forEach(formsetName => {
        const addBtn = document.querySelector(`button[data-formset="${formsetName}"]`);
        if (addBtn) {
            addBtn.onclick = () => addFormsetItem(formsetName);
        }
    });

    // Initialize delete buttons
    document.querySelectorAll('.delete-formset').forEach(btn => {
        const formsetName = btn.closest('[data-section]').dataset.section;
        btn.onclick = () => deleteFormsetItem(btn.closest('.formset-item'), formsetName);
    });
}

// Call this function when the document loads
document.addEventListener('DOMContentLoaded', initializeFormsetManagement);
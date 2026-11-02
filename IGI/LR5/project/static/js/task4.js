const createBtn = document.getElementById('create_phone');
const createBox = document.getElementById('place_create');

let saved = JSON.parse(localStorage.getItem('forms') || '[]');

if (!Array.isArray(saved)) {
    saved = [];
}

const name_i = document.querySelector('.attr-name');
const placeholder = document.querySelector('.attr-placeholder');
const value_i = document.querySelector('.attr-value');
const pattern = document.querySelector('.attr-pattern');
const required = document.querySelector('.attr-required');
const maxlength = document.querySelector('.attr-maxlength');

function updateInput(input, data = null) {

    const settings = data || {
        name: name_i.value,
        placeholder: placeholder.value,
        value: value_i.value,
        pattern: pattern.value,
        required: required.checked,
        maxlength: maxlength.value
    };
    if (settings.name) {
        input.setAttribute('name', settings.name);
    } else {
        input.removeAttribute('name');
    }
    if (settings.placeholder) {
        input.setAttribute('placeholder', settings.placeholder);
    } else {
        input.removeAttribute('placeholder');
    }
    input.value = settings.value || '';
    if (settings.pattern) {
        input.setAttribute('pattern', settings.pattern);
    } else {
        input.removeAttribute('pattern');
    }
    input.required = settings.required || false;
    if (settings.maxlength) {
        input.setAttribute('maxlength', settings.maxlength);
    } else {
        input.removeAttribute('maxlength');
    }
}

function saveForms() {
    const forms = [...createBox.querySelectorAll('.generated-form')];

    const data = forms.map(form => {
        const input = form.querySelector('.input');

        return {
            name: input.getAttribute('name') || '',
            placeholder: input.getAttribute('placeholder') || '',
            value: input.value,
            pattern: input.getAttribute('pattern') || '',
            required: input.required,
            maxlength: input.getAttribute('maxlength') || ''
        };
    });

    localStorage.setItem('forms', JSON.stringify(data));
}

function create_input(data = null) {

    const form = document.createElement('form');
    form.className = 'generated-form';

    const input = document.createElement('input');
    input.type = 'tel';
    input.className = 'input';

    updateInput(input, data);

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Удалить форму';
    deleteBtn.type = 'button';

    deleteBtn.addEventListener('click', () => {
        form.remove();
        saveForms();
    });

    input.addEventListener('input', saveForms);

    form.appendChild(input);
    form.appendChild(deleteBtn);

    createBox.appendChild(form);

    saveForms();
}

saved.forEach(data => create_input(data));

createBtn.addEventListener('click', () => create_input());
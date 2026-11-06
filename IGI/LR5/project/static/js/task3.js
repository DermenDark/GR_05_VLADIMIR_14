import { createPagination } from "./pagination.js";
const table = document.querySelector("#employees-table");
const headers = [...document.querySelectorAll(".capital_table")];
const pager = document.querySelector(".pages_button");
const preloader = document.querySelector(".preloader-demo");
const perPage = 3;

let employees = [];
let filteredEmployees = [];
let filterText = "";

let activeHeader = null;
const selectedEmployees = new Map();

let nextOrder = 0;


const pagination = createPagination(pager, perPage, renderPage);


function renderPage(pageEmployees) {

    preloader.hidden = false;
    table.innerHTML = "";

    if (pageEmployees.length === 0) {
        table.innerHTML = `
            <tr>
                <td colspan="7">Сотрудники не найдены.</td>
            </tr>
        `;
    }

    pageEmployees.forEach(employee => {

        const row = document.createElement("tr");
        const photoCell = document.createElement("td");

        if (employee.photo) {
            const img = document.createElement("img");
            img.src = employee.photo;
            img.alt = employee.name;
            img.width = 70;
            photoCell.appendChild(img);
        } else {
            photoCell.textContent = "Нет фото";
        }

        row.appendChild(photoCell);
        [
            employee.name,
            employee.department,
            employee.description,
            employee.phone,
            employee.email
        ].forEach(value => {
            const cell = document.createElement("td");
            cell.textContent = value || "";
            row.appendChild(cell);
        });
        const cell = document.createElement("td");
        const checkbox = document.createElement("input");

        checkbox.type = "checkbox";
        checkbox.className = "earn-checkbox";
        checkbox.checked = selectedEmployees.has(String(employee.id));

        checkbox.addEventListener("change", () => {
            addEmploerPremi(employee, checkbox.checked);
        });

        cell.appendChild(checkbox);
        row.appendChild(cell);
        row.addEventListener("click", event => {
            if (event.target.closest("input, button, a")) return;

            showEmployeeDetails(employee);
        });

        table.appendChild(row);
    });
    requestAnimationFrame(() => {
        preloader.hidden = true;
    });
}


headers.forEach(header => {
    header.dataset.direction = "1";

    header.addEventListener("click", () => {
        sort_by(header);
    });
});

function sort_by(header) {
    if (activeHeader !== header) {

        employees.sort((a, b) => a.order - b.order);

        headers.forEach(item => {
            item.dataset.direction = "1";
        });

        activeHeader = header;
    }

    const direction = Number(header.dataset.direction);
    const field = header.dataset.sort;

    employees.sort((a, b) => {

        const textA = String(a[field] || "");
        const textB = String(b[field] || "");

        return textA.localeCompare(
            textB,
            "ru",
            { numeric: true, sensitivity: "base" }
        ) * direction || a.order - b.order;
    });

    header.dataset.direction = -direction;

    document.querySelector("#sort-status").textContent =
        `Сортировка: ${header.textContent.trim()} — ${direction === 1 ? "по возрастанию" : "по убыванию"
        }`;

    applyFilter();
}


const filterForm = document.querySelector("#employee-filter");
const searchInput = document.querySelector("#employee-search");

filterForm.addEventListener("submit", event => {

    event.preventDefault();

    filterText = searchInput.value.trim().toLocaleLowerCase("ru");

    applyFilter();
});

function applyFilter() {

    filteredEmployees = employees.filter(employee => {

        const text = [
            employee.name,
            employee.department,
            employee.description,
            employee.phone,
            employee.email
        ].join(" ").toLocaleLowerCase("ru");

        return text.includes(filterText);
    });

    pagination.setItems(filteredEmployees, 1);
}


function showEmployeeDetails(employee) {

    const details = document.querySelector("#employee-details");

    details.innerHTML = "<h2>Информация о сотруднике</h2>";

    if (employee.photo) {
        const img = document.createElement("img");
        img.src = employee.photo;
        img.alt = employee.name;
        img.width = 120;
        details.appendChild(img);
    }

    const fields = {
        "ФИО": employee.name,
        "Отдел": employee.department,
        "Описание": employee.description,
        "Телефон": employee.phone,
        "Почта": employee.email
    };

    Object.entries(fields).forEach(([key, value]) => {

        const p = document.createElement("p");
        p.textContent = `${key}: ${value || "Не указано"}`;

        details.appendChild(p);
    });

    if (employee.url) {
        const link = document.createElement("a");
        link.href = employee.url;
        link.target = "_blank";
        link.rel = "noopener";
        link.textContent = "Страница сотрудника";

        details.appendChild(link);
    }
}

function addEmploerPremi(employee, checked) {

    const id = String(employee.id);

    if (checked) {
        selectedEmployees.set(id, employee);
    } else {
        selectedEmployees.delete(id);
    }
}

document.querySelector("#premiate-selected").addEventListener("click", () => {

    const names = [...selectedEmployees.values()].map(employee =>
        employee.name.trim().split(/\s+/)[0]
    );

    const result = document.querySelector("#premium-result");

    result.textContent = names.length
        ? `Предлагается премировать сотрудников: ${names.join(", ")}.`
        : "Выберите сотрудников для премирования.";
});


const addPanel = document.querySelector("#add-employee-panel");

document.querySelector("#show-add-form").addEventListener("click", () => {
    addPanel.hidden = !addPanel.hidden;
});

const addForm = document.querySelector("#employee-add-form");
const addButton = document.querySelector("#add-employee-submit");

const nameInput = document.querySelector("#new-name");
const photoInput = document.querySelector("#new-photo");
const urlInput = document.querySelector("#new-url");
const descriptionInput = document.querySelector("#new-description");
const phoneInput = document.querySelector("#new-phone");
const emailInput = document.querySelector("#new-email");

function validateURL(value) {

    try {
        const url = new URL(value);

        return (
            ["http:", "https:"].includes(url.protocol) &&
            /\.(php|html)$/i.test(url.pathname)
        );
    } catch {
        return false;
    }
}

function validatePhone(value) {

    return /^(?:\+375\s*\(?29\)?|8\s*\(?029\)?)[\s-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}$/
        .test(value.trim());
}

function showValidation(input, result, valid, title) {

    input.classList.toggle(
        "field-invalid",
        input.value.trim() !== "" && !valid
    );

    result.textContent = !input.value.trim()
        ? ""
        : valid
            ? `${title}: корректно`
            : `${title}: некорректно`;
}


function checkAddForm() {

    const urlValid = validateURL(urlInput.value);
    const phoneValid = validatePhone(phoneInput.value);

    showValidation(
        urlInput,
        document.querySelector("#url-result"),
        urlValid,
        "URL"
    );

    showValidation(
        phoneInput,
        document.querySelector("#phone-result"),
        phoneValid,
        "Телефон"
    );

    const fieldsFilled = [...addForm.querySelectorAll("[required]")]
        .every(input => input.type === "file"
            ? input.files.length > 0
            : input.value.trim() !== ""
        );

    addButton.disabled = !(
        fieldsFilled &&
        addForm.checkValidity() &&
        urlValid &&
        phoneValid
    );
}

addForm.addEventListener("input", checkAddForm);
addForm.addEventListener("change", checkAddForm);

addForm.addEventListener("submit", event => {

    event.preventDefault();
    checkAddForm();

    if (addButton.disabled) return;

    const employee = {
        id: "local-" + Date.now(),

        name: nameInput.value.trim(),
        department: "Не указан",
        description: descriptionInput.value.trim(),
        phone: phoneInput.value.trim(),
        email: emailInput.value.trim(),

        url: urlInput.value.trim(),
        photo: URL.createObjectURL(photoInput.files[0]),

        order: nextOrder++
    };

    employees.push(employee);
    if (activeHeader) {
        const field = activeHeader.dataset.sort;
        const direction = -Number(activeHeader.dataset.direction);

        employees.sort((a, b) =>
            String(a[field] || "").localeCompare(
                String(b[field] || ""),
                "ru",
                { numeric: true, sensitivity: "base" }
            ) * direction || a.order - b.order
        );
    }
    searchInput.value = "";
    filterText = "";

    addForm.reset();
    addButton.disabled = true;
    addPanel.hidden = true;

    applyFilter();
    showEmployeeDetails(employee);
});


async function loadEmployees() {

    preloader.hidden = false;

    try {
        const response = await fetch(table.dataset.url);

        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }

        const result = await response.json();

        employees = result.employees.map((employee, index) => ({
            ...employee,
            order: index
        }));

        nextOrder = employees.length;

        applyFilter();

    } catch (error) {

        console.error("Ошибка загрузки:", error);
        table.innerHTML = `
            <tr>
                <td colspan="7">Не удалось загрузить сотрудников.</td>
            </tr>
        `;
        preloader.hidden = true;
    }
}

loadEmployees();
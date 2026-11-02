const box_catalog = document.querySelector(".catalog-grid");
const product = [...box_catalog.querySelectorAll('.product-card')];

const box_pager = document.querySelector(".pages_button");

const perPage = 3;
const MaxPage = Math.ceil(product.length / perPage);

for (let i = 0; i < MaxPage; i++) {
    const pagesBtn = document.createElement('button');

    pagesBtn.textContent = i + 1;
    pagesBtn.type = 'button';

    pagesBtn.addEventListener('click', () => {
        apply_page(i + 1);
    });

    box_pager.appendChild(pagesBtn);
}

function apply_page(page) {
    const start = (page - 1) * perPage;
    const end = start + perPage;

    product.forEach((card, index) => {
        card.hidden = index < start || index >= end;
    });

    [...box_pager.querySelectorAll('button')].forEach((button, index) => {
        button.classList.toggle('active', index + 1 === page);
    });
}

apply_page(1);
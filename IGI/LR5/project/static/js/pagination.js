export function createPagination(pager, perPage, onPageChange) {

    let items = [];

    function apply_page(page) {

        const start = (page - 1) * perPage;
        const end = start + perPage;

        const visible = items.slice(start, end);

        pager.innerHTML = "";

        const MaxPage = Math.ceil(items.length / perPage);

        for (let i = 0; i < MaxPage; i++) {

            const pagesBtn = document.createElement("button");

            pagesBtn.textContent = i + 1;
            pagesBtn.type = "button";

            pagesBtn.classList.toggle("active", i + 1 === page);

            pagesBtn.addEventListener("click", () => {
                apply_page(i + 1);
            });

            pager.appendChild(pagesBtn);
        }

        onPageChange(visible);
    }

    return {
        setItems(newItems, page = 1) {
            items = newItems;
            const maxPage = Math.ceil(items.length / perPage);
            apply_page(Math.min(page, maxPage || 1));
        }
    };
}
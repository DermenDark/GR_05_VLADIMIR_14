import { createPagination } from "./pagination.js";

const box_catalog = document.querySelector(".catalog-grid");
const product = [...box_catalog.querySelectorAll(".product-card")];

const box_pager = document.querySelector(".pages_button");

const pagination = createPagination(
    box_pager,
    3,
    visibleProducts => {

        product.forEach(card => card.hidden = true);

        visibleProducts.forEach(card => card.hidden = false);
    }
);

pagination.setItems(product);
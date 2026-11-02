const cards = document.querySelectorAll(".product-card");

function mousemv(card_w, offsetX, offsetY) {

    const rect = card_w.getBoundingClientRect();

    const width = rect.width;
    const height = rect.height;
    const middleX = width / 2;
    const middleY = height / 2;
    const x = ((offsetX - middleX) / middleX);
    const y = ((offsetY - middleY) / middleY);

    const rotateX = -y * 15;
    const rotateY = x * 10;

    requestAnimationFrame(() => {
        card_w.style.transform = `
            perspective(500px)
            rotateX(${rotateX}deg)
            rotateY(${5 + rotateY}deg)
        `;
    });
}
function mouselv(card_w) {
    console.log("leave", cards.values)
    requestAnimationFrame(() => {
        card_w.classList.remove('is-hovered', 'is-clicked');
        card_w.style.transform = '';
        card_w.style.setProperty('--posx', '50%');
        card_w.style.setProperty('--posy', '50%');
    });
}
function mouseent(card_w, offsetX, offsetY) {
    card_w.classList.add('is-hovered');
}
function tremble(card_w, offsetX, offsetY) {
    card_w.classList.remove('is-clicked');
    card_w.classList.add('is-clicked');
    clickTimer = setTimeout(() => {
        card_w.classList.remove('is-clicked');
    }, 500);
}

cards.forEach(
    card_w => {
        card_w.addEventListener('mouseenter', (event) => { mouseent(card_w, event.offsetX, event.offsetY) });
        card_w.addEventListener('mousemove', (event) => { mousemv(card_w, event.offsetX, event.offsetY) });
        card_w.addEventListener('mouseleave', () => mouselv(card_w));
        card_w.onclick = (event) => { tremble(card_w, event.offsetX, event.offsetY); }
    }
);
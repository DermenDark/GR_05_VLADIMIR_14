const box = document.querySelector("#box");
const image = box.dataset.bottle;
const rows = 40;
const columns = 80;

for (let row = 0; row < rows; row++) {
    for (let col = 0; col < columns; col++) {
        if ((row + col) % 2 === 0) {
            const bottle = document.createElement("img");

            bottle.src = image;
            bottle.className = "bottle";

            bottle.style.gridColumn = col + 1;
            bottle.style.gridRow = row + 1;

            box.appendChild(bottle);
        }
    }
}

const bottles = [...box.querySelectorAll('.bottle')];

let ticking = false;

window.addEventListener('scroll', () => {

    requestAnimationFrame(() => {
        const value = window.scrollY;
        const shift = -Math.sin(value * 0.01) * 30;

        bottles.forEach((bottle) => {
            bottle.style.transform = `
                translateX(${shift * 2}px)
                rotate(${shift}deg)
            `;
        });

    });
}, { passive: true });
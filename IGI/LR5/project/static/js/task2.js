const styleBtn = document.getElementById('styleChange');

let statusStyle = JSON.parse(localStorage.getItem('styleOptions') || 'false');

function applyStyle() {
    document.body.classList.toggle('dark-theme', statusStyle);
    styleBtn.textContent = statusStyle ? "☾" : "☀";
}
function changeStyle() {
    statusStyle = !statusStyle;
    localStorage.setItem('styleOptions', JSON.stringify(statusStyle));
    applyStyle();
}


styleBtn.addEventListener('click', () => changeStyle());
applyStyle();
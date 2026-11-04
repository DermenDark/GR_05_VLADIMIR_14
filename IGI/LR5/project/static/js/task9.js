const map = L.map('map').setView([0, 0], 2);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    referrerPolicy: 'strict-origin-when-cross-origin',
    updateWhenIdle: true
}).addTo(map);

const locationLayer = L.layerGroup().addTo(map);

const mapLink = document.querySelector("#map-link");
const findBtn = document.querySelector("#find-me");


function geoFindMe() {
    const status = document.querySelector("#status");
    mapLink.href = "";
    mapLink.textContent = "";

    locationLayer.clearLayers();

    if (!navigator.geolocation) {
        status.textContent =
            "Geolocation не поддерживается вашим браузером";
        return;
    }

    status.textContent = "Определение местоположения...";

    navigator.geolocation.getCurrentPosition(success, error);


    function success(position) {

        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;
        const accuracy = position.coords.accuracy;

        const coordinates = [latitude, longitude];

        map.setView(coordinates, 16);
        L.marker(coordinates)
            .addTo(locationLayer)
            .bindPopup("Вы находитесь здесь!")
            .openPopup();

        L.circle(coordinates, {
            radius: accuracy,
            color: 'green',
            fillColor: '#39ff14',
            fillOpacity: 0.15
        }).addTo(locationLayer);

        status.textContent =
            `Широта: ${latitude}°, Долгота: ${longitude}°`;
        mapLink.href =
            `https://www.openstreetmap.org/#map=18/${latitude}/${longitude}`;

        mapLink.textContent = "Открыть местоположение в OpenStreetMap";
    }

    function error(event) {

        switch (event.code) {
            case 1:
                status.textContent = "Доступ к местоположению запрещён.";
                break;

            case 2:
                status.textContent = "Информация о местоположении недоступна.";
                break;

            default:
                status.textContent = "Невозможно получить ваше местоположение.";
        }
    }
}

findBtn.addEventListener('click', geoFindMe);

// async function getIP() {
//     const ipElement = document.getElementById('user_ip');

//     try {
//         const response = await fetch('https://api.ipify.org?format=json');
//         const data = await response.json();

//         ipElement.textContent = `Ваш IP: ${data.ip}`;

//     } catch (error) {
//         ipElement.textContent = 'Не удалось определить IP';
//     }
// }

// getIP();
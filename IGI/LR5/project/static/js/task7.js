const birthInput = document.getElementById('id_birth_date');
const birthInfo = document.getElementById('birth_info');

birthInput.addEventListener('change', () => {

    if (!birthInput.value) {
        birthInfo.textContent = '';
        return;
    }

    const [year, month, day] = birthInput.value.split('-').map(Number);

    const birthday = new Date(year, month - 1, day);
    const today = new Date();

    let age = today.getFullYear() - year;

    if (
        today.getMonth() + 1 < month ||
        (today.getMonth() + 1 === month && today.getDate() < day)
    ) {
        age--;
    }
    if (age < 0) {
        birthInfo.textContent =
            `Ваш возраст: введен неправильно.`;
    }
    else if (age < 18) {
        birthInfo.textContent = `Ваш возраст: ${age} лет.`;

        alert(
            "Вы несовершеннолетний! Для использования сайта необходимо разрешение родителей. Разрешение:"
        );
    }
    else {
        const weekday = birthday.toLocaleDateString('ru-RU', {
            weekday: 'long'
        });

        birthInfo.textContent =
            `Ваш возраст: ${age} лет. День рождения: ${weekday}.`;
    }
});
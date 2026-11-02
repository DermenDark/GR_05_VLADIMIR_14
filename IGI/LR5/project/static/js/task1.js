const banner = document.querySelector('.banner');

if (banner) {
    const img = banner.querySelector('.banner__img');
    const caption = banner.querySelector('.banner__caption');
    const counter = banner.querySelector('.banner__counter');
    const dot = banner.querySelector('.banner__dots');
    const dots = [...banner.querySelectorAll('.banner__dot')];
    const prevBtn = banner.querySelector('.banner__btn--prev');
    const nextBtn = banner.querySelector('.banner__btn--next');
    const admin = document.querySelector('.banner__admin');
    const adminBtn = document.querySelector('.banner__admin-set');

    const captions = ['Доступность', 'Удобство', 'Забота о вашем здоровье'];
    const slides = dots.map((dot, i) => ({
        src: dot.dataset.slideSrc,
        caption: captions[i] || ''
    }));

    const saved = JSON.parse(localStorage.getItem('bannerOptions') || '{}');
    const options = {};

    admin.querySelectorAll('[data-opt]').forEach(input => {
        const key = input.dataset.opt;

        if (saved[key] !== undefined) {
            input.type === 'checkbox'
                ? input.checked = saved[key]
                : input.value = saved[key];
        }

        options[key] = input.type === 'checkbox'
            ? input.checked
            : Number(input.value);
    });

    let current = 0;
    let timer;

    function render(index) {
        current = options.loop
            ? (index + slides.length) % slides.length
            : Math.max(0, Math.min(index, slides.length - 1));

        img.src = slides[current].src;
        img.alt = slides[current].caption;
        caption.textContent = slides[current].caption;
        counter.textContent = `${current + 1} / ${slides.length}`;

        dots.forEach((dot, i) =>
            dot.classList.toggle('banner__dot--active', i === current)
        );

        prevBtn.disabled = !options.loop && current === 0;
        nextBtn.disabled = !options.loop && current === slides.length - 1;
    }

    function autoplay() {
        clearTimeout(timer);

        if (options.auto && !document.hidden) {
            timer = setTimeout(() => {
                if (options.loop || current < slides.length - 1) {
                    render(current + 1);
                    autoplay();
                }
            }, options.delay * 1000);
        }
    }

    function goTo(index) {
        render(index);
        autoplay();
    }

    prevBtn.onclick = () => goTo(current - 1);
    nextBtn.onclick = () => goTo(current + 1);

    dots.forEach((dot, i) => dot.onclick = () => goTo(i));

    banner.addEventListener('keydown', e => {
        if (e.key === 'ArrowLeft') goTo(current - 1);
        if (e.key === 'ArrowRight') goTo(current + 1);
    });

    banner.addEventListener('mouseenter', () => {
        if (options.stopMouseHover) clearTimeout(timer);
    });

    banner.addEventListener('mouseleave', autoplay);
    document.addEventListener('visibilitychange', autoplay);

    adminBtn.addEventListener('click', () => {
        admin.querySelectorAll('[data-opt]').forEach(input => {
            const key = input.dataset.opt;

            options[key] = input.type === 'checkbox'
                ? input.checked
                : Math.max(1, Math.min(60, Number(input.value) || 5));

            if (input.type === 'number') {
                input.value = options[key];
            }
        });

        localStorage.setItem('bannerOptions', JSON.stringify(options));

        prevBtn.hidden = nextBtn.hidden = !options.navs;
        dots.forEach(dot => dot.hidden = !options.pags);
        dot.hidden = !options.pags;

        render(current);
        autoplay();
    });

    prevBtn.hidden = nextBtn.hidden = !options.navs;
    dots.forEach(dot => dot.hidden = !options.pags);
    dot.hidden = !options.pags;

    render(0);
    autoplay();
}
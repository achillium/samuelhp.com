(function() {
    const field = document.createElement('div');
    field.id = 'starfield';
    field.className = 'starfield';
    document.body.insertBefore(field, document.body.firstChild);

    function createStarImage(seed, count) {
        let random = seed;
        const nextRandom = () => {
            random = (random * 16807) % 2147483647;
            return (random - 1) / 2147483646;
        };

        let stars = '';
        for (let i = 0; i < count; i++) {
            const x = (nextRandom() * 1000).toFixed(1);
            const y = (nextRandom() * 1000).toFixed(1);
            const radius = (nextRandom() * 1.4 + 0.3).toFixed(2);
            const opacity = (nextRandom() * 0.5 + 0.3).toFixed(2);
            stars += `<circle cx="${x}" cy="${y}" r="${radius}" opacity="${opacity}"/>`;
        }

        const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" preserveAspectRatio="xMidYMid slice"><rect width="1000" height="1000" fill="transparent"/><g fill="white">${stars}</g></svg>`;
        return `data:image/svg+xml,${encodeURIComponent(svg)}`;
    }

    [
        { count: 150, duration: 150 },
        { count: 110, duration: 105 },
        { count: 75, duration: 75 }
    ].forEach((layerConfig, index) => {
        const layer = document.createElement('div');
        layer.className = 'star-layer';
        layer.style.opacity = `${0.65 - index * 0.12}`;

        const track = document.createElement('div');
        track.className = 'star-track';
        track.style.animationDuration = `${layerConfig.duration}s`;
        const seed = Math.floor(Math.random() * 2147483646) + 1;
        const source = createStarImage(seed, layerConfig.count);

        for (let i = 0; i < 2; i++) {
            const image = document.createElement('img');
            image.src = source;
            image.alt = '';
            track.appendChild(image);
        }

        layer.appendChild(track);
        field.appendChild(layer);
    });

    const issSource = new URL('../iss.png', document.currentScript.src).href;

    function launchISS() {
        const iss = document.createElement('img');
        iss.className = 'iss-transit';
        iss.src = issSource;
        iss.alt = '';
        iss.style.setProperty('--iss-start-x', `${Math.random() * 90 - 10}vw`);
        iss.style.setProperty('--iss-end-x', `${Math.random() * 90 + 10}vw`);
        iss.style.setProperty('--iss-rotation', `${Math.random() * 360}deg`);
        document.body.appendChild(iss);
        iss.addEventListener('animationend', () => iss.remove(), { once: true });
    }

    setInterval(launchISS, 120000);
})();

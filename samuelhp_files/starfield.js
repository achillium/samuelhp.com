(function() {
    const canvas = document.createElement('canvas');
    canvas.id = 'starfield';
    canvas.style.cssText = 'position: fixed; inset: 0; width: auto; height: auto; z-index: 0; pointer-events: none;';
    document.body.insertBefore(canvas, document.body.firstChild);

    const ctx = canvas.getContext('2d');
    let stars = [];

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function initStars() {
        stars = [];
        const count = Math.floor((window.innerWidth * window.innerHeight) / 5000);
        for (let i = 0; i < count; i++) {
            stars.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                r: Math.random() * 1.4 + 0.3,
                opacity: Math.random() * 0.5 + 0.3,
                speed: Math.random() * 0.12 + 0.02,
                twinkle: Math.random() * Math.PI * 2,
                twinkleSpeed: Math.random() * 0.015 + 0.003
            });
        }
    }

    let lastFrameTime = 0;

    function animate(timestamp) {
        if (timestamp - lastFrameTime < 33) {
            requestAnimationFrame(animate);
            return;
        }

        const elapsed = Math.min(timestamp - lastFrameTime || 33, 100);
        lastFrameTime = timestamp;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let s of stars) {
            s.y += s.speed * elapsed / 33;
            s.twinkle += s.twinkleSpeed;
            if (s.y > canvas.height + 5) {
                s.y = -5;
                s.x = Math.random() * canvas.width;
            }
            const tw = s.opacity * (0.6 + 0.4 * Math.sin(s.twinkle));
            ctx.beginPath();
            ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(255, 255, 255, ${tw})`;
            ctx.fill();
        }
        requestAnimationFrame(animate);
    }

    resize();
    initStars();
    animate();

    window.addEventListener('resize', () => {
        resize();
        initStars();
    });
})();

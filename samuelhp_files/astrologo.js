(function() {
    const logo = document.querySelector('.logo');
    if (!logo) return;

    let logoSide = 'right';
    let logoTop = -50;
    let lastFrameTime = 0;

    function animateLogo(timestamp) {
        if (timestamp - lastFrameTime < 33) {
            requestAnimationFrame(animateLogo);
            return;
        }

        const elapsed = Math.min(timestamp - lastFrameTime || 33, 100);
        lastFrameTime = timestamp;
        logoTop += 0.15 * elapsed / 16.67;
        if (logoTop > 100) {
            logoTop = -50;
            logoSide = logoSide === 'right' ? 'left' : 'right';
            if (logoSide === 'right') {
                logo.style.left = '';
                logo.style.right = '0vw';
            } else {
                logo.style.right = '';
                logo.style.left = '0vw';
            }
        }
        logo.style.top = logoTop + 'vh';
        requestAnimationFrame(animateLogo);
    }

    logo.style.right = '0vw';
    animateLogo();
})();

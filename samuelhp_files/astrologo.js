(function() {
    const logo = document.querySelector('.logo');
    if (!logo) return;

    let logoSide = 'right';
    let logoTop = -50;

    function animateLogo() {
        logoTop += 0.15;
        if (logoTop > 100) {
            logoTop = -50;
            logoSide = logoSide === 'right' ? 'left' : 'right';
            logo.style.left = logoSide === 'right' ? '75vw' : '5vw';
        }
        logo.style.top = logoTop + 'vh';
        requestAnimationFrame(animateLogo);
    }

    logo.style.left = '75vw';
    animateLogo();
})();

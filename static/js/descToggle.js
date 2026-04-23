function toggleDesc() {
    const short = document.getElementById('desc-short');
    const full  = document.getElementById('desc-full');
    const btn   = document.querySelector('.desc-toggle');
    if (full.classList.contains('d-none')) {
        short.classList.add('d-none');
        full.classList.remove('d-none');
        btn.textContent = 'Show less';
    } else {
        full.classList.add('d-none');
        short.classList.remove('d-none');
        btn.textContent = 'Show full description';
    }
}

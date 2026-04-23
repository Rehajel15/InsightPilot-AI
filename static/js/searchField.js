(function () {
    function filter(query) {
        const tbody = document.getElementById('product-table-body');
        if (!tbody) return;

        const q = (query || '').toLowerCase().trim();
        const rows = tbody.querySelectorAll('tr');
        let count = 0;

        rows.forEach(function (row) {
            if (row.id === 'no-products-row') return;
            const text = row.textContent.toLowerCase();
            if (text.indexOf(q) !== -1) {
                row.style.display = '';
                count++;
            } else {
                row.style.display = 'none';
            }
        });

        const badge = document.getElementById('product-count');
        if (badge) badge.textContent = count + ' Products found';
    }

    function wire(id) {
        const el = document.getElementById(id);
        if (!el) return;
        el.addEventListener('input', function () { filter(el.value); });
    }

    wire('product-search');
    wire('product-search-mobile');
})();

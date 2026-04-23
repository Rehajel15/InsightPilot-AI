(function () {
    const productCountBadge = document.getElementById('product-count');
    const tableBody = document.getElementById('product-table-body');
    if (!tableBody) return;

    const rows = tableBody.getElementsByTagName('tr');

    function filterProducts(searchTerm) {
        searchTerm = searchTerm.toLowerCase();
        let visibleCount = 0;
        for (let i = 0; i < rows.length; i++) {
            if (rows[i].id === 'no-products-row') continue;
            const title = rows[i].cells[1] ? rows[i].cells[1].textContent.toLowerCase() : '';
            const type  = rows[i].cells[3] ? rows[i].cells[3].textContent.toLowerCase() : '';
            if (title.includes(searchTerm) || type.includes(searchTerm)) {
                rows[i].style.display = '';
                visibleCount++;
            } else {
                rows[i].style.display = 'none';
            }
        }
        if (productCountBadge) {
            productCountBadge.textContent = visibleCount + ' Products found';
        }
    }

    function attachSearch(id) {
        const el = document.getElementById(id);
        if (!el) return;
        el.addEventListener('input', function () { filterProducts(el.value); });
        el.addEventListener('keyup',  function () { filterProducts(el.value); });
    }

    attachSearch('product-search');
    attachSearch('product-search-mobile');
}());

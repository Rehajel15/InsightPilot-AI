document.addEventListener('DOMContentLoaded', function() {
    const productCountBadge = document.getElementById('product-count');
    const tableBody = document.getElementById('product-table-body');
    const rows = tableBody.getElementsByTagName('tr');

    function filterProducts(searchTerm) {
        searchTerm = searchTerm.toLowerCase();
        let visibleCount = 0;
        for (let i = 0; i < rows.length; i++) {
            if (rows[i].id === 'no-products-row') continue;
            const title = rows[i].cells[1].textContent.toLowerCase();
            const type = rows[i].cells[3].textContent.toLowerCase();
            if (title.includes(searchTerm) || type.includes(searchTerm)) {
                rows[i].style.display = '';
                visibleCount++;
            } else {
                rows[i].style.display = 'none';
            }
        }
        productCountBadge.textContent = visibleCount + ' Products found';
    }

    const desktopSearch = document.getElementById('product-search');
    const mobileSearch  = document.getElementById('product-search-mobile');

    if (desktopSearch) {
        desktopSearch.addEventListener('input', () => filterProducts(desktopSearch.value));
    }
    if (mobileSearch) {
        mobileSearch.addEventListener('input', () => filterProducts(mobileSearch.value));
    }
});

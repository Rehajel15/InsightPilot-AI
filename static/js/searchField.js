document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('product-search');
    const searchForm = document.getElementById('search-form');
    const productCountBadge = document.getElementById('product-count');
    const tableBody = document.getElementById('product-table-body');
    const rows = tableBody.getElementsByTagName('tr');

    // Prevent page reload on form submit (Enter key)
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
    });

    searchInput.addEventListener('input', function() {
        const searchTerm = searchInput.value.toLowerCase();
        let visibleCount = 0;

        for (let i = 0; i < rows.length; i++) {
            // Skip the row if it's the "empty" message row
            if (rows[i].id === 'no-products-row') continue;

            const title = rows[i].cells[1].textContent.toLowerCase();
            const type = rows[i].cells[3].textContent.toLowerCase();

            if (title.includes(searchTerm) || type.includes(searchTerm)) {
                rows[i].style.display = "";
                visibleCount++;
            } else {
                rows[i].style.display = "none";
            }
        }

        // Update the product counter badge
        productCountBadge.textContent = visibleCount + " Products found";
    });
});
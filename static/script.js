const form = document.querySelector('.search-form');

if (form) {
  form.addEventListener('submit', () => {
    const maxPriceInput = form.querySelector('input[name="max_price"]');
    if (maxPriceInput && !maxPriceInput.value) {
      maxPriceInput.value = 999999999999;
    }
  });
}

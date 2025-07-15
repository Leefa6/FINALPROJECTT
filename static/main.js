// AJAX for Add to Cart (shop and detail pages)
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.add-to-cart-form').forEach(function(form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const url = form.action;
      const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest',
        },
      });
      const data = await response.json();
      if (data.success) {
        // Update cart count in navbar
        const badge = document.querySelector('.navbar .badge.bg-danger');
        if (badge) badge.textContent = data.cart_count;
        // Show a temporary success message
        let msg = document.createElement('div');
        msg.className = 'alert alert-success position-fixed top-0 start-50 translate-middle-x mt-3 shadow';
        msg.style.zIndex = 2000;
        msg.textContent = data.message;
        document.body.appendChild(msg);
        setTimeout(() => msg.remove(), 1800);
      }
    });
  });

  // AJAX for review form (detail page)
  const form = document.getElementById('review-form');
  if (form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const url = form.action;
      const rating = form.rating.value;
      const comment = form.comment.value;
      const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify({ rating, comment })
      });
      const data = await response.json();
      if (response.ok) {
        const reviewsDiv = document.getElementById('reviews');
        const newReview = document.createElement('div');
        newReview.className = 'border rounded p-2 mb-3';
        // Show stars for the rating
        let stars = '';
        for (let i = 1; i <= 5; i++) {
          stars += i <= data.rating ? '★' : '☆';
        }
        newReview.innerHTML = `<strong>${data.reviewer}</strong> - <span>${stars}</span> <span class='text-muted'>(${data.created_at})</span><div>${data.comment}</div>`;
        reviewsDiv.prepend(newReview);
        form.reset();
      } else {
        alert(data.error || 'Error submitting review.');
      }
    });
  }

  // AJAX remove from cart in dropdown
  document.querySelectorAll('.remove-from-cart').forEach(function(button) {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      const url = this.dataset.url;
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '';
      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest',
        },
      })
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          // Remove the item from the DOM
          this.closest('li').remove();
          // Update cart count
          const badge = document.querySelector('.navbar .badge.bg-danger');
          if (badge) badge.textContent = data.cart_count;
        }
      });
    });
  });
}); 
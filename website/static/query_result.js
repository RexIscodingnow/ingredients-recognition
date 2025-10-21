const modal = document.getElementById('recipe-modal');
const modalImg = document.getElementById('modal-img');
const modalTitle = document.getElementById('modal-title');
const modalSteps = document.getElementById('modal-steps');
const modalClose = document.getElementById('modal-close');

document.querySelectorAll('.recipe-card').forEach(card => {
    card.addEventListener('click', () => {
        const name = card.dataset.name;
        const step = card.dataset.step;
        const img = card.dataset.img;

        modalImg.src = img;
        modalTitle.textContent = name;
        modalSteps.textContent = step;

        modal.style.display = 'flex';
    });
});

modalClose.addEventListener('click', () => {
    modal.style.display = 'none';
});

modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.style.display = 'none';
});

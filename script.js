document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('subscribeForm');
    const submitBtn = document.getElementById('submitBtn');
    const messageDiv = document.getElementById('message');
    const btnText = submitBtn.querySelector('span');
    const spinner = submitBtn.querySelector('.spinner');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Reset state
        messageDiv.classList.add('hidden');
        messageDiv.className = 'message hidden';
        submitBtn.disabled = true;
        btnText.textContent = 'Subscribing...';
        spinner.classList.remove('hidden');

        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value
        };

        try {
            const response = await fetch('/api/save_subscriber', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok && data.success) {
                showMessage('Successfully subscribed! Welcome aboard. 🚀', 'success');
                form.reset();
            } else {
                throw new Error(data.message || 'Something went wrong. Please try again.');
            }
        } catch (error) {
            console.error('Submission error:', error);
            showMessage(error.message || 'Failed to connect to the server.', 'error');
        } finally {
            submitBtn.disabled = false;
            btnText.textContent = 'Subscribe Now';
            spinner.classList.add('hidden');
        }
    });

    function showMessage(text, type) {
        messageDiv.textContent = text;
        messageDiv.className = `message ${type}`;
        messageDiv.classList.remove('hidden');
    }
});

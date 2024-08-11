let container = document.getElementById('container');
let currentState = localStorage.getItem('formState'); // Check if there's a stored state

toggle = () => {
    if (container.classList.contains('sign-up')) {
        container.classList.remove('sign-up');
        container.classList.add('sign-in');
        currentState = 'sign-in';
    } else {
        container.classList.remove('sign-in');
        container.classList.add('sign-up');
        currentState = 'sign-up';
    }
    // Update the current state in local storage after toggling
    localStorage.setItem('formState', currentState);
}

// If there's a stored state, set the form to that state
if (currentState === 'sign-up') {
    container.classList.add('sign-up');
} else {
    container.classList.add('sign-in');
}
console.log(currentState);

setTimeout(() => {
    // Ensure the default state is set after a delay
    container.classList.add(currentState);
}, 200);

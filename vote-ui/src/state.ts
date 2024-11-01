import { reactive } from 'vue';

export const state = reactive({
    isLoggedIn: localStorage.getItem('isLoggedIn') === 'true'
});

export function login() {
    state.isLoggedIn = true;
    localStorage.setItem('isLoggedIn', 'true');
}

export function logout() {
    state.isLoggedIn = false;
    localStorage.removeItem('isLoggedIn');
}


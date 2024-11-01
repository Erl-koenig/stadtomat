import { login as loginState, logout as logoutState, state } from '../state';

export const loginService = {
    login,
    logout,
    isLoggedIn
};

function login(username: string, password: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            // TODO: Replace with actual authentication
            if (username === "admin" && password === "admin") {
                loginState();
                resolve(true);
            } else {
                reject(false);
            }
        }, 1000);
    });
}

function logout(): Promise<boolean> {
    return new Promise((resolve) => {
        setTimeout(() => {
            logoutState();
            resolve(true);
        }, 1000);
    });
}

function isLoggedIn(): boolean {
    return state.isLoggedIn;
}
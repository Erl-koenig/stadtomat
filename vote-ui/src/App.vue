<template>
  <div id="app" class="p-12">
    <nav id="nav"
      class="bg-white dark:bg-gray-900 fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-600">
      <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
        <a href="#" @click.prevent class="flex items-center space-x-3 rtl:space-x-reverse">
          <img src="./assets/logo.png"
            class="logo h-28 p-6 transition filter duration-300 hover:drop-shadow-[0_0_2em_rgba(108,133,158,0.67)]"
            alt="Stadtomat Logo" />
        </a>
        <div class="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">

          <button v-if="loginService.isLoggedIn() === true" type="button" @click="loginService.logout"
            class="text-white bg-ostMain hover:bg-ostSecondary focus:ring-2 focus:outline-none focus:ring-ostDark font-medium rounded-lg text-sm px-4 py-2 mr-2 text-center">
            Logout
          </button>

          <button type="button"
            class="text-white bg-ostMain hover:bg-ostSecondary focus:ring-2 focus:outline-none focus:ring-ostDark font-medium rounded-lg text-sm px-4 py-2 text-center">
            Contact
          </button>
          <button @click="toggleMenu" type="button"
            class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
            aria-controls="navbar-sticky" aria-expanded="false">
            <span class="sr-only">Open main menu</span>
            <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M1 1h15M1 7h15M1 13h15" />
            </svg>
          </button>
        </div>
        <div :class="{ 'hidden': !isMenuOpen, 'block': isMenuOpen }"
          class="items-center justify-between w-full md:flex md:w-auto md:order-1" id="navbar-sticky">
          <ul
            class="flex flex-col p-4 md:p-0 mt-4 font-medium border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
            <li>
              <router-link @click="closeMenu" to="/"
                class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-ostSecondary md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
                active-class="text-ostMain">
                Home
              </router-link>
            </li>
            <li>
              <router-link @click="closeMenu" to="/additem"
                class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-ostSecondary md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
                active-class="text-ostMain">
                Add Item
              </router-link>
            </li>
            <li>
              <router-link @click="closeMenu" to="/votes"
                class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-ostSecondary md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
                active-class="text-ostMain">
                Votes
              </router-link>
            </li>
            <li>
              <router-link to="/admin" @click="closeMenu"
                class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-ostSecondary md:p-0 md:dark:hover:text-blue-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent"
                active-class="text-ostMain">
                Admin
              </router-link>
            </li>
          </ul>

        </div>
      </div>
    </nav>
    <div class="ml-5 p-8 pl-0 flex-grow">
      <router-view />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';
import { RouterView } from 'vue-router';
import { loginService } from './services/loginService';
const isMenuOpen = ref(false);
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};
const closeMenu = () => {
  isMenuOpen.value = false;
};

</script>

<template>
  <div id="app" class="flex max-w-screen-xl mx-auto p-8">
    <nav class="w-72 pl-8 pr-8 bg-darkest h-screen fixed top-0 left-0">
      <a href="#" @click.prevent>
        <img src="./assets/logo.png"
          class="logo h-auto 40 p-6 transition filter duration-300 hover:drop-shadow-[0_0_2em_rgba(108,133,158,0.67)]" />
      </a>
      <div class="border-b border-medium my-4"></div>
      <ul class="list-none p-0 flex flex-col items-center mt-4">
        <li class="my-4">
          <router-link to="/" class="font-medium text-light hover:text-medium" active-class="text-lightest">
            Home
          </router-link>
        </li>
        <li class="my-4">
          <router-link to="/additem" class="font-medium text-light hover:text-medium" active-class="text-lightest">
            Add Item
          </router-link>
        </li>
        <li class="my-4">
          <router-link to="/votes" class="font-medium text-light hover:text-medium" active-class="text-lightest">
            Votes
          </router-link>
        </li>
        <li class="my-4">
          <router-link to="/admin" class="font-medium text-light hover:text-medium" active-class="text-lightest">
            Admin
          </router-link>
        </li>
      </ul>
      <div v-if="loginService.isLoggedIn() === true" class="border-t border-medium my-4">
        <button type="button" @click="loginService.logout" class="w-full text-light hover:text-lightest">Logout</button>
      </div>
      <div class="absolute bottom-5 p-0 w-4/5">
        <p class="text-light text-center">Version: {{ version }}</p>
      </div>
    </nav>
    <div class="ml-56 p-8 pl-16 flex-grow">
      <router-view />
    </div>
  </div>
</template>
<script setup lang="ts">
import { RouterView } from 'vue-router';
import packageJson from '../package.json';
import { loginService } from './services/loginService';
const version = packageJson.version;



</script>

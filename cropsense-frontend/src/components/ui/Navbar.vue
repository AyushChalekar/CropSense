<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';

const isMenuOpen = ref(false);
const route = useRoute();

// Automatically close mobile menu when route changes
watch(() => route.path, () => {
  isMenuOpen.value = false;
});
</script>

<template>
  <nav class="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        
        <div class="flex items-center">
          <router-link to="/" class="flex-shrink-0 flex items-center gap-2">
            <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332-4.5 1.253"></path></svg>
            <span class="font-bold text-xl tracking-tight text-gray-900">Crop<span class="text-green-600">Sense</span></span>
          </router-link>
        </div>

        <div class="hidden sm:ml-6 sm:flex sm:items-center sm:space-x-8">
          <router-link to="/" v-slot="{ isActive }">
            <span :class="[
              isActive ? 'border-green-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-green-300 hover:text-gray-700',
              'inline-flex items-center px-1 pt-1 border-b-2 h-16 text-sm font-medium transition-colors cursor-pointer'
            ]">
              Dashboard
            </span>
          </router-link>
          
          <router-link to="/predict" v-slot="{ isActive }">
            <span :class="[
              isActive ? 'border-green-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-green-300 hover:text-gray-700',
              'inline-flex items-center px-1 pt-1 border-b-2 h-16 text-sm font-medium transition-colors cursor-pointer'
            ]">
              Predict
            </span>
          </router-link>
          
          <a href="#" class="border-transparent text-gray-500 hover:border-green-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 h-16 text-sm font-medium">
            History
          </a>
        </div>

        <div class="hidden sm:flex sm:items-center sm:ml-6 space-x-3">
          <router-link to="/login" class="text-gray-600 hover:text-green-600 px-4 py-2 text-sm font-semibold transition-colors">
            Sign In
          </router-link>
          <router-link to="/signup" class="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-lg text-sm font-semibold shadow-sm transition-all duration-200 active:scale-95">
            Sign Up
          </router-link>
        </div>

        <div class="-mr-2 flex items-center sm:hidden">
          <button @click="isMenuOpen = !isMenuOpen" class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-green-500">
            <span class="sr-only">Open main menu</span>
            <svg :class="isMenuOpen ? 'hidden' : 'block'" class="h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg>
            <svg :class="isMenuOpen ? 'block' : 'hidden'" class="h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
      </div>
    </div>

    <div v-show="isMenuOpen" class="sm:hidden bg-white border-t border-gray-100">
      <div class="pt-2 pb-3 space-y-1">
        <router-link to="/" v-slot="{ isActive }">
          <span :class="[
            isActive ? 'bg-green-50 border-green-500 text-green-700' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300',
            'block pl-3 pr-4 py-2 border-l-4 text-base font-medium transition-all'
          ]">Dashboard</span>
        </router-link>

        <router-link to="/predict" v-slot="{ isActive }">
          <span :class="[
            isActive ? 'bg-green-50 border-green-500 text-green-700' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300',
            'block pl-3 pr-4 py-2 border-l-4 text-base font-medium transition-all'
          ]">Predict</span>
        </router-link>
      </div>
      
      <div class="pt-4 pb-3 border-t border-gray-200">
        <div class="flex flex-col space-y-2 px-4">
          <router-link to="/login" class="text-center w-full text-gray-600 font-medium py-2 hover:bg-gray-50 rounded-md">Sign In</router-link>
          <router-link to="/signup" class="text-center w-full bg-green-600 text-white font-medium py-2 rounded-md shadow-sm active:scale-95 transition-transform">Sign Up</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>
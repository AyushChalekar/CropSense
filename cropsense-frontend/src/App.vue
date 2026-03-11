<script setup lang="ts">
import { RouterView } from 'vue-router';
import Navbar from './components/ui/Navbar.vue'; // Adjust the path to where your Navbar is saved
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />

    <main>
      <RouterView />
    </main>
  </div>
</template>

<style>
/* Basic reset for minimalist look */
body {
  margin: 0;
  font-family: 'Inter', sans-serif;
  background-color: #f8f9fa;
  color: #333;
}
</style>
<script setup lang="ts">
import { ref } from 'vue';

const name = ref('');
const email = ref('');
const password = ref('');
const termsAccepted = ref(false);

const handleSignup = () => {
  console.log('Signing up:', name.value, email.value);
};
</script>

<template>
  <div class="min-h-[calc(100vh-64px)] bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md text-center">
      <h2 class="text-3xl font-extrabold text-gray-900">Join CropSense</h2>
      <p class="mt-2 text-sm text-gray-600">Start optimizing your agricultural yield today</p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow-xl border border-gray-100 sm:rounded-xl sm:px-10">
        <form @submit.prevent="handleSignup" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700">Full Name</label>
            <input v-model="name" type="text" placeholder="John Doe" required 
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Email address</label>
            <input v-model="email" type="email" placeholder="farmer@example.com" required 
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Password</label>
            <input v-model="password" type="password" placeholder="••••••••" required 
              class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-green-500 focus:border-green-500 sm:text-sm" />
          </div>

          <div class="flex items-start">
            <div class="flex items-center h-5">
              <input v-model="termsAccepted" id="terms" type="checkbox" required
                class="h-4 w-4 text-green-600 focus:ring-green-500 border-gray-300 rounded" />
            </div>
            <div class="ml-3 text-sm">
              <label for="terms" class="text-gray-600">I agree to the <a href="#" class="text-green-600 underline">Terms of Service</a></label>
            </div>
          </div>

          <button type="submit" 
            class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-semibold text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all active:scale-95">
            Create Account
          </button>
        </form>

        <div class="mt-6 text-center text-sm">
          <span class="text-gray-500">Already have an account?</span>
          <router-link to="/login" class="ml-1 font-medium text-green-600 hover:text-green-500">Sign in</router-link>
        </div>
      </div>
    </div>
  </div>
</template>
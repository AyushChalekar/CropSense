// ./Dashboard.vue
<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Navbar from '../components/ui/Navbar.vue'; // Import the new Navbar

const router = useRouter();

const recentPredictions = ref([
  { id: 1, date: '2023-10-24', crop: 'Rice', predictedYield: '4.2 Tons/Ha' },
  { id: 2, date: '2023-10-22', crop: 'Wheat', predictedYield: '3.8 Tons/Ha' },
  { id: 3, date: '2023-10-20', crop: 'Maize', predictedYield: '5.1 Tons/Ha' },
]);

const navigateToPredict = () => {
  router.push('/predict');
};
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <Navbar />

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <header class="bg-gradient-to-r from-green-600 to-green-800 rounded-2xl shadow-lg p-10 text-center text-white mb-10 transform transition hover:scale-[1.01] duration-300">
        <h1 class="text-4xl md:text-5xl font-bold mb-3 tracking-tight">
          Welcome to CropSense
        </h1>
        <p class="text-green-50 text-lg md:text-xl font-medium opacity-90">
          Intelligent Paddy Harvest Forecasting System
        </p>
      </header>

      <main class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        
        <section class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all duration-300 hover:-translate-y-1">
          <div class="flex items-center justify-between mb-4 border-b-2 border-green-500 pb-2">
             <h2 class="text-xl font-bold text-slate-800">New Forecast</h2>
             <span class="text-green-500 text-2xl">🌱</span>
          </div>
          <p class="text-slate-600 mb-6 leading-relaxed">
            Input soil and weather parameters to generate a new high-accuracy yield prediction.
          </p>
          <button 
            @click="navigateToPredict" 
            class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg shadow-sm transition-colors duration-200 flex justify-center items-center gap-2"
          >
            Start Prediction
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
          </button>
        </section>

        <section class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all duration-300 hover:-translate-y-1">
           <div class="flex items-center justify-between mb-4 border-b-2 border-blue-500 pb-2">
             <h2 class="text-xl font-bold text-slate-800">System Status</h2>
             <span class="text-blue-500 text-2xl">⚡</span>
          </div>
          
          <div class="space-y-4">
            <div class="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
              <span class="text-slate-600 font-medium">Model Accuracy (MAE)</span>
              <span class="text-blue-600 font-bold bg-blue-50 px-3 py-1 rounded-full text-sm">0.42</span>
            </div>
            <div class="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
              <span class="text-slate-600 font-medium">Model Version</span>
              <span class="text-slate-800 font-mono text-sm bg-gray-200 px-2 py-1 rounded">v1.0.2</span>
            </div>
            <div class="flex justify-between items-center p-3 bg-slate-50 rounded-lg">
              <span class="text-slate-600 font-medium">Server Status</span>
              <span class="flex items-center gap-2 text-green-600 font-bold text-sm">
                <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> Online
              </span>
            </div>
          </div>
        </section>

        <section class="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-all duration-300 hover:-translate-y-1">
          <div class="flex items-center justify-between mb-4 border-b-2 border-amber-500 pb-2">
             <h2 class="text-xl font-bold text-slate-800">Recent Activity</h2>
             <span class="text-amber-500 text-2xl">📋</span>
          </div>
          
          <ul class="space-y-3">
            <li v-for="prediction in recentPredictions" :key="prediction.id" class="flex justify-between items-center p-3 hover:bg-gray-50 rounded-lg transition-colors border-b border-gray-50 last:border-0">
              <div class="flex flex-col">
                <span class="text-xs text-gray-400 font-medium uppercase tracking-wider">{{ prediction.date }}</span>
                <span class="text-slate-800 font-semibold">{{ prediction.crop }}</span>
              </div>
              <span class="text-green-700 font-bold bg-green-50 px-3 py-1 rounded-full text-sm">
                {{ prediction.predictedYield }}
              </span>
            </li>
          </ul>
        </section>

      </main>
    </div>
  </div>
</template>